import os
from azure.storage.blob import *

connect_str = 'DefaultEndpointsProtocol=https;AccountName=harvestyourlife;AccountKey=JQVDdkJJ4nYuswBksaHiKxBm2u+Lie4K4iAzIMxMSH5BLN5vkYiJlUDakyiV/JDqjNwfzm5BzUzm0Uz4jC1rMg==;EndpointSuffix=core.windows.net'

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

#Folder to download blob
local_path = "./data"
download_file_path = os.path.join(local_path, 'DOWNLOAD.pdf')

#Get existed container
container_name = "demoazure1"
container_client = blob_service_client.get_container_client(container=container_name)

# List the blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)

# Get data from blob
blob_client = blob_service_client.get_blob_client(container=container_name, blob='dummy.pdf')

# Download blob
with open(download_file_path, "wb") as download_file:
    download_file.write(blob_client.download_blob().readall())
