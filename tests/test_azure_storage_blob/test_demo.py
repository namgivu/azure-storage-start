import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
path = os.path.abspath(__file__ + '/../')
root = os.path.abspath(__file__ + '/../../../')

load_dotenv()
class Test:
    def test00__AZURE_STORAGE_CONNECTION_STRING(self):
        """
        in .env require AZURE_STORAGE_CONNECTION_STRING
        """
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        assert connect_str is not None

    def test01__open_connection(self):
        """
        sample code from quickstart guide
        ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
        ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python#get-the-connection-string
        """
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)


    def test02_create_container(self):
        """
        sample code from quickstart guide
        ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
        ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python#get-the-connection-string
        """
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        container_client = blob_service_client.create_container(container_name)

    def test03_upload_dummy_pdf(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = f"test{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        container_client = blob_service_client.create_container(container_name)

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"dummy-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        with open(f'{path}/dummy.pdf', "rb") as data:
            blob_client.upload_blob(data)

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            assert type(blob.name) == str

    def test04_download_dummy_pdf(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        container_client = blob_service_client.create_container(container_name)

        blob_name = f"dummy-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(f'{path}/dummy.pdf', "rb") as data:
            blob_client.upload_blob(data)

        with open(f'{root}/data/{blob_name}.pdf', "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    def test05_delete_container(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        container_client = blob_service_client.create_container(container_name)

        blob_service_client.delete_container(container_name)

    def test06_upload_to_existed_container(self):
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = "demo-upload-container"
        container_client = blob_service_client.get_container_client(container=container_name)

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"dummy-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        with open(f'{path}/dummy.pdf', "rb") as data:
            blob_client.upload_blob(data)

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            assert type(blob.name) == str
