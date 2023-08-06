import requests

from superwise.utils.client import Client
from superwise.utils.exceptions import SuperwiseStorageUploadAWSError
from superwise.utils.storage.internal_storage.internal_storage import InternalStorage


class AWSInternalStorage(InternalStorage):
    def __init__(self, superwise_web_client: Client, bucket_name: str):
        super().__init__(superwise_web_client)
        self._bucket_name = bucket_name

    def _put_in_storage(self, blob_name: str, content: str):
        try:
            url, fields = self._cloud_token['url'], self._cloud_token['fields']
            file = {'file': (blob_name, content)}
            res = requests.post(url, data=fields, files=file)
            res.raise_for_status()
            return f"s3://{self._bucket_name}/{blob_name}"
        except Exception as e:
            raise SuperwiseStorageUploadAWSError(f"error upload file {blob_name} to internal bucket with ext{e}")

    def _is_cloud_token_active(self) -> bool:
        """
        cloud token is enable per file path to every upload a new token should be created
        """
        return False
