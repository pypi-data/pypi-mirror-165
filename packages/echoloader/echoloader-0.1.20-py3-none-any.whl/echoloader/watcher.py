import argparse
import base64
import csv
import json
import logging
import math
import os
import socket
import sys
import threading
import time
import traceback
from getpass import getpass
from io import BytesIO
from multiprocessing.dummy import Pool
from pathlib import Path
from time import sleep

import cv2
import imageio
import numpy as np
import pydicom
import requests
from pydicom import uid
from pydicom.encaps import encapsulate, generate_pixel_data_frame
from pydicom.errors import InvalidDicomError
from pydicom.pixel_data_handlers import apply_color_lut
from pynetdicom import AE, evt, ALL_TRANSFER_SYNTAXES
from pynetdicom.sop_class import UltrasoundMultiframeImageStorage, UltrasoundImageStorage
from tqdm import tqdm
from watchdog.events import FileCreatedEvent, FileMovedEvent, FileModifiedEvent
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from echoloader.lib import unpack
from echoloader.sync import PacsConnection, Sync

logger = logging.getLogger('echolog')
OS_VAR_PREFIX = 'US2_'


class ENV:
    def __init__(self, env):
        prefix = "" if env and env == "production" else env + "-"
        self.cloud = '://' not in env
        self.api_url = f"https://{prefix}api.us2.ai" if self.cloud else env


class Auth:
    auth_mutex = threading.Lock()

    def __init__(self, args, username, password):
        self.args = args
        self.api_url = args.env.api_url
        self.username = username
        self.password = password
        self.id_token = ''
        self.refresh_token = ''
        self.payload = {}
        self.exp = 0
        self.groups = []
        self.sub = ''
        self.authenticate()

    def expired(self):
        return time.time() > self.exp - 5

    def unpack_auth(self, request):
        data = unpack(request)
        auth = data['AuthenticationResult']
        self.id_token = auth['IdToken']
        self.refresh_token = auth.get('RefreshToken', self.refresh_token)
        self.payload = json.loads(base64.b64decode(self.id_token.split('.')[1] + '===').decode())
        self.exp = self.payload['exp']
        user = unpack(requests.get(f"{self.api_url}/users/current", headers=self.get_headers()))
        self.groups = user.get('permissions', [])
        self.sub = user.get('cognito_id')

    def authenticate(self):
        self.unpack_auth(
            requests.post(f"{self.api_url}/users/login", json={'username': self.username, 'password': self.password}),
        )

    def check_token(self):
        if self.expired():
            with self.auth_mutex:
                try:
                    self.unpack_auth(
                        requests.post(f"{self.api_url}/users/refresh", json={'refreshToken': self.refresh_token}),
                    )
                except Exception as exc:
                    logger.warning(f'Failed to renew token due to {exc}, re-authenticating')
                    self.authenticate()

    def customer(self):
        groups = self.groups
        s3 = [g for g in groups if g.startswith('s3-')]
        if s3:
            return s3[0].split('-', 1)[1]
        if 'upload' in groups:
            return self.sub

    def get_headers(self):
        self.check_token()
        return {"Authorization": f"Bearer {self.id_token}"}


def is_video(img=None, shape=None):
    shape = shape or (isinstance(img, np.ndarray) and img.shape)
    return shape and (len(shape) == 4 or (len(shape) == 3 and shape[-1] > 4))


def ybr_to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_YCR_CB2BGR)


def blank_top_bar(media, regions):
    video = is_video(media)
    image = np.mean(media, axis=0) if video else media
    new_image = np.mean(image[..., :3], axis=-1) if 3 <= image.shape[-1] <= 4 else image
    binary_image = (new_image > 2).astype('uint8')
    h = int(binary_image.shape[0] * 0.2)
    sum_pixel = np.sum(binary_image[:h, :], axis=1)
    top_bar = np.where(sum_pixel > (binary_image.shape[0] * 0.88))
    top_bar_bottom = 0
    if len(top_bar[0]) != 0:
        new_image[top_bar, :] = 0
        image[top_bar, :] = 0
        top_bar_bottom = top_bar[0][-1] + 1
    top_bar_bottom = max(top_bar_bottom, 40)
    mask = np.ones_like(media[0] if video else media)
    mask[:top_bar_bottom] = 0
    for region in regions:
        xo, xn = region.RegionLocationMinX0, region.RegionLocationMaxX1
        yo, yn = region.RegionLocationMinY0, region.RegionLocationMaxY1
        mask[yo:yn, xo:xn] = 1
    media *= mask


