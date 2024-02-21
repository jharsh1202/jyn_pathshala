from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.conf import settings

class AzureBlobStorage:
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    container_name = settings.AZURE_ACCOUNT_CONTAINER_NAME
    
    def __init__(self):
        # Create a BlobServiceClient
        blob_service_client = BlobServiceClient(account_url=f"https://{self.account_name}.blob.core.windows.net", credential=self.account_key)

        # Create a container client
        self.container_client = blob_service_client.get_container_client(self.container_name)
            
    def upload_file(self, file_path, file_name):
        # file upload to Azure Blob Storage
        blob_client = self.container_client.get_blob_client(file_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
    
    def download_file(self, file_name):
        # Implement file download from Azure Blob Storage
        pass
