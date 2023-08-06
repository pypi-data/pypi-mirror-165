import copy
import os.path
import re
import subprocess
import tempfile

import yaml
from semantic_version import Version

from cx_releaser.src.docker_registry import AwsRegistry


class Release:
    version_pattern = Version.partial_version_re

    def __init__(self, registry_client: AwsRegistry, name, version,
                 local_name=None, equal_tags=None,
                 incr_version='minor', on_tag_exist='replace',
                 on_repo_not_exist='create'):
        """
        :param registry_client:  registry client like AwsRegistry client
        :param name: name of image
        :param version: version (tag) of the image
        :param local_name: name of local image
        :param equal_tags: additional tags for the image (beside version)
        :param incr_version: minor, major or patch. Which version we should increment/decrement
        :param on_tag_exist: if raise raise ValueError else replace this tag with new image
        :param on_repo_not_exist: if repo not exist raise or create new one
        """
        self.registry_client = registry_client
        self.name = name
        self.equal_tags = equal_tags or []
        self.version = version
        self.local_name = local_name or f'{self.name}:{self.version}'
        self.incr_version = incr_version
        self.on_tag_exist = on_tag_exist
        self.on_repo_not_exist = on_repo_not_exist
        self.hash = None
        self.pushed_at = None
        self._next = None
        self._prev = None
        if self.on_repo_not_exist == 'create':
            self.registry_client.get_or_create(self.name)

    def get_equal_tags_from_remote(self, hash_filter='', images=None, with_hash=False):
        equal_tags = []
        hashes = self.registry_client.get_images_on_unique_hash(self.name, hash_filter=hash_filter, images=images)
        new_hash = None
        for hash, img in hashes.items():
            tags = img['image']['imageTags']
            if self.version in tags:
                new_hash = hash
                equal_tags.extend(tags)
        if equal_tags:
            equal_tags.remove(self.version)
        if with_hash:
            return equal_tags, hashes.get(new_hash)
        return equal_tags

    def exist_on_remote(self):
        hashes = self.registry_client.get_images_on_unique_hash(self.name, hash_filter='')
        for hash, tags in hashes.items():
            if self.version in tags['image']['imageTags']:
                return True
        return False

    def validate_push(self, images=None, check_is_next=True, check_new_hash=False):
        images = images or self.registry_client.get_all_image_tags(self.name, tag_filter=self.version_pattern)
        if check_is_next:
            self._check_is_next_release(images)
        if check_new_hash:
            self._check_is_different_release()
        self._resolve_conflicting_tags()
        return True

    def validate_rollback(self, prev_release):
        exist = self.exist_on_remote()
        if not exist:
            raise ValueError(f'Release {self.version} does not exist')
        if prev_release and prev_release.version_sem() >= self.version_sem():
            raise ValueError('Provide one of previous releases to rollback. One with smaller version')
        if prev_release and not prev_release.exist_on_remote():
            raise ValueError(f'Release {prev_release.version} does not exist on remote. Could not rollback to it')
        return True

    def update_tags(self, new_tags=None):
        self.registry_client. \
            update_image_tags(self.name, self.version, new_tags or [])
        return True

    def pull(self):
        return self.registry_client.pull_image(self.name, self.version)

    def push(self, validate=True, checks=None, test_tag=None):
        checks = checks or {}
        if test_tag:
            return self.registry_client.push_image(self.name, test_tag, local_name=self.local_name)
        validate and self.validate_push(check_is_next=
                                        'check_is_newest' in checks,
                                        check_new_hash=
                                        'check_is_new_hash' in checks)
        result = self.registry_client.push_image(self.name, self.version, local_name=self.local_name)
        for tag in self.equal_tags:
            self.registry_client.push_image(self.name, str(tag), local_name=self.local_name)
        return result

    def rollback(self, prev_release=None,
                 validate=True, tags_to_move=None,
                 delete_equal_content_tags=False):
        validate and self.validate_rollback(prev_release)
        self.sync_with_remote()
        prev_release = prev_release or self._prev
        to_move = []
        if not delete_equal_content_tags:
            to_move = self.equal_tags[:]
        if prev_release:
            prev_release.sync_with_remote()
            to_move.append(prev_release.version)
            if tags_to_move:
                to_move_prev = [tag for tag in tags_to_move if tag not in prev_release.equal_tags]
                to_move_prev = list(set(to_move_prev))
                prev_release.update_tags(to_move_prev)
                to_move.extend(to_move_prev)
        return self.delete(with_equal_tags=True, excl_tags=to_move)

    def prev(self, unique_hash=True, prev_id=1):
        res = self.get_all_from_remote(self.name, self.registry_client,
                                       local_name=self.local_name,
                                       unique_hashes=unique_hash)
        if len(res) < 2:
            raise ValueError(f'Could not find previous release. Only {len(res)} found')
        print(f'Found {len(res)} releases')
        return res[prev_id]

    def sync_with_remote(self, images=None, version=False):
        if version:
            self.version = str(self.get_versions(last=True))
        self.equal_tags, data = self.get_equal_tags_from_remote(with_hash=True, images=images)
        digset, date = data['image']['imageDigest'], data['pushed_at']
        self.hash, self.pushed_at = digset, date
        return self

    def delete(self, with_equal_tags=True, incl_tags=None, excl_tags=None):
        result = self.registry_client.delete_image(self.name, str(self.version), soft=False)
        if with_equal_tags:
            for tag in self.equal_tags:
                if incl_tags and tag not in incl_tags:
                    continue
                if excl_tags and tag in excl_tags:
                    continue
                self.registry_client.delete_image(self.name, str(tag), soft=False)
        return result

    def delete_tags(self, tags, soft=False):
        for tag in tags:
            self.registry_client.delete_image(self.name, str(tag), soft=soft)
        return True

    def version_sem(self):
        return Version.coerce(self.version)

    def _check_is_next_release(self, images):
        versions = []
        for image in images:
            versions.append(Version(image['tag']))
        versions.sort(reverse=True)
        if versions and versions[0] >= Version.coerce(self.version):
            raise ValueError(f'Deployed version {str(versions[0])} is not smaller than current {str(self.version)}')
        return True

    def _resolve_conflicting_tags(self):
        for tag in self.equal_tags:
            res = self.registry_client.get_all_image_tags(self.name, tag)
            if res:
                if self.on_tag_exist == 'replace':
                    self.delete_tags([tag], soft=True)
                else:
                    raise ValueError(f'Tag <{tag}> already exist')

    def _check_is_different_release(self):
        test_tag = '0.0.0-test_tag_test'
        self.push(validate=False, test_tag=test_tag)
        digset = self.registry_client.get_image_hash(local_name=self.local_name)
        result = self.registry_client.get_images_on_unique_hash(self.name,
                                                                hash_filter=digset)
        self.delete_tags([test_tag])
        if result:
            for dig, img in result.items():
                tags = img['image']['imageTags']
                if tags != [test_tag]:
                    raise ValueError(
                        f'Already {len(list(result.values())[0])} tags: {tags} with the same hash: {digset} has been deployed')
        return True

    def get_versions(self, last=True):
        images = self.registry_client.get_all_image_tags(self.name, tag_filter=self.version_pattern)
        versions = []
        for image in images:
            versions.append(Version.coerce(image['tag']))
        versions.sort(reverse=True)
        if last:
            return versions[0] if versions else Version.coerce('0.0.0')
        return versions

    def next(self, incr_version=None, remote_sync=False, inplace=False):
        if remote_sync:
            version = self.get_versions(last=True)
        else:
            version = self.version_sem()
        if inplace:
            obj = self
        else:
            obj = copy.copy(self)
        position = incr_version or obj.incr_version
        obj.version = str(getattr(version, f'next_{position}')())
        return obj

    @classmethod
    def from_remote(cls, name, client: AwsRegistry,
                    local_name=None, sort_key='tag'):
        results = cls.get_all_from_remote(name, client, local_name,
                                          unique_hashes=False,
                                          sort_key=sort_key)
        if not results:
            raise ValueError(f"Remote release does not exist for {name}")
        return results[0]

    @classmethod
    def get_all_from_remote(cls, name,
                            client: AwsRegistry, local_name=None,
                            unique_hashes=False, sort_key='tag'):
        images_version = client.get_all_image_tags(name, tag_filter=cls.version_pattern)
        images = client.get_all_image_tags(name, tag_filter='')
        results = []
        hashes = set()
        for image in images_version:
            obj = cls(client, name, image['tag'], local_name=local_name)
            obj.sync_with_remote(images)
            if unique_hashes and obj.hash in hashes:
                continue
            results.append(obj)
        if sort_key == 'tag':
            return sorted(results, reverse=True)
        elif sort_key == 'pushed_at':
            return results
        else:
            ValueError('Sort key can be tag or pushed_at')
        return results

    @classmethod
    def from_local(cls, name, client: AwsRegistry,
                   local_name=None):
        obj = cls.from_remote(name, client, local_name=local_name)
        local_img = client.client_docker.images.get(name=local_name)
        if local_img:
            obj.local_name = local_img
        raise ValueError(f'Could not find any image {name}')

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version

    def __lt__(self, other):
        return self.name == other.name and self.version_sem() < other.version_sem()


