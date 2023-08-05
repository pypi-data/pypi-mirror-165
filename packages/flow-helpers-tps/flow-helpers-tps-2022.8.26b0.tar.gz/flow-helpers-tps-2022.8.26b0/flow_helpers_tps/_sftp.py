import pysftp
import os

class Sftp:
    """
    basic functions for interfacing with sftp
    see pysftp documentation here: https://pysftp.readthedocs.io/en/release_0.2.8/pysftp.html
    recommended to have ssh keys somewhere for added security beyond login credentials
    note that this version does not use context statement, so connection will NOT auto close)
    if using SSH, provide a filepath to the SSH key (which should be in OpenSSH format)
    """
    def __init__(self,host, username, password=None, hostkeys=None, sshkey=None, sshkeypassword=None):
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = hostkeys
        self.connection = pysftp.Connection(host=host,
                                         username=username,
                                         password=password,
                                         cnopts=self.cnopts,
                                         private_key=sshkey,
                                         private_key_pass=sshkeypassword
                                         )

    def close(self):
        self.connection.close()

    def post_file(self, filename, local_path, remote_path):

        if local_path.endswith('/'):
            localfilenamepath = local_path + filename
        else:
            localfilenamepath = local_path + '/' + filename

        if remote_path.endswith('/'):
            remote_path = remote_path + filename
        else:
            remote_path = remote_path + '/' + filename

        sftp = self.connection
        print(f'sftp connected, posting {filename} to {remote_path}')
        sftp.put(localfilenamepath, remote_path, callback=None, confirm=False)
        print(f'file posted')

    def list_file(self, remote_path):
        if remote_path.endswith('/'):
            remote_path = remote_path
        else:
            remote_path = remote_path + '/'

        sftp = self.connection
        print(f'sftp connected, list files in {remote_path}')
        sftp.cwd(remote_path)
        directory_structure = sftp.listdir()

        return print(directory_structure)

    def list_filemodifieddict(self, remote_path):
        """create a dict of filenames + their modified times in UNIX epoch format"""

        if remote_path.endswith('/'):
            remote_path = remote_path
        else:
            remote_path = remote_path + '/'

        filedict = {}
        sftp = self.connection
        print(f'sftp connected, list files in {remote_path}')
        sftp.cwd(remote_path)
        directory_structure = sftp.listdir_attr()

        for attr in directory_structure:
            filedict[attr.filename] = attr.st_mtime

        return filedict

    def get_file(self, filename, remote_path, local_path=None):
        if local_path is not None and local_path.endswith('/'):
            localfilepathname = local_path + filename
        elif local_path is not None:
            localfilepathname = local_path + '/' + filename
        else:
            localfilepathname = os.getcwd() + '/' + filename

        if remote_path.endswith('/'):
            remotefilepathname = remote_path + filename
        else:
            remotefilepathname = remote_path + '/' + filename

        sftp = self.connection
        print(f'sftp connected, get {filename} from {remote_path}')
        sftp.get(remotepath=remotefilepathname, localpath=localfilepathname, preserve_mtime=True)
        print(f'file retrieved')

    def remove(self, filename, remote_path):
        if remote_path.endswith('/'):
            remotefilepathname = remote_path + filename
        else:
            remotefilepathname = remote_path + '/' + filename

        sftp = self.connection
        print(f'sftp connected, get {filename} from {remote_path}')
        sftp.remove(remotefile=remotefilepathname)
        print(f'file removed')

    def list_lastmodifiedfile(self, remote_path, neg_identifier=None, pos_identifier=None):
        filedict = self.list_filemodifieddict(remote_path)

        if neg_identifier is not None and pos_identifier is not None:
            list_mtime = [mtime for file, mtime in filedict.items() if neg_identifier not in file if pos_identifier in file]
        elif neg_identifier is not None:
            list_mtime = [mtime for file, mtime in filedict.items() if neg_identifier not in file]
        elif pos_identifier is not None:
            list_mtime = [mtime for file, mtime in filedict.items() if pos_identifier in file]
        else:
            list_mtime = [mtime for file, mtime in filedict.items()]

        for file, mtime in filedict.items():
            if mtime == max(list_mtime):
                return file

    def list_files(self, remote_path, neg_identifier=None, pos_identifier=None):
        filedict = self.list_filemodifieddict(remote_path)

        if neg_identifier is not None and pos_identifier is not None:
            list_file = [file for file, mtime in filedict.items() if neg_identifier not in file if pos_identifier in file]
        elif neg_identifier is not None:
            list_file = [file for file, mtime in filedict.items() if neg_identifier not in file]
        elif pos_identifier is not None:
            list_file = [file for file ,mtime in filedict.items() if pos_identifier in file]
        else:
            list_file = [file for file, mtime in filedict.items()]

        return list_file

    def rename_file(self, original_remote_path, original_filename, new_filename, new_remote_path=None):
        if original_remote_path.endswith('/'):
            original_remote_path = original_remote_path
        else:
            original_remote_path = original_remote_path + '/'

        if new_remote_path is not None and new_remote_path.endswith('/'):
            new_remote_path = new_remote_path
        elif new_remote_path is not None:
            new_remote_path = new_remote_path + '/'
        elif new_remote_path is None:
            new_remote_path = original_remote_path

        originalfilepathname = original_remote_path + original_filename
        newfilepathname = new_remote_path + new_filename

        sftp = self.connection
        sftp.rename(originalfilepathname, newfilepathname)
        print(f'file renamed from {originalfilepathname} to {newfilepathname}')



# # testing
# from prefect.client import Secret
# hostname = Secret('journera_sftp_server').get()
# username = str(Secret('journera_sftp_user').get())
# pwd = Secret('sfmc_pwd').get()

# test = Sftp(host=hostname,
#             username=username,
#             password=None,
#             hostkeys = None,
#             sshkey = '/home/prefect/.prefect/TPS Journera SFTP Private Key - OpenSSH.ppk')

# file2 = test.list_filemodifieddict(remote_path='./from tps/')
# print(file2)
