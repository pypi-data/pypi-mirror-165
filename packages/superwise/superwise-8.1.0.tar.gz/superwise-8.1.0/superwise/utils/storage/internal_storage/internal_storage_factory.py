from superwise.utils.client import Client
from superwise.utils.storage.internal_storage.aws import AWSInternalStorage
from superwise.utils.storage.internal_storage.azure import AzureInternalStorage
from superwise.utils.storage.internal_storage.gcs import GCSInternalStorage
from superwise.utils.storage.internal_storage.internal_storage import CloudProvider
from superwise.utils.storage.internal_storage.internal_storage import InternalStorage


class InternalStorageFactory:
    @staticmethod
    def get_internal_bucket(superwise_web_client: Client, settings: dict) -> InternalStorage:
        cloud_provider = settings.get('cloud_provider')
        if cloud_provider == CloudProvider.AZURE.value:
            return AzureInternalStorage(superwise_web_client,
                                        settings.get('azure_account_name'),
                                        settings.get('azure_container_name'))
        if cloud_provider == CloudProvider.GCP.value:
            return GCSInternalStorage(superwise_web_client,
                                      settings.get('gcs_bucket_name'))
        if cloud_provider == CloudProvider.AWS.value:
            return AWSInternalStorage(superwise_web_client,
                                      settings.get('s3_bucket_name'))
        else:
            raise ValueError(f"cloud provider {cloud_provider} isn't recognized")
