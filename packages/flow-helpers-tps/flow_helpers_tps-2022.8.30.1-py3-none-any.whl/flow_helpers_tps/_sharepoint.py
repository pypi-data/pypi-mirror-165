from office365.sharepoint.client_context import ClientContext, ClientCredential
from office365.sharepoint.files.file import File
import io
import os
import pandas as pd


class Sharepoint:
    # Purpose: use Office365-REST-Python-Client library to access TPS Sharepoint using app credentials
    #     source: https://github.com/vgrem/Office365-REST-Python-Client

    def __init__(self, site_url, sharepoint_id, sharepoint_secret):
        self.sharepoint_id = sharepoint_id
        self.sharepoint_secret = sharepoint_secret
        self.site_url = site_url
        self.client_credentials = ClientCredential(self.sharepoint_id, self.sharepoint_secret)
        self.ctx = ClientContext(self.site_url).with_credentials(self.client_credentials)

    def list_files(self, folder_url, subfolder, incl_childfolders=False):
        """returns a list of tuples holding filename, id, and serverRelativeUrl for specified folder"""
        # 'folder_url' should equal 'ServerRelativeUrl' as defined by properties for root directory
        # ends with '/'
        # 'subfolder' should equal string name for given subfolder of root directory to reference

        ctx = self.ctx

        libraryRoot = ctx.web.get_folder_by_server_relative_url(os.path.join(folder_url, subfolder))
        ctx.load(libraryRoot)
        ctx.execute_query()

        filefolder_list = []

        if incl_childfolders is True:
            folders = libraryRoot.folders
            ctx.load(folders)
            ctx.execute_query()
            for folder in folders:
                f = (folder.properties['Name'], folder.properties['UniqueId'],folder.properties['ServerRelativeUrl'])
                filefolder_list.append(f)

        files = libraryRoot.files
        ctx.load(files)
        ctx.execute_query()
        for file in files:
            # create tuple of filename, unique ID, server relative url
            # then append into file_list and return it
            f = (file.properties['Name'], file.properties['UniqueId'], file.properties['ServerRelativeUrl'])
            filefolder_list.append(f)

        return filefolder_list

    def get_file_to_df(self, folder_url, subfolder, filename, remove_sheets_list):
        # convert to pandas dataframe all sheets in file 'get_file' saved to specified folder directory
        # any sheet not wanted in dataframe needs to be identified in [remove_sheets_list]
        # 'folder_url' should equal 'ServerRelativeUrl' as defined by properties for root directory
        # ends with '/'
        # 'subfolder' should equal string name for given subfolder of root directory to reference

        ctx = self.ctx

        libraryRoot = ctx.web.get_folder_by_server_relative_url(os.path.join(folder_url, subfolder))

        files = libraryRoot.files
        ctx.load(files)
        ctx.execute_query()

        for file in files:
            if file.properties['Name'] == filename:
                serverrelativeurl = file.properties['ServerRelativeUrl']
                print(serverrelativeurl)

                response = File.open_binary(ctx, serverrelativeurl)
                bytes_file_obj = io.BytesIO()
                bytes_file_obj.write(response.content)
                bytes_file_obj.seek(0)

                if filename[-3:] == 'csv':

                    sheets_dict = pd.read_csv(bytes_file_obj,header=0).T

                else:
                    sheets_dict = pd.read_excel(bytes_file_obj,
                                                sheet_name=None)  # None means all sheets
                                                # this produces a dict of DataFrames with the keys as the sheet names

                # Using pop() + list comprehension
                # Remove multiple keys from dictionary
                [sheets_dict.pop(key) for key in remove_sheets_list]

                df = pd.DataFrame()
                for name, sheet in sheets_dict.items():
                    sheet['sheet'] = name
                    df = df.append(sheet)

                df.reset_index(inplace=True, drop=True)

            else:
                pass

        return df

    def post_file(self, folder_url, subfolder, filenamepath):
        # 'folder_url' should equal 'ServerRelativeUrl' as defined by properties for root directory
        # ends with '/'
        # 'subfolder' should equal string name for given subfolder of root directory to reference

        ctx = self.ctx

        target_folder = ctx.web.get_folder_by_server_relative_url(os.path.join(folder_url, subfolder))

        chunksize = 1000000
        file_size = os.path.getsize(filenamepath)
        print(f'{filenamepath} is {file_size} large, preparing to upload in chunks of {chunksize}')

        uploaded_file = target_folder.files.create_upload_session(source_path=filenamepath, chunk_size=chunksize)
        print('executing upload')
        ctx.execute_query()
        print('File {0} has been uploaded successfully'.format(uploaded_file.serverRelativeUrl))

    def download_file(self, download_directory, serverRelativeUrl=None, folder_url=None, subfolder = None, filename=None):
        # https://github.com/vgrem/Office365-REST-Python-Client/blob/master/examples/sharepoint/files/download_file.py
        """download file as specified by either the direct serverRelativeUrl,
        or specify through combination of folder_url, subfolder, and filename
        """

        if serverRelativeUrl is None and folder_url is None and filename is None:
            return 'need to supply serverRelativeUrl, or folder_url + subfolder  + filename'
        if serverRelativeUrl:
            file_url = serverRelativeUrl
        elif not serverRelativeUrl:
            file_url = os.path.join(folder_url, subfolder, filename)

        ctx = self.ctx

        download_filenamepath = os.path.join(download_directory, os.path.basename(file_url))
        with open(download_filenamepath, "wb") as local_file:
            file = ctx.web.get_file_by_server_relative_url(file_url).download(local_file).execute_query()
        print("[Ok] file has been downloaded: {0}".format(download_filenamepath))
