import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

PWD      = os.path.abspath(__file__ + '/../')
APP_HOME = os.path.abspath(PWD + '/../../')

load_dotenv()  # load the .env for unittest; required in macos

def YmdHMSf():
    return datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    #                                             millisecond ref. https://stackoverflow.com/a/18406412/248616

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


    #region container crud

    def test02a_create_container(self):
        connect_str         = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name      = f"test-{YmdHMSf()}"
        _                   = blob_service_client.create_container(container_name)


    def test02b_delete_container(self):
        connect_str         = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # prepare container to delete ie create it first to delete later
        container_name = f"test-{YmdHMSf()}"; _ = blob_service_client.create_container(container_name)

        # delete container
        blob_service_client.delete_container(container_name)


    def test_container_exists(self):
        connect_str         = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        cc = blob_service_client.get_container_client(container='some-container-for-testing')  # cc aka container_client
        try   : _ = cc.get_container_properties(); c_exist = True  # c_xxx aka container_xxx
        except: c_exist = False

        assert c_exist is True
    #endregion container crud


    #region blob crud

    def test03_upload_dummy_blob(self):
        # open connection
        connect_str         = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # load container
        container_name      = f'test{YmdHMSf()}'
        container_client    = blob_service_client.create_container(container_name)

        # blob upload
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f'dummy-blob-{YmdHMSf()}')
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

        container_name = f'test-{YmdHMSf()}'  ; _ = blob_service_client.create_container(container_name)  # prepare the container
        blob_name      = f'dummy-{YmdHMSf()}'

        # upload the blob so as to download it later
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(f'{PWD}/dummy-blob.pdf', 'rb') as f_upload:
            blob_client.upload_blob(f_upload)

        # download it
        with open(f'{APP_HOME}/data/{blob_name}.pdf', 'wb') as f_download:
            f_download.write(blob_client.download_blob().readall())


    def test06_upload_to_existing_container(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # check container exists
        container_name = 'some-container-for-testing'
        containers = blob_service_client.list_containers()
        assert container_name in [ c.name for c in containers ]

        # upload to it
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f'dummy-blob-{YmdHMSf()}')
        with open(f'{PWD}/dummy-blob.pdf', 'rb') as f: blob_client.upload_blob(f)

        # aftermath list the blobs in the container
        container_client = blob_service_client.get_container_client(container=container_name)
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            assert type(blob.name) == str


    def test07_cleanup_container(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        containers_list = blob_service_client.list_containers()
        for container in containers_list:
            if container.name.startswith('test'):  # container name as testXXX
                blob_service_client.delete_container(container.name)

    #endregion blob crud
