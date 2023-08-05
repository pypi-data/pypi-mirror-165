from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import HttpError
import httplib2

from io import BytesIO
import os
import sys
import time

class GCS:

    def __init__(self, key):
        self.key = key
        scopes = ['https://www.googleapis.com/auth/cloud-platform'] #https://cloud.google.com/storage/docs/authentication
        credentials = service_account.Credentials.from_service_account_info(self.key, scopes=scopes)
        self.service = build('storage', 'v1', credentials=credentials)

        self.RETRYABLE_ERRORS = (httplib2.HttpLib2Error, IOError)
        self.NUM_RETRIES = 5  # Number of times to retry failed downloads.
        self.DEFAULT_MIMETYPE = 'application/octet-stream'  # Mimetype to use if one can't be guessed from the file extension.
        # format of bucket-object URI should be gs://bucket/object

    # https://github.com/GoogleCloudPlatform/storage-file-transfer-json-python/blob/master/chunked_transfer.py
    def handle_progressless_iter(self, error, progressless_iters):
        if progressless_iters > self.NUM_RETRIES:
            print ('failed to make progress for too many consecutive iterations')
            raise error

        sleeptime = 30 * (2**progressless_iters)
        print ('Caught exception (%s). Sleeping for %s seconds before retry #%d.'
             % (str(error), sleeptime, progressless_iters))
        time.sleep(sleeptime)

    def download(self, bucket, object, destination_filename, chunksize=2 * 1024 * 1024):
        """download file"""
        file = open(destination_filename, 'xb')
        request = self.service.objects().get_media(bucket=bucket, object=object)
        media = MediaIoBaseDownload(file, request, chunksize=chunksize)

        print(f'Downloading from bucket {bucket}, object {object} to {destination_filename}')

        progressless_iters = 0
        done = False
        while not done:
            error = None
            try:
                progress, done = media.next_chunk()
                if progress:
                    print('Download %d%%.' % int(progress.progress() * 100))
            except HttpError as err:
                error=err
                if err.resp.status < 500:
                    raise
            except self.RETRYABLE_ERRORS as err:
                error = err

            if error:
                progressless_iters += 1
                self.handle_progressless_iter(error, progressless_iters)
            else:
                progressless_iters = 0

        print('Download complete')

    #TODO: probably requires update
    def upload(self, bucket, object, source_filename, chunksize=2 * 1024 * 1024):
        """upload a file to specified bucket and object"""

        media = MediaFileUpload(source_filename, chunksize=chunksize, resumable=True)
        if not media.mimetype():
            media = MediaFileUpload(source_filename, mimetype=self.DEFAULT_MIMETYPE, resumable=True)
        request = self.service.objects().insert(bucket=bucket,
                                                name=object,
                                                media_body=media)

        progressless_iters = 0
        response = None
        while response is None:
            error = None
            try:
                progress, response = request.next_chunk()
                if progress:
                    print('Upload %d%%' % (100 * progress.progress()))
            except HttpError as err:
                error = err
                if err.resp.status < 500:
                    raise
            except self.RETRYABLE_ERRORS as err:
                error = err

            if error:
                progressless_iters += 1
                self.handle_progressless_iter(error, progressless_iters)
            else:
                progressless_iters = 0

        print('Upload complete!')

    def delete_object(self, bucket, object):
        """delete specified object"""

        request = self.service.objects().delete(bucket=bucket,
                                                name=object)

        response = request.execute()

        return response