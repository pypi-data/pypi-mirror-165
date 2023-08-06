import datetime
import io
import logging
import threading
import time

import requests
from dateutil import parser
from pydicom import dcmread
from pynetdicom import AE

from echoloader.lib import unpack

logger = logging.getLogger('echolog')


class PacsConnection:
    def __init__(self, details):
        self.host, port, self.ae_title = details.split(':')
        self.port = int(port)

    def store(self, ds):
        ae = AE(ae_title=self.ae_title)
        ae.add_requested_context(ds.SOPClassUID, ds.file_meta.TransferSyntaxUID)
        assoc = ae.associate(self.host, self.port)
        if not assoc.is_established:
            logger.error('Association rejected, aborted or never connected')
            return
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        try:
            # force treat context as supporting the SCP role
            for cx in assoc.accepted_contexts:
                cx._as_scp = True

            status = assoc.send_c_store(ds)

            # Check the status of the storage request
            if status:
                # If the storage request succeeded this will be 0x0000
                logger.debug(f'C-STORE request status: 0x{status.Status:04x}')
            else:
                logger.error('Connection timed out, was aborted or received invalid response')
        finally:
            # Release the association
            assoc.release()

    def __str__(self):
        return f"{self.host}:{self.port}"


class Sync(threading.Thread):
    def __init__(self, cmd, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.args = cmd
        self.connections = cmd.sync
        self.auth = cmd.auth
        self.api_url = self.auth.api_url
        self.customer = cmd.customer
        self.killed = False
        self.search = f"{self.api_url}/study/search?customer={self.customer}&reportCompleted=true"
        self.last_sync = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
        self.params = {}
        if cmd.sync_url:
            self.params['url'] = True
        if cmd.sync_main_findings:
            self.params['main_findings'] = True

    def sr(self, study):
        return f"{self.api_url}/study/sr/{study}"

    def stop(self):
        self.killed = True

    def sync(self):
        t = self.last_sync
        res = unpack(requests.get(self.search, headers=self.auth.get_headers()), {})
        results = res.get('results', [])
        for study in results:
            sid = study['id']
            try:
                pd = parser.parse(study['processedDate']).replace(tzinfo=datetime.timezone.utc)
                if pd > self.last_sync:
                    bs = unpack(requests.get(self.sr(sid), headers=self.auth.get_headers(), params=self.params))
                    ds = dcmread(io.BytesIO(bs))
                    for conn in self.connections:
                        conn.store(ds)
                        logger.info(f'Synced {sid} to {conn}')
                t = max(pd, t)
            except Exception as exc:
                logger.error(f'Failed to sync SR for {sid} due to {exc}')
        self.last_sync = t

    def run(self) -> None:
        while not self.killed:
            try:
                self.sync()
            except Exception as exc:
                logger.error(f'Failed sync due to: {exc}')
            time.sleep(10)
