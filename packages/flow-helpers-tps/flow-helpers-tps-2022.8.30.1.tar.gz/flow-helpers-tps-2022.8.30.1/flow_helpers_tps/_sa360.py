from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

import os
import time
import json
import sys

class SA360:
    """
    The SA 360 class is scoped to the ADVERTISER.
    Each class instance will be associated with the advertiser, and can be re-used to retrieve multiple reports.
    Best practice though is probably to generate 1 instance per report.
    """

    def __init__(self, key, agency_id, advertiser_id):
        self.key=key
        self.agency_id=agency_id
        self.advertiser_id=advertiser_id
        self.file_id = None
        self.filenamepathdict={}

        credentials = service_account.Credentials.from_service_account_info(self.key)
        self.service = discovery.build('doubleclicksearch', 'v2', credentials=credentials)

#https://developers.google.com/search-ads/v2/how-tos/reporting/asynchronous-requests
    def generate_request(self, sdate, edate, reportType, columns, filters):
        """construct a report request"""

        columnlist = []
        filterclauselist = []

        for each in columns:
            dict = {'columnName': each}
            columnlist.append(dict)

        if filters == '':
            requestbody={
                'reportScope': {
                    'agencyId': self.agency_id,
                    'advertiserId': self.advertiser_id},
                'reportType': reportType,
                'columns': columnlist,
                'timeRange': {
                    'startDate': sdate,
                    'endDate': edate},
                'includeDeletedEntities': True,
                'includeRemovedEntities': True,
                'verifySingleTimeZone':False,
                'downloadFormat': 'csv',
                'statisticsCurrency': 'agency',
                'maxRowsPerFile': 100000000
            }

        elif filters != '':
            for each in filters:
                dict = {
                        'column': {
                            'columnName': each[0]},
                        'operator': each[1],
                        'values': [each[2]]}
                filterclauselist.append(dict)

            requestbody = {
                'reportScope': {
                    'agencyId': self.agency_id,
                    'advertiserId': self.advertiser_id},
                'reportType': reportType,
                'columns': columnlist,
                'timeRange': {
                    'startDate': sdate,
                    'endDate': edate},
                'filters':filterclauselist,
                'includeDeletedEntities': True,
                'includeRemovedEntities': True,
                'verifySingleTimeZone': True,
                'downloadFormat': 'csv',
                'statisticsCurrency': 'agency',
                'maxRowsPerFile': 100000000
            }

        return requestbody


    def find_file(self, requestbody):

        # execute the report request. if request is valid, SA360 will return response with file_id
        service = self.service
        request = service.reports().request(body=requestbody)
        response = request.execute()

        self.reportfile_id=response['id']

        return self.reportfile_id


    def generate_filename(self, name, reportfile_id, report_fragment):
        """Generates a report file name per fragment based on the file metadata."""

        service = self.service
        request = service.reports().get(reportId=reportfile_id)

        response=request.execute()

        # craft the filename
        file_name = 'sa360' \
                    + '_' \
                    + name \
                    + '_' \
                    + 'fragment-' \
                    + report_fragment \
                    + '_' \
                    + response['id'] \
                    + '_' \
                    + response['request']['timeRange']['startDate'] \
                    + '_' \
                    + response['request']['timeRange']['endDate'] \
                    + '.' \
                    + response['request']['downloadFormat']

        return file_name


    def generate_filename_path(self, file_name):
        """Generates a report file name and path based on the file metadata."""

        path = os.getcwd()
        filename_path = path + '/' + file_name

        return filename_path


    def download_files(self, name, reportfile_id, report_fragment, filename_path):
        """Generate and print sample report.

        Args:
          service: An authorized Doubleclicksearch service.
          report_id: The ID DS has assigned to a report.
          report_fragment: The 0-based index of the file fragment from the files array.
        """
        service = self.service
        request = service.reports().getFile(
            reportId=reportfile_id,
            reportFragment=report_fragment)

        f=open(filename_path, 'w')
        f.write(request.execute())
        f.close()

        return print(f'file fragment {report_fragment} has been downloaded and written to {filename_path}')


    def poll_download_file(self, name, reportfile_id):
        service = self.service

        for _ in range(10):
            try:
                request = service.reports().get(reportId=reportfile_id)
                response = request.execute()
                if response['isReportReady']:
                    print('The report is ready.')

                    # For large reports, DS automatically fragments the report into multiple
                    # files. The 'files' property in the JSON object that DS returns contains
                    # the list of URLs for file fragment. To download a report, DS needs to
                    # know the report ID and the index of a file fragment.
                    for i in range(len(response['files'])):
                        print('Downloading fragment ' + str(i) + ' for report ' + reportfile_id)
                        file_name = self.generate_filename(name=name,
                                                           reportfile_id=reportfile_id,
                                                           report_fragment=str(i))
                        filename_path = self.generate_filename_path(file_name)

                        self.filenamepathdict.update({file_name:filename_path})

                        self.download_files(name=name,
                                            reportfile_id=reportfile_id,
                                            report_fragment=str(i),
                                            filename_path=filename_path)

                    return print(f'all files downloaded')

                else:
                    retrytime=60
                    print(f'Report is not ready. I will try again in {retrytime}s.')
                    for i in range(retrytime, 0, -1):
                        sys.stdout.write(str(i) + ' ')
                        sys.stdout.flush()
                        time.sleep(1)
                    time.sleep(retrytime)

            except HttpError as e:
                error = json.loads(e.content)['error']['errors'][0]

                # See Response Codes
                print('HTTP code %d, reason %s' % (e.resp.status, error['reason']))
                break


    def download_files(self, name, reportfile_id, report_fragment, filename_path):
        """Generate and print sample report.

        Args:
          service: An authorized Doubleclicksearch service.
          report_id: The ID DS has assigned to a report.
          report_fragment: The 0-based index of the file fragment from the files array.
        """
        service = self.service
        request = service.reports().getFile(
            reportId=reportfile_id,
            reportFragment=report_fragment)
        response=request.execute()

        f=open(filename_path, 'wb')
        f.write(response)
        f.close()