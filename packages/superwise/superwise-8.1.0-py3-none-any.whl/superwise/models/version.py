""" This module implement version  model  """
import pandas as pd

from superwise.models.base import BaseModel


class Version(BaseModel):
    """ Version model class, model  for version data """

    def __init__(
        self,
        id=None,
        model_id=None,
        name=None,
        created_at=None,
        data_entities=None,
        baseline_df=None,
        status=None,
        dataset_id=None,
        **kwargs
    ):
        """
        ### Description:

        Constructor for Version class

        ### Args:

        `id`: id of Version

        `model_id`: id of model (model))

        `name`: name of version

        `created_at`:

        `data_entities`: list of DataEntity (List[DataEntity])

        `baseline_df`: pandas df of basline data

        `status`:

        `dataset_id`: Dataset to connect to this version
        """
        self.id = id
        self.model_id = model_id
        self.dataset_id = dataset_id
        self.name = name
        self.baseline_files = []
        self.created_at = created_at
        self.data_entities = data_entities or []
        self.status = status
        self.baseline_df = baseline_df
