import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

PWD      = os.path.abspath(__file__ + '/../')
APP_HOME = os.path.abspath(PWD + '/../../')

load_dotenv()  # load the .env for unittest; required in macos

def YmdHMS():
    return datetime.now().strftime('%Y%m%d-%H%M%S')

class Test:
    """
    sample code from quickstart guide
    ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
    ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python#get-the-connection-string
    """

    def test00_AZURE_STORAGE_CONNECTION_STRING(self):
        """
        in .env require AZURE_STORAGE_CONNECTION_STRING
        """
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        assert connect_str is not None


    def test01_open_connection(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        _           = BlobServiceClient.from_connection_string(connect_str)


    def test02_create_container(self):
        connect_str         = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name      = f"test-{YmdHMS()}"
        _                   = blob_service_client.create_container(container_name)

    def test03_upload_dummy_blob(self):
        # open connection
        connect_str         = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # load container
        container_name      = f'test{YmdHMS()}'
        container_client    = blob_service_client.create_container(container_name)

        # blob upload
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f'dummy-blob-{YmdHMS()}')
        with open(f'{PWD}/dummy-blob.pdf', 'rb') as data: blob_client.upload_blob(data)

        # list blob
        print('list blob')
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            assert type(blob.name) == str
            print(f'blob.name={blob.name}')


    def test04_download_dummy_blob(self):
        connect_str         = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = f'test-{YmdHMS()}'
        blob_name      = f'dummy-{YmdHMS()}'

        # upload the blob so as to download it later
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(f'{PWD}/dummy-blob.pdf', 'rb') as f_upload: blob_client.upload_blob(f_upload)

        # download it
        with open(f'{APP_HOME}/data/{blob_name}.pdf', 'wb') as f_download:
            f_download.write(blob_client.download_blob().readall())


    def test05_delete_container(self):
        connect_str         = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = f"test-{YmdHMS()}"

        container_client = blob_service_client.create_container(container_name)

        blob_service_client.delete_container(container_name)

    def test06_upload_to_existed_container(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = "demo-upload-container"
        container_client = blob_service_client.get_container_client(container=container_name)

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f'dummy-blob-{YmdHMS()}')
        with open(f'{PWD}/dummy-blob.pdf', 'rb') as data:
            blob_client.upload_blob(data)

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            assert type(blob.name) == str