class DockerComposeReleaseTrigger:
    REGISTRY = 'DOCKER_REGISTRY'
    VERSION = 'VERSION'

    def __init__(self, path, release: Release = None, services=None):
        self.path = path
        self.release = release
        if services and len(services) == 1 and 'all' in services:
            self.services = None
        else:
            self.services = services
        with open(path, 'r') as yml:
            self.raw_content = yml.read()

    def _prepare_content(self):
        new_content = self.raw_content
        if self.release and self.release.version:
            new_content = re.sub('\${VERSION.*?}', self.release.version, new_content, re.MULTILINE|re.DOTALL)
            new_content = re.sub('\${DOCKER_REGISTRY.*?}',
                                 self.release.registry_client.registry_name, new_content, re.MULTILINE)
        op = yaml.load(new_content, yaml.FullLoader)
        images = []

        for service, data in op['services'].items():
            if self.services:
                if service in self.services:
                    images.append(data['image'])
            else:
                images.append(data['image'])

        return new_content, images

    def build(self, extra_cmd=''):
        extra_cmd = extra_cmd or '' + ' '
        content, images = self._prepare_content()
        if self.services:
            extra_cmd += ' '.join(self.services)
        with tempfile.NamedTemporaryFile(mode='w+', dir=os.path.dirname(self.path)) as tp:
            tp.write(content)
            tp.seek(0)
            cmd = subprocess.Popen([f'docker-compose -f {tp.name} build {extra_cmd}'],
                                    stderr=subprocess.PIPE,
                                    stdout=subprocess.PIPE, shell=True)
            stdout, stderr = cmd.communicate()
            print(stdout.decode())
            print(stderr.decode())
            return stdout, stderr

    def get_releases(self):
        content, images = self._prepare_content()
        releases = []
        for image in images:
            name = re.search('/([^:]+):', image).group(1)
            nw_releas = copy.copy(self.release)
            nw_releas.name = name
            nw_releas.local_name = image
            if not nw_releas.version:
                nw_releas = nw_releas.next(remote_sync=True)
            releases.append(nw_releas)
        return releases

    def get_image_names(self):
        content, images = self._prepare_content()
        names = []
        for image in images:
            name = re.search('/([^:]+):', image).group(1)
            names.append(name)
        return names
