import boto3
import pytest
import requests
from google.cloud import storage
from google.oauth2 import service_account
from requests import Response

from superwise import Superwise
from superwise.models.segment import Segment
from superwise.models.segment import SegmentCondition
from superwise.models.segment import SegmentConditionDefinition
from superwise.utils.client import Client
from superwise.utils.exceptions import *
from tests import get_sw
from tests import print_results

segment_id = None


def mock_boto_client(monkeypatch):
    class BotoClient:
        def __init__(self, *args, **kwargs):
            pass

        def get_object(self, *args, **kwargs):
            class ObjectResposne:
                def read(self):
                    return "blablabla"

            return dict(Body=ObjectResposne())

    monkeypatch.setattr(boto3, "client", lambda *args, **kwargs: BotoClient())


@pytest.fixture(scope="function")
def mock_gcp_client(monkeypatch):
    class GCSClient:
        def __init__(self, *args, **kwargs):
            self.name = "test"

        def bucket(self, bucket_name):
            return GCSClient()

        def blob(self, file_name):
            return GCSClient()

        def download_as_string(self):
            return "asdasdaas"

        def upload_from_string(self, data):
            return None

    monkeypatch.setattr(service_account.Credentials, "from_service_account_info", lambda *args, **kwargs: "")
    monkeypatch.setattr(storage, "Client", lambda *args, **kwargs: GCSClient())


@pytest.fixture(scope="function")
def mock_get_token(monkeypatch):
    monkeypatch.setattr(
        Client,
        "get_token",
        lambda *args, **kwargs: "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ3ZDdmMDg2In0.eyJzdWIiOiI5YzNlZmUxZC03NGNlLTRlZTItYTMyOC1kMWZmNmQyMDAyM2YiLCJlbWFpbCI6InN3X2JhcmFrQHN1cGVyd2lzZS5haSIsInVzZXJNZXRhZGF0YSI6e30sInRlbmFudElkIjoiYmFyYWsiLCJyb2xlcyI6WyJWaWV3ZXIiXSwicGVybWlzc2lvbnMiOlsiZmUuc2VjdXJlLndyaXRlLnVzZXJBcGlUb2tlbnMiLCJmZS5zZWN1cmUuZGVsZXRlLnVzZXJBcGlUb2tlbnMiLCJmZS5zZWN1cmUucmVhZC51c2VyQXBpVG9rZW5zIl0sIm1ldGFkYXRhIjp7fSwiY3JlYXRlZEJ5VXNlcklkIjoiNDg5ZmM5Y2YtZDlhYy00MWMwLWJmM2ItN2VhNDUyNDY4ODEyIiwidHlwZSI6InVzZXJBcGlUb2tlbiIsInVzZXJJZCI6IjQ4OWZjOWNmLWQ5YWMtNDFjMC1iZjNiLTdlYTQ1MjQ2ODgxMiIsImlhdCI6MTYzNjY0ODIyMywiZXhwIjoxNjM2NzM0NjIzLCJpc3MiOiJmcm9udGVnZyJ9.qhEclIsSpfwXpCTFb8qhKpizRWtpQSnkE7VMsy9Et3guLcOcTiTVZ2wOJPmemtL3g3AStKH2jFSOEwQOoqnvgSR3dum9I_Ae3UwrFNRnM3EqOz7UsD0cJAd1AYy-69-67o5oX9A2U4MPZSA5Dr5Edbvn86-AsBJhADGDs5AyEyuGmlJTq0ACGAmoC8qZlxwnOsn9wIzTiQVU7085M73n5iJ26SNhsy4KNpU-8oR2lC1akDroHzL8aIr5dAWSWZz_cfcyWQyC1gqb4_ZAvG1GXiKwsGW2irFyfGoD9zrwMoMGuWXKCbXnHxIzuv8ImX_cRVPXq5xVBYUXwODr83Q3FA",
    )


@pytest.fixture(scope="function")
def mock_segments_requests(monkeypatch):
    post_response = Response()
    post_response._content = b'{"status": "ACTIVE", "created_at": "2022-08-01 11:39:17", "project_id": 1, "created_by": "auto", "archived_at": null, "id": 7, "definition_json": [[{"value": 23.0, "condition": "==", "entity_id": 4, "entity_name": "age"}]], "name": "hello2"}'
    post_response.status_code = 201
    get_response = Response()
    get_response._content = b'[{"status": "ACTIVE", "created_at": "2022-08-01 11:39:17", "project_id": 1, "created_by": "auto", "archived_at": null, "id": 7, "definition_json": [[{"value": 23.0, "condition": "==", "entity_id": 4, "entity_name": "age"}]], "name": "hello2"}, {"status": "ACTIVE", "created_at": "2022-08-01 11:39:17", "project_id": 1, "created_by": "auto", "archived_at": null, "id": 7, "definition_json": [[{"value": 23.0, "condition": "==", "entity_id": 4, "entity_name": "age"}]], "name": "hello2"}]'
    get_response.status_code = 200
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: post_response)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: get_response)


def test_create_segment_inline(mock_get_token, mock_segments_requests, sw):
    inline_model_test = sw.segment.create(
        Segment(
            project_id=1,
            name="hello2",
            definition=[
                [
                    SegmentConditionDefinition(
                        entity_id=1, condition=SegmentCondition.IN, value=["Israel", "United States of America"]
                    ),
                    SegmentConditionDefinition(entity_id=2, condition=SegmentCondition.GREATER_THAN, value=0.5),
                ]
            ],
        )
    )
    print_results("created segment object 1", inline_model_test.get_properties())
    assert inline_model_test.project_id == 1
    assert inline_model_test.name == "hello2"
    assert inline_model_test.id is not None


def test_get_segment(mock_get_token, mock_segments_requests, sw):
    segments = sw.segment.get({})
    assert len(segments) == 2
    assert int(segments[0].id) == 7
