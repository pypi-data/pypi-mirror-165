from googleapiclient import discovery
from googleapiclient import http
from google.oauth2 import service_account

import os
import io

class DCM:
    """
    The DCM class is scoped to the REPORT level.
    Each instance should be associated with a specific report that needs to be retried.
    """

    # instance attributes
    def __init__(self, report_id, key, profile_id):
        self.report_id = report_id
        self.key=key
        self.profile_id = profile_id
        self.file_id = None
        self.file_name = None
        self.filename_path = None

        credentials = service_account.Credentials.from_service_account_info(self.key)
        self.service = discovery.build('dfareporting', 'v3.5', credentials=credentials)


    def find_file(self):
        """return latest file_id for a given report"""

        # identify target file
        target = None
        request = self.service.reports().files().list(profileId=self.profile_id,
                                                 reportId=self.report_id,
                                                 sortField="LAST_MODIFIED_TIME",
                                                 sortOrder="DESCENDING")
        response = request.execute()

        # iterate through the resource object until you find most recent available file
        for report_file in response['items']:
            if report_file['status'] == 'REPORT_AVAILABLE':  # take last avail file.
                # TODO: in theory should work, but will want to account for edge cases
                target = report_file
                break

        if not target and response['items'] and response['nextPageToken']:
            request = self.service.reports().files().list_next(request, response)

        file_id = target['id']

        self.file_id = file_id

        return self.file_id

    def generate_filename(self, report_file=None, file_id=None):
        """Generates a report file name based on the file metadata."""

        # if report_file is not already specified, get metadata
        if report_file is None:
            report_file = self.service.files().get(reportId=self.report_id, fileId=file_id).execute()

        # craft the filename
        file_name = report_file['fileName'] \
                    + '_' \
                    + report_file['id'] \
                    + '_' \
                    + report_file["dateRange"]["startDate"] \
                    + "_" \
                    + report_file["dateRange"]["endDate"]

        extension = '.csv' if report_file['format'] == 'CSV' else '.xml'

        self.file_name = file_name + extension

        return self.file_name

    def generate_filename_path(self, file_name):
        """Generates a report file name and path based on the file metadata."""

        path = os.getcwd()
        self.filename_path = path + '/' + file_name

        return self.filename_path

    def media_download(self):
        """Request the file to be downloaded and download"""

        file_id = self.find_file()
        
        # retrieve target file metadata
        target_file = self.service.files().get(reportId=self.report_id, fileId=file_id).execute()

        # prepare outfile, establish class instance vars for filename and path.
        file_name = self.generate_filename(report_file=target_file)
        file_name_path = self.generate_filename_path(file_name=file_name)
        out_file = io.FileIO(file_name_path, mode='wb')

        # create get request
        request = self.service.files().get_media(reportId=self.report_id, fileId=file_id)

        # create media downloader instance
        downloader = http.MediaIoBaseDownload(out_file, request)

        # execute get request and download file
        download_finished = False
        while download_finished is False:
            _, download_finished = downloader.next_chunk()


if __name__=='__main__':
    pass