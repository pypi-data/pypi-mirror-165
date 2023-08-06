import os
import gzip
import shutil

class File:
    def __init__(self):
        pass

    def remove(self, file):
        try:
            os.remove(file)
            print(f'removed file {file}')
        except OSError:
            print(f'could not remove file {file}')

    def convert_to_gzip(self, source_file, dest_file):
        with open(source_file, 'rb') as file_in:
            with gzip.open(dest_file, 'wb') as file_out:
                shutil.copyfileobj(file_in, file_out)