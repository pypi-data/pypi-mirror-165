import os.path

import pytest

from cx_releaser.src.release import DockerComposeReleaseTrigger, Release


@pytest.mark.usefixtures("example_release_name")
@pytest.mark.usefixtures('example_aws_registry')
class TestReleasePush:

    @pytest.fixture(autouse=True)
    def get_release(self, example_aws_registry, example_release_name):
        self._release = Release.from_remote(example_release_name, example_aws_registry)

    def test_push(self):
        assert self._release.push() == '{Pushed Successfully}'

    def test_push_docker_compose(self):
        names = ['my_sevice', 'my_sevice2']
        path = os.path.dirname(__file__)
        compose = os.path.join(path, 'data', 'dc.yml')
        compose = DockerComposeReleaseTrigger(compose, self._release)
        dw = compose.get_releases()
        for n, rel in enumerate(dw):
            assert rel.name == names[n]
            assert rel.push() == '{Pushed Successfully}'
