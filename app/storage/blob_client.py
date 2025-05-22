from azure.storage.blob import BlobServiceClient

class AzureBlobService:
    def __init__(self, connection_string: str, container_name: str):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload_df_to_blob(self, df, blob_path: str):
        filename = blob_path + '.csv'
        self.container_client.upload_blob(name=filename, data=df, overwrite=True)
