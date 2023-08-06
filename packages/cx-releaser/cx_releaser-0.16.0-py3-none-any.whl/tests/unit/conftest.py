import datetime
import os

import boto3
import botocore
import pytest
from dateutil.tz import tzlocal
from mock import patch

from cx_releaser.src.docker_registry import AwsRegistry

orig = botocore.client.BaseClient._make_api_call


class MockImage:
    '''A fake Docker API container object.'''

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def tag(self, *args, **kwargs):
        return '{Taged successfully}'


class MockImagesApi:
    '''A fake Docker API with containers calls.'''

    def get(self, *args, **kwargs):
        return MockImage(*args, **kwargs)

    def push(self, *args, **kwargs):
        return '{Pushed Successfully}'


class MockDockerApi:
    '''A fake Docker API.'''

    def __init__(self):
        self.images = MockImagesApi()


def mock_make_api_call(self, operation_name, kwarg):
    if operation_name == 'DescribeImages':
        parsed_response = {'imageDetails': [

            {'registryId': '131413450532', 'repositoryName': 'managed_insights_flows',
             'imageDigest': 'sha256:2c39806f742d472842b544cdb73ec33613c9c197729e5bc95ff492b92416b3f8',
             'imageTags': ['1.0.0', 'latest'], 'imageSizeInBytes': 358693412,
             'imagePushedAt': datetime.datetime(2022, 3, 17, 19, 14, 46,
                                                tzinfo=tzlocal()),
             'imageManifestMediaType': 'application/vnd.docker.distribution.manifest.v2+json',
             'artifactMediaType': 'application/vnd.docker.container.image.v1+json'},
            {'registryId': '131413450532', 'repositoryName': 'managed_insights_flows',
             'imageDigest': 'sha256:8f5f8220a116fb39ad87f6d46fde0f1626f6aaa1b4a495c6a8e6870ecbca99b9',
             'imageTags': ['0.9.0'], 'imageSizeInBytes': 359329906,
             'imagePushedAt': datetime.datetime(2022, 3, 12, 14, 54, 58,
                                                tzinfo=tzlocal()),
             'imageManifestMediaType': 'application/vnd.docker.distribution.manifest.v2+json',
             'artifactMediaType': 'application/vnd.docker.container.image.v1+json'}],
            'ResponseMetadata': {'RequestId': '2e58da7f-df14-4581-807b-ae1325619414',
                                 'HTTPStatusCode': 200, 'HTTPHeaders': {
                    'x-amzn-requestid': '2e58da7f-df14-4581-807b-ae1325619414',
                    'date': 'Tue, 29 Mar 2022 18:14:16 GMT',
                    'content-type': 'application/x-amz-json-1.1', 'content-length': '3135'},
                                 'RetryAttempts': 0}}
        return parsed_response

    if operation_name == 'BatchGetImage':
        return {'images': [{'imageId': '0.9.0'}]}

    if operation_name == 'GetAuthorizationToken':
        return 'OK'
    if operation_name == 'BatchDeleteImage':
        return {'Deleted': 'ok'}
    if operation_name == 'CreateRepository':
        return {'Created': True}
    return orig(self, operation_name, kwarg)


@pytest.fixture(scope='class')
def boto_client():
    with patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call):
        os.environ['AWS_ACCESS_KEY_ID'] = 'a'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'b'
        client = boto3.client('ecr', region_name='us-east-1')
        yield client


@pytest.fixture(scope='class')
def example_aws_registry(boto_client):
    docker_client = MockDockerApi()
    with patch('cx_releaser.src.docker_registry.AwsRegistry._login', return_value='Logged In'):
        obj = AwsRegistry(boto_client, docker_client)
        obj.registry_name = '131413450532'
        obj.auth_config = {'username': 'A', 'password': 'b'}
        yield obj


@pytest.fixture(scope='class')
def example_release_name():
    return 'managed_insights_flows'
