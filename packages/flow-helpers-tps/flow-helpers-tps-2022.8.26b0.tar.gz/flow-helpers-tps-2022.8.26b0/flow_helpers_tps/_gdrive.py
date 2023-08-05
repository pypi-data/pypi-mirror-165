from __future__ import print_function

import os
from datetime import datetime, timedelta
from io import BytesIO

import numpy as np
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class GDrive:

    # instance vars
    def __init__(self, key):
        self.key = key
        scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]
        credentials = service_account.Credentials.from_service_account_info(self.key, scopes=scopes)
        self.service = build('drive', 'v3', credentials=credentials)

    def get_file_list(self, folder_id, days=None, text=None, recursive=True):

        files = self.service.files().list(q="trashed=false", driveId=folder_id, includeItemsFromAllDrives=True,
                                          corpora='drive', supportsAllDrives=True,
                                          fields='files(id, name, mimeType, modifiedTime, parents)').execute()
        files = files['files']

        if days is not None:
            files = [files[i] for i in range(len(files)) if
                     datetime.strptime(files[i]['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%f%z").replace(
                         tzinfo=None) >= datetime.now() - timedelta(days=days)]

        if text is not None:
            ind = np.where(np.array([text in files[n]['name'] for n in range(0, len(files))]))
            ind = ind[0].tolist()
            files = [files[i] for i in ind]

        if not recursive:
            nested = [folder_id in files[n]['parents'] for n in range(len(files))]
            nested_index = np.where(np.array(nested))[0].tolist()
            files = [files[n] for n in nested_index]

        return files

    def download(self, file_id, sheet_name=0, header=0):
        file = self.service.files().get_media(fileId=file_id).execute()
        file = BytesIO(file)

        try:
            df = pd.read_csv(file)
        except:
            df = pd.read_excel(file, sheet_name=sheet_name, header=header)

        return df

    def upload(self, file_name, folder_id, file_path=None, mime_type='text/csv'):

        body = {'name': file_name, 'mimeType': mime_type, 'parents': [folder_id]}

        if file_path is None:
            file_path = os.path.abspath(file_name)

        media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        create = self.service.files().create(body=body, media_body=media_body, fields='id',
                                             supportsAllDrives=True).execute()

        return create