def mpeg4hp41(ds):
    frames = imageio.mimread(next(generate_pixel_data_frame(ds.PixelData)), memtest=False, format='mp4')
    return np.asarray(frames)


def unusual_frame_mean(px: np.ndarray, threshold=58):
    """
    If mean pixel value of frame is larger than threshold, background is likely non-black
    (usually happens when dicom tag is RGB but the frames are actually in YBR).
    """
    frame = px[px.shape[0] // 2] if is_video(px) else px  # take middle frame for video
    return frame.mean() > threshold


def parse_dicom_pixel(dicom):
    """Parse color space and coerce to RGB, and anonymize by blanking out top bar."""
    try:
        px = dicom.pixel_array
    except NotImplementedError as exc:
        handler = parse_dicom_pixel.custom_handlers.get(dicom.file_meta.TransferSyntaxUID)
        if not handler:
            raise exc
        px = handler(dicom)
    pi = dicom.PhotometricInterpretation
    dicom.PhotometricInterpretation = 'RGB'
    if pi in ['YBR_FULL', 'YBR_FULL_422', 'RGB'] and unusual_frame_mean(px):
        px = np.asarray([ybr_to_rgb(img) for img in px]) if is_video(px) else ybr_to_rgb(px)
    elif pi in ['PALETTE COLOR']:
        px = (apply_color_lut(px, dicom) // 255).astype('uint8')
    else:
        dicom.PhotometricInterpretation = pi
    return px


parse_dicom_pixel.custom_handlers = {
    uid.MPEG4HP41: mpeg4hp41,
}


def ensure_even(stream):
    # Very important for some viewers
    if len(stream) % 2:
        return stream + b"\x00"
    return stream


def person_data_callback(ds, e):
    if e.VR == "PN" or e.tag == (0x0010, 0x0030):
        del ds[e.tag]


def pad_to_multiple(arr, size, dims=(1, 2)):
    pad_dims = [(0, size - (s % size)) if i in dims else (0, 0) for i, s in enumerate(arr.shape)]
    return np.pad(arr, pad_dims, 'constant')


def compress_dicom(ds, anonymize):
    # Populate required values for file meta information
    ds.remove_private_tags()
    media = parse_dicom_pixel(ds)
    if anonymize:
        ds.walk(person_data_callback)
        blank_top_bar(media, getattr(ds, "SequenceOfUltrasoundRegions", []))
    video = is_video(media)

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    if len(media.shape) < 3 + video:
        media = np.repeat(np.expand_dims(media, -1), 3, -1)
    ds.Rows, ds.Columns, ds.SamplesPerPixel = media.shape[video:]
    ds.PhotometricInterpretation = "RGB"
    if video:
        ds.StartTrim = 1
        ds.StopTrim = ds.NumberOfFrames = media.shape[0] if video else 1
        fps = getattr(ds, 'CineRate', 1000 / getattr(ds, 'FrameTime', 40))
        ds.CineRate = ds.RecommendedDisplayFrameRate = round(fps, 2)
        ds.FrameTime = 1000 / ds.CineRate
        ds.ActualFrameDuration = math.ceil(1000 / ds.CineRate)
        ds.PreferredPlaybackSequencing = 0
        ds.FrameDelay = 0
        ds.file_meta.TransferSyntaxUID = uid.MPEG4HP41
        ds.PixelData = encapsulate([
            imageio.mimwrite(imageio.RETURN_BYTES, pad_to_multiple(media, 16), fps=fps, format='mp4')])
    else:
        ds.file_meta.TransferSyntaxUID = uid.JPEGBaseline8Bit
        ds.PixelData = encapsulate([imageio.imwrite(imageio.RETURN_BYTES, media, format='jpg')])
    ds['PixelData'].is_undefined_length = True


def wait_file(path):
    path = Path(path)
    old = None
    cur = os.path.getsize(path)
    while old != cur or not cur:
        sleep(1)
        old, cur = cur, os.path.getsize(path)


class Handler(FileSystemEventHandler):
    def __init__(self, args):
        self.args = args
        self.pool = Pool(args.n)
        self.pbar = tqdm(total=0)
        self.closed = False
        self.write(['customer', 'trial', 'patientID', 'visit', 'filename'])

    def processing(self):
        return self.pbar.n < self.pbar.total

    def write(self, row):
        if self.args.csv_out:
            csv.writer(open(self.args.csv_out, 'a', newline='')).writerow(row)

    def stop(self):
        self.closed = True
        self.pool.terminate()

    def join(self):
        self.pool.join()

    def file_params(self, ds, ae_title):
        customer = getattr(self.args, 'customer', '') or ae_title
        return {
            'customer': customer,
            'trial': customer,
            'patient_id': ds.PatientID,
            'visit_id': ds.StudyID or ds.StudyInstanceUID or ds.StudyDate or 'No Study ID',
            'filename': f"{ds.SOPInstanceUID}.dcm",
        }

    def upload(self, ds, param):
        content_type = 'application/dicom'
        auth = self.args.auth
        env = self.args.env
        headers = auth.get_headers()
        param['content_type'] = content_type
        upload_param = {}
        url = f"{auth.api_url}/dicom/upload"
        if env.cloud:
            r = requests.get(url, params=param, headers=headers)
            d = unpack(r)
            url = d['url']
            headers = d['headers']
        else:
            upload_param = param
        buf = BytesIO()
        ds.save_as(buf)
        buf.seek(0)
        return unpack(requests.put(url, data=buf.read(), headers=headers, params=upload_param))

    def process(self, path=None, ds=None, ae_title=None):
        self.pbar.disable = False
        if self.closed:
            return
        path = path and Path(path)
        params = self.file_params(ds or pydicom.dcmread(path, stop_before_pixels=True), ae_title=ae_title)
        extracted = self.args.extracted
        k = tuple(params.values())
        if k not in extracted:
            ds = ds or pydicom.dcmread(path)
            compress_dicom(ds, anonymize=self.args.anonymize)
            dst = self.args.dst
            if dst:
                src = self.args.src
                rel = path.relative_to(src) if src else f"{ds.SOPInstanceUID}.dcm"
                out = (Path(dst) / rel).with_suffix(".dcm")
                if self.args.overwrite or not out.is_file():
                    out.parent.mkdir(exist_ok=True, parents=True)
                    ds.save_as(out)
            if hasattr(self.args, "auth"):
                self.upload(ds, params)
            extracted.add(k)
            self.write(k)
        self.pbar.update(1)

    def handle_err(self, err, vargs, kwargs):
        if isinstance(err, InvalidDicomError):
            logger.debug(f'Error during process call: {err}, vargs: {vargs}, kwargs: {kwargs}')
            self.pbar.total -= 1
            self.pbar.update(0)
            return
        logger.error(f'Error during process call: {err}, vargs: {vargs}, kwargs: {kwargs}')
        logger.debug(traceback.format_tb(err.__traceback__))
        self.pbar.update(1)

    def handle(self, *vargs, **kwargs):
        self.pbar.total += 1
        self.pbar.refresh()
        self.pool.apply_async(self.process, vargs, kwargs,
                              error_callback=lambda err: self.handle_err(err, vargs, kwargs))

    def on_any_event(self, event):
        logger.debug(f'got event {event}')
        if isinstance(event, (FileCreatedEvent, FileMovedEvent, FileModifiedEvent)):
            path = event.src_path
            wait_file(path)
            self.handle(path)


def handle_store(event, handler):
    """Handle EVT_C_STORE events."""
    remote_ae_title = event.assoc.remote['ae_title'].strip().decode()
    ds = event.dataset
    ds.file_meta = event.file_meta
    ds.preamble = b"\0" * 128
    handler.handle(ds=ds, ae_title=remote_ae_title)
    return 0x0000


def extracted_list(path):
    return {tuple(row) for row in csv.reader(open(path))}


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()


def main():
    parser = argparse.ArgumentParser('EchoLoader')
    parser.add_argument(
        "--src", type=Path,
        help="The folder to anonymize")
    parser.add_argument(
        "--dst",
        help="The output folder for the anonymized DICOM, defaults to src folder suffixed with '_anonymized'")
    parser.add_argument(
        "--watch", action="store_true",
        help="Watch the src folder for changes")
    parser.add_argument(
        "--pacs", action="store_true",
        help="Starts PACS server")
    parser.add_argument(
        "--pacs-ae-title", default="Us2.ai",
        help="PACS AE Title, defaults to Us2.ai")
    parser.add_argument(
        "--pacs-port", default=11112, type=int,
        help="PACS port, defaults to 11112")
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Overwrite files in the output folder")
    parser.add_argument(
        "--n", type=int, default=4,
        help="Number of workers")
    parser.add_argument(
        "--upload", action='store_true',
        help="Will upload all anonymized imaging to Us2.ai cloud")
    parser.add_argument(
        "--env", type=ENV,
        help="The Us2.ai environment to use")
    parser.add_argument(
        "--extracted", type=extracted_list, default=set(),
        help="File of cases to ignore - csv file with customer, trial, patientID, visit, filename")
    parser.add_argument(
        "--csv-out",
        help="Path to csv file of extracted cases")
    parser.add_argument(
        "--verbose", action='store_true',
        help="Path to csv file of extracted cases")
    parser.add_argument(
        '--no-anonymization', action='store_false', dest='anonymize',
        help="No anonymization of data prior to upload",
    )
    parser.add_argument(
        '--customer',
        help="The customer tag used for the upload (Admin only)",
    )
    parser.add_argument(
        '--sync',
        nargs='+',
        default=[],
        type=PacsConnection,
        help="Will try to sync structured report back to specified location. Format: IP:PORT:AE_TITLE",
    )
    parser.add_argument(
        '--sync-url',
        default=False,
        action='store_true',
        help='Include url to measurement page in SR export',
    )
    parser.add_argument(
        '--sync-main-findings',
        default=False,
        action='store_true',
        help='Include main findings in SR export',
    )
    args = parser.parse_args(sys.argv[1:])
    args.env = args.env or ENV('production')
    if args.verbose:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
    if args.upload or args.sync:
        args.auth = Auth(
            args,
            os.environ.get(f"{OS_VAR_PREFIX}COGNITO_USERNAME") or input("username: "),
            os.environ.get(f"{OS_VAR_PREFIX}COGNITO_PASSWORD") or getpass("password: "),
        )
        args.customer = args.customer or args.auth.customer()
    handler = Handler(args)
    sync = None
    try:
        if args.src:
            src = args.src
            paths = [src] if src.is_file() else [p for p in src.rglob("*") if p.is_file()]
            args.n = len(paths)
            args.i = 0
            for path in paths:
                handler.handle(path)
            if args.watch:
                logger.warning(f"watching folder {os.path.abspath(src)}")
                src.mkdir(exist_ok=True, parents=True)
                observer = args.observer = Observer()
                observer.schedule(handler, src, recursive=True)
                observer.start()
        if args.sync:
            sync = Sync(args)
            sync.start()
        if args.pacs:
            logger.warning(
                f"Starting pacs server on {get_ip()}:{args.pacs_port} with AE title {args.pacs_ae_title}")
            handlers = [(evt.EVT_C_STORE, handle_store, [handler])]
            ae = AE()
            ae.add_supported_context(UltrasoundMultiframeImageStorage, ALL_TRANSFER_SYNTAXES)
            ae.add_supported_context(UltrasoundImageStorage, ALL_TRANSFER_SYNTAXES)
            ae.start_server(('0.0.0.0', args.pacs_port), block=True, evt_handlers=handlers, ae_title=args.pacs_ae_title)
        while hasattr(args, 'observer') or handler.processing() or sync:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("Interrupted, finishing up jobs")
    finally:
        to_wait = [handler, getattr(args, 'observer', None), sync]
        to_wait = [e for e in to_wait if e]
        for e in to_wait:
            e.stop()
        for e in to_wait:
            e.join()
