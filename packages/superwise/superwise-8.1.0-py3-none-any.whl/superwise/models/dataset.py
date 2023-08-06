""" This module implement Dataset model  """
from typing import Dict
from typing import List
from typing import Union

from superwise.models.base import BaseModel
from superwise.resources.superwise_enums import DatasetStatus
from superwise.resources.superwise_enums import DatasetType


class Dataset(BaseModel):
    """DataSet"""

    def __init__(
        self,
        name: str,
        files: Union[str, List[str]],
        project_id: int,
        type: Union[DatasetType, str] = DatasetType.TRAIN,
        dtypes: Dict[str, str] = None,
        roles: Dict[str, str] = None,
        **kwargs
    ):
        """
        ### Description:

        Constructor for Dataset class

        ### Args:

        `name`: The name of the dataset.

        `files`: The raw data of the dataset. Can be provided as local or cloud file paths. (GCS or S3)

        `project_id`: The ID of the project which this dataset will be assigned to.

        `type`: The type of the dataset (See 'superwise.resources.superwise_enums.DatasetType' enum). Default 'TRAIN'.

        `dtypes`: An optional mapping between columns and their dtypes.
                  if not provided, will be inferred.

        `roles`: An optional mapping between columns and their roles.
                 If not provided, will be inferred.
        """
        BaseModel.__init__(self, **kwargs)
        self.project_id = project_id
        self.name = name
        self.type = type.value if isinstance(type, DatasetType) else type
        self.dtypes = dtypes
        self.roles = roles
        self.files = files
        self.matching_entities = kwargs.get("matching_entities")
        self.internal_files = kwargs.get("internal_files")
        self.created_at = kwargs.get("created_at")
        self.created_by = kwargs.get("created_by")
        self.num_rows = kwargs.get("num_rows")
        self.num_columns = kwargs.get("num_columns")
        self.head = kwargs.get("head")
        self.status = kwargs.get("status", DatasetStatus.UNKNOWN.value)
        self.status_reason = kwargs.get("status_reason")
        self.is_static = kwargs.get("is_static", True)
