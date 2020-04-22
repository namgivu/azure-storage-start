from azure.storage.fileshare import ShareServiceClient, ShareDirectoryClient
import os

EXISTING_SHARE_NAME='receivefromharvest'

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
