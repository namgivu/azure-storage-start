import os
from azure.storage.blob import BlobServiceClient
import uuid


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


    def TODOtest02_quickstart(self):
        """
        sample code from quickstart guide
        ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
        ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python#get-the-connection-string
        """
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = f"test_quickstart_{str(uuid.uuid4())}"
        container_name = f"test_quickstart"

        container_client = blob_service_client.create_container(container_name)
        #TODO why we have error  > E azure.core.exceptions.HttpResponseError: The specifed resource name contains invalid characters.
