import base64
import datetime
import re
from collections import defaultdict
from subprocess import PIPE, Popen

import boto3
import docker


class AwsRegistry:
    LATEST_TAG = 'latest'
    DELETE_PREFIX_TAG = 'DELETEON_'

    def __init__(self, client_aws=None, client_docker=None):
        self.client_aws = client_aws or boto3.client('ecr', region_name='us-east-1')
        self._login()
        self.client_docker = client_docker or docker.from_env()

    def get_or_create(self, name, tags=None, mutability="MUTABLE", scan_on_push=True, encryption='AES256'):
        try:
            response = self.client_aws.create_repository(
                repositoryName=name,
                tags=[
                    tags or {"Key": 'name', 'Value': name}
                ],
                imageTagMutability=mutability,
                imageScanningConfiguration={
                    'scanOnPush': scan_on_push
                },
                encryptionConfiguration={
                    'encryptionType': encryption,
                }
            )
        except self.client_aws.exceptions.RepositoryAlreadyExistsException:
            response = self.client_aws.describe_images(repositoryName=name)
        return response

    def get_all_image_tags(self, image_name, tag_filter='', with_deleted=False):
        images = self.client_aws.describe_images(repositoryName=image_name)

        results = []
        for image in images['imageDetails']:
            if not 'imageTags' in image:
                continue
            for tag in image['imageTags']:
                content_match = re.match(tag_filter, tag) if not with_deleted else \
                    re.match(tag_filter, tag) or re.match(self.DELETE_PREFIX_TAG + tag_filter, tag)
                if content_match:
                    pushed_at = image['imagePushedAt']
                    results.append({'tag': tag, 'pushed_at': pushed_at, 'image': image})
        results = sorted(results, key=lambda x: x['pushed_at'], reverse=True)
        return results

    def get_images_on_unique_hash(self, image_name='', hash_filter='', images=None):
        images = images or self.get_all_image_tags(image_name)
        hash_dict = defaultdict(list)
        for image in images:
            digest = image['image']['imageDigest']
            if digest.startswith(hash_filter):
                hash_dict[digest] = image
        return hash_dict

    def pull_image(self, image_name, tag=None):
        if tag is None:
            tag = self.get_all_image_tags(image_name)[0]['tag']
        response = self.client_docker.images.pull(self._get_image_url(image_name, tag), stream=True)
        return response

    def delete_image(self, image_name, tag, soft=True):
        dayint = datetime.date.today()
        images = self.get_all_image_tags(image_name, tag_filter='')
        img_tags = {image['tag']: image['image'] for image in images}
        if not img_tags.get(tag):
            print(f'Did not found images with tag {tag}')
            return
        delete_tag = dayint.strftime("%Y-%m-%d")
        delete_tag = '_DELETEON_' + delete_tag
        response = self.client_aws.batch_get_image(
            repositoryName=image_name,
            imageIds=[
                {
                    'imageTag': tag
                }
            ]
        )
        if soft:
            response_delete = self.client_aws.batch_get_image(
                repositoryName=image_name,
                imageIds=[
                    {
                        'imageTag': tag + delete_tag
                    }
                ]
            )
            if not response_delete:
                self.client_aws.put_image(
                    repositoryName=image_name,
                    imageManifest=response['images'][0]['imageManifest'],
                    imageTag=tag + delete_tag
                )

        ids = [image['imageId'] for image in response['images']]
        return self.client_aws.batch_delete_image(repositoryName=image_name, imageIds=ids)

    def push_image(self, image_name, tag, local_name=None, as_latest=False):
        self.tag_image(image_name, tag, local_name, as_latest)
        response = self.client_docker.images.push(self._get_image_url(image_name), tag=tag, stream=True)
        self._process_docker_response(response, raise_=False)
        return response

    def tag_image(self, image_name, tag, local_name=None, as_latest=False):
        image_tag_name = local_name or self._get_image_url(image_name, with_registry=False)
        image = self.client_docker.images.get(image_tag_name)
        if as_latest:
            image.tag(self._get_image_url(image_name), self.LATEST_TAG)
        image.tag(self._get_image_url(image_name), tag)
        return image

    def update_image_tags(self, image_name, tag, new_tags):
        response = self.client_aws.batch_get_image(
            repositoryName=image_name,
            imageIds=[
                {
                    'imageTag': tag
                }
            ]
        )
        for new_tag in new_tags:
            self.client_aws.put_image(
                repositoryName=image_name,
                imageManifest=response['images'][0]['imageManifest'],
                imageTag=new_tag
            )
        return True

    def get_image_hash(self, image_name=None, tag=None, local_name=None):
        if local_name:
            image_tag_name = local_name
        else:
            image_tag_name = self._get_image_url(image_name, tag, with_registry=False)
        image = self.client_docker.images.get(image_tag_name)
        for dig in image.attrs["RepoDigests"]:
            if dig.startswith(self.registry_name):
                return 'sha256:' + dig.split('@sha256:')[-1]
        return None

    def _login(self):
        token = self.client_aws.get_authorization_token()
        username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        registry = token['authorizationData'][0]['proxyEndpoint'].replace("https://", "")
        self.registry_name = registry
        self.auth_config = {'username': username, 'password': password}
        command = f'docker login --username {username} --password {password} {registry}'
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = process.communicate()
        if not b'Login Succeeded' in stdout:
            raise ValueError(f'Could not login to ecr registry. Got: {stderr}')
        return self.auth_config

    def _get_image_url(self, image, tag=None, with_registry=True):
        suffix, prefix = '', ''
        if tag:
            suffix = f':{tag}'
        if with_registry:
            prefix = f'{self.registry_name}/'
        return f'{prefix}{image}{suffix}'

    def _process_docker_response(self, response, raise_=False):
        for resp in response:
            resp = resp.decode() if not isinstance(resp, str) else resp
            err = re.search('.*errorDetails.*', resp)
            if err:
                if raise_:
                    raise ValueError(err.group(0))
                return
            print(resp)
