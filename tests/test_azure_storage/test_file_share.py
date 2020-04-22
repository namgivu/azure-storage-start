from azure.storage.fileshare import ShareServiceClient, ShareDirectoryClient, ShareFileClient
import os

PWD = os.path.abspath(__file__ + '/../')

EXISTING_SHARE_NAME = 'receivefromharvest'
EXISTING_FOLDER     = 'archive'

class Test:

    def test_connection(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        _ = ShareServiceClient.from_connection_string(conn_str=connect_str)


    def test_list_file(self):
        connect_str   = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        folder_client = ShareDirectoryClient.from_connection_string(conn_str=connect_str, share_name=EXISTING_SHARE_NAME, directory_path='')

        f_all = list(folder_client.list_directories_and_files())
        for f in f_all:
            assert isinstance(f, dict)
            k='name'         ; v=f.get(k); assert v is not None; assert isinstance(v, str)
            k='is_directory' ; v=f.get(k); assert v is not None; assert isinstance(v, bool)

        print(f'\n{f_all}')


    def test_upload_download_delete_file(self):  #TODO what if destination folder not pre-exist, will it create on the fly?
        connect_str   = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        folder_client = ShareDirectoryClient.from_connection_string(conn_str=connect_str, share_name=EXISTING_SHARE_NAME, directory_path='')

        dummy_filename = 'dummy-file'
        dummy_f        = f'{PWD}/{dummy_filename}'

        # ensure CANNOT list sample file :dummy_f in :EXISTING_FOLDER
        f_all = list(folder_client.list_directories_and_files(name_starts_with=dummy_filename))
        assert len(f_all) == 0

        # upload a sample file :dummy_f to EXISTING_SHARE_NAME  #CAUTION: re-upload will overwrite current file if any
        file_client = ShareFileClient.from_connection_string(conn_str=connect_str, share_name=EXISTING_SHARE_NAME, file_path=f'{dummy_filename}')
        with open(dummy_f, 'rb') as uf: file_client.upload_file(uf)  # uf aka upload_file

        # ensure can list sample file :dummy_f in :EXISTING_FOLDER
        f_all = list(folder_client.list_directories_and_files(name_starts_with=dummy_filename))
        assert len(f_all) == 1

        # clean up :dummy_f
        file_client.delete_file()
