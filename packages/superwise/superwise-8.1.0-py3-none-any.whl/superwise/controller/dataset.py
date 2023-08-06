""" This module implement dataset functionality  """
import os
import time
import urllib.parse
import uuid
from typing import List
from typing import Union

from timeout_decorator import timeout

from superwise.controller.base import BaseController
from superwise.models.dataset import Dataset
from superwise.resources.superwise_enums import DatasetOnFailureOptions
from superwise.resources.superwise_enums import DatasetStatus
from superwise.utils.exceptions import SuperwiseDatasetFailureError
from superwise.utils.exceptions import SuperwiseTimeoutError
from superwise.utils.storage.azure import AzureClientReader
from superwise.utils.storage.gcs import GcsClient
from superwise.utils.storage.local import load_from_local_storage
from superwise.utils.storage.s3 import S3Client


class DatasetController(BaseController):
    """ Datasets controller class, implement functionalities for dataset API """

    def __init__(self, client, sw, internal_bucket):
        """

        ### Args:

        `client`: superwise client object

        `sw`: superwise object

        """
        super().__init__(client, sw)
        self.path = "model/v1/datasets"
        self.model_name = "Dataset"
        self._internal_bucket = internal_bucket
        self._scheme_to_func = {
            "gs": self._get_file_from_gcs,
            "s3": self._get_file_from_s3,
            "abfs": self._get_file_from_blob_storage,
        }

    @staticmethod
    def _get_file_from_gcs(file_path, service_account, validate_size, **kwargs):
        gcs = GcsClient()
        return gcs.get_file_from_gcs(file_path=file_path, service_account=service_account, validate_size=validate_size)

    @staticmethod
    def _get_file_from_s3(file_path, access_key_id, secret_access_key, role_arn, validate_size, **kwargs):
        s3_client = S3Client()
        filename, body = s3_client.get_s3_file(
            file_path=file_path,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            role_arn=role_arn,
            validate_size=validate_size,
        )
        data = body.read()
        return filename, data

    @staticmethod
    def _get_file_from_blob_storage(file_path, connection_string, validate_size, **kwargs):
        azure_client = AzureClientReader(connection_string=connection_string)
        data = azure_client.get_file_from_blob_storage(file_path=file_path, validate_size=validate_size)
        filename = file_path

        return filename, data

    def _upload_files_to_storage(
        self,
        file_paths: Union[str, List[str]],
        project_id: int,
        gcs_service_account: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_role_arn: str = None,
        azure_connection_string: str = None,
    ):
        auth_params = dict(
            service_account=gcs_service_account,
            access_key_id=aws_access_key_id,
            secret_access_key=aws_secret_access_key,
            role_arn=aws_role_arn,
            connection_string=azure_connection_string,
        )
        for file_path in file_paths:
            external_path = file_path
            parsed_url = urllib.parse.urlparse(file_path)
            storage_scheme = parsed_url.scheme

            if storage_scheme in self._scheme_to_func:
                get_file_func = self._scheme_to_func[storage_scheme]
                filename, data = get_file_func(file_path, validate_size=True, **auth_params)
            else:
                filename, data = load_from_local_storage(file_path, validate_size=True)
                external_path = f"file://{filename}"

            base_name, extension = os.path.splitext(filename)
            file_name = self._internal_bucket.generate_file_name(prefix=base_name, extension=extension)
            blob_path = f"datasets/project_id={project_id}/{file_name}"
            inner_path = self._internal_bucket.upload(blob_path=blob_path, content=data)
            yield inner_path, external_path

    @staticmethod
    def _extract_inner_paths(file_paths: List[tuple]) -> List[str]:
        return [file_path[0] for file_path in file_paths]

    @staticmethod
    def _extract_external_paths(file_paths: List[tuple]) -> List[str]:
        return [file_path[1] for file_path in file_paths]

    def get_field(self, dataset_id, field):
        dataset = self.get_by_id(idx=dataset_id)

        return getattr(dataset, field)

    def _get_timeout_func(self, dataset_id, dataset_statuses: List[DatasetStatus], timeout_seconds=30):
        @timeout(
            seconds=timeout_seconds,
            timeout_exception=SuperwiseTimeoutError,
            exception_message=f"Timed out while waiting for dataset with ID: '{dataset_id}' to be in one of "
            f"the statuses {[s.value for s in dataset_statuses]}, "
            f"got status: '{self.get_field(dataset_id, 'status')}', "
            f"with reason: '{self.get_field(dataset_id, 'status_reason') or '<unknown reason>'}'",
        )
        def __wait_to_status():
            dataset = self.get_by_id(dataset_id)
            status = dataset.status

            while status not in [dataset_status.value for dataset_status in dataset_statuses]:
                dataset = self.get_by_id(dataset_id)
                status = dataset.status
                time.sleep(7)

            return dataset

        return __wait_to_status

    def _trigger_full_flow(
        self,
        model: Dataset,
        return_model: bool,
        wait_until_complete: bool,
        timeout_seconds: int,
        on_failure: str,
        **kwargs,
    ):
        model.full_flow = True
        response = BaseController.create(self, model, return_model, **kwargs)
        response_id = response.id if return_model else response["id"]

        if not wait_until_complete:
            return response

        wait_to_status = self._get_timeout_func(
            timeout_seconds=timeout_seconds,
            dataset_id=response_id,
            dataset_statuses=[DatasetStatus.SUMMARIZED, DatasetStatus.FAILED],
        )
        try:
            self.logger.info("Waiting for the dataset to be completely processed...")
            dataset = wait_to_status()
        except SuperwiseTimeoutError:
            if on_failure == DatasetOnFailureOptions.RAISE:
                raise
            return response
        if dataset.status == DatasetStatus.FAILED.value and on_failure == DatasetOnFailureOptions.RAISE:
            raise SuperwiseDatasetFailureError(
                f"Dataset creation failed for ID '{response_id}'. "
                f"got status: '{self.get_field(response_id, 'status')}', "
                f"with reason: '{self.get_field(response_id, 'status_reason') or '<unknown reason>'}'"
            )

        return dataset

    def create(
        self,
        model: Dataset,
        return_model=True,
        gcs_service_account: dict = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_role_arn: str = None,
        azure_connection_string: str = None,
        wait_until_complete: bool = True,
        timeout_seconds: int = 60 * 5,
        on_failure="raise",
        **kwargs,
    ):
        """
        ### Description:

        Create a new dataset.

        ### Args:

        `model`: Dataset model.

        `return_model`: return model if True or response.body if False. Default True.

        `gcs_service_account`: GCP service account object used to authenticate and pull dataset files from a customer
                               GCS bucket. If not provided, will be inferred from the environment.
                               (See Google Cloud auth)

        `aws_access_key_id`: AWS access key ID used to authenticate and pull dataset files from a customer S3 bucket.
                             If not provided, will be inferred from the environment.
                             (Used together with `aws_secret_access_key` parameter)

        `aws_secret_access_key`: AWS secret access key used to authenticate and pull dataset files from a customer S3
                                 bucket. If not provided, will be inferred from the environment.
                                 (Used together with `aws_access_key_id` parameter)

        `aws_role_arn`: AWS role ARN used to authenticate and pull dataset files from a customer S3 bucket.
                        If not provided, the authentication will use the `aws_access_key_id` and `aws_secret_access_key`
                        parameters.

        `azure_connection_string`: Azure blob storage connection string used to authenticate and pull dataset files from
                                   a customer blob storage container.
                                   MUST be provided in order to pull files from azure.

        `wait_until_complete`: if True, wait until the dataset is fully processed in the system, and return the final
                               object. If False, return immediately after the dataset is created and the given dataset
                               files are validated, without waiting for the processing. A partially set Dataset object
                               is returned, without all the processed fields. Afterwards the status can be checked with
                               'get_by_id' method. Default True.

        `timeout_seconds`: Timeout for dataset processing waiting. Only relevant if 'wait_until_complete' is True.
                           Default 30.

        `on_failure`: Action to take in case the dataset processing failed. Only relevant if 'wait_until_complete'
                      is True. Possible values are:
                      - 'ignore': Don't raise an exception, and returned the object.
                      - 'raise': Raise a 'SuperwiseDatasetFailureError' exception.
                      Default 'raise'.
        """
        if not isinstance(model.files, list):
            model.files = [model.files]
        on_failure = DatasetOnFailureOptions(on_failure)

        self.logger.info("Uploading dataset files...")
        file_paths = list(
            self._upload_files_to_storage(
                file_paths=model.files,
                project_id=model.project_id,
                gcs_service_account=gcs_service_account,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_role_arn=aws_role_arn,
                azure_connection_string=azure_connection_string
            )
        )
        model.internal_files = self._extract_inner_paths(file_paths)
        model.files = self._extract_external_paths(file_paths)

        self.logger.info("Finished uploading, start processing dataset...")
        return self._trigger_full_flow(model, return_model, wait_until_complete, timeout_seconds, on_failure, **kwargs)
