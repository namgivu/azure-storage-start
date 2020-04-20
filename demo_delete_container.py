from azure.storage.blob import *

connect_str = 'DefaultEndpointsProtocol=https;AccountName=harvestyourlife;AccountKey=JQVDdkJJ4nYuswBksaHiKxBm2u+Lie4K4iAzIMxMSH5BLN5vkYiJlUDakyiV/JDqjNwfzm5BzUzm0Uz4jC1rMg==;EndpointSuffix=core.windows.net'

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create a unique name for the container
container_name = "demoazure1"

#Delete container
blob_service_client.delete_container(container_name)
