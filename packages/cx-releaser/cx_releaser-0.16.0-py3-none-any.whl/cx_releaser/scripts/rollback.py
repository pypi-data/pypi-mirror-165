import boto3

from cx_releaser.config.config import Config
from cx_releaser.src.docker_registry import AwsRegistry
from cx_releaser.src.release import DockerComposeReleaseTrigger, Release


def args(parser):
    rollback = parser.add_parser('rollback', help='Rollback release')
    rollback.add_argument('--prev_release', help='Version of prev release')
    rollback.add_argument('--auto_prev', help='Rollback to last different release deployed before newest one',
                          action='store_true')
    rollback.add_argument('--all_tags', help='If image has more than version tag, delete all of them',
                          action='store_true')
    rollback.add_argument('--docker_compose_path', help='Path to docker compose file to build and push images. If docker '
                                                    'compose path is provided --images should be compose')
    rollback.add_argument('--compose_services', nargs='+', help='Services for docker compose')
    return parser


def rollback(tenant, version, conf_path, images=None,
             prev_release_version=None, local_version=None, all_tenants=False,
             auto_prev=False, tags_to_move=None, delete_all_equal_tags=False,
             docker_compose_path=None, image_prefix=None, compose_services=None):
    if tenant is None and all_tenants is False:
        raise ValueError('Specify tenant or pass all_tenants')
    conf = Config(conf_path)
    tenants = [conf.get_by(tenant)] if tenant else list(conf.traverse_envs())
    releases = []
    for tenant_conf in tenants:
        registry = AwsRegistry(boto3.client('ecr', region_name=tenant_conf.get('region_name', 'us-east-1'),
                                            aws_access_key_id=tenant_conf['aws_access_key_id'],
                                            aws_secret_access_key=tenant_conf['aws_secret_access_key']))
        for image in images:
            if ':' in image:
                local, remote = image.split(':')
                all_remote = remote.split(',')
            else:
                local, remote = local_version, image
                all_remote = [remote]
            if docker_compose_path:
                trigger = DockerComposeReleaseTrigger(docker_compose_path,
                                                      services=compose_services)
                all_remote = trigger.get_image_names()
            for remote in all_remote:
                remote_name = ''.join([image_prefix or '', remote])
                if not version:
                    release = Release.from_remote(remote_name, registry, local)
                else:
                    release = Release(registry, remote_name, version, local_name=local)
                if prev_release_version:
                    prev_release = Release(registry, remote, prev_release_version, local_name=local)
                    release._prev = prev_release
                elif auto_prev:
                    release._prev = release.prev()
                releases.append((tenant_conf, release))
    for tenant_conf, release in releases:
        release.validate_rollback(release._prev)
    for tenant_conf, release in releases:
        tags_to_move = tags_to_move or tenant_conf.get('tags_to_move')
        release.rollback(tags_to_move=tags_to_move, delete_equal_content_tags=delete_all_equal_tags)
        print(f'Successfully performed rollback of {release.version} on tenant {release.registry_client.registry_name}')
