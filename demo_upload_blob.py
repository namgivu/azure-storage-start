from azure.storage.blob import *

connect_str = 'DefaultEndpointsProtocol=https;AccountName=harvestyourlife;AccountKey=JQVDdkJJ4nYuswBksaHiKxBm2u+Lie4K4iAzIMxMSH5BLN5vkYiJlUDakyiV/JDqjNwfzm5BzUzm0Uz4jC1rMg==;EndpointSuffix=core.windows.net'

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create a unique name for the container
container_name = "demoazure1"

# Create container
blob_service_client.create_container(container_name)

# Get container
container_client = blob_service_client.get_container_client(container=container_name)

# Upload to blob
blob_client = blob_service_client.get_blob_client(container=container_name, blob='dummy.pdf')
with open('/Users/trangtruong/Desktop/azure-storage-start/tests/test_azure_storage_blob/dummy.pdf', "rb") as data:
    blob_client.upload_blob(data)

# List the blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)

