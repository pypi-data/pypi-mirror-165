import boto3

from cx_releaser.config.config import Config
from cx_releaser.src.docker_registry import AwsRegistry
from cx_releaser.src.release import DockerComposeReleaseTrigger, Release


def args(parser):
    push = parser.add_parser('push', help='Push release')
    push.add_argument('--equal_tags', help='Additional tags to add to release image', nargs='+')
    push.add_argument('--auto_incr_version', choices=['minor', 'major', 'patch'], default='minor')
    push.add_argument('--on_repository_not_exist', choices=['create', 'raise'], default='raise')
    push.add_argument('--docker_compose_path', help='Path to docker compose file to build and push images. If docker '
                                                      'compose path is provided --images should be compose')
    push.add_argument('--compose_services', nargs='+', help='Services for docker compose')
    push.add_argument('--compose_build_cmd', help='string containing additional compose build arguments')
    push.add_argument('--releases_file', help="name of a file to store list of performed releases")
    return parser


def push(tenant, version, conf_path, images=None, equal_tags=None, local_version=None, all_tenants=False,
         auto_incr_version='minor', on_tag_exist=None, on_repository_not_exist=None,
         docker_compose_path=None, image_prefix=None, compose_services=None, compose_build_cmd='', releases_file=None):
    if tenant is None and all_tenants is False:
        raise ValueError('Specify tenant or pass all_tenants')
    conf = Config(conf_path)
    tenants = [conf.get_by(tenant)] if tenant else list(conf.traverse_envs())
    releases = []
    for tenant_conf in tenants:
        registry = AwsRegistry(boto3.client('ecr', region_name=tenant_conf.get('region_name', 'us-east-1'),
                                            aws_access_key_id=tenant_conf['aws_access_key_id'],
                                            aws_secret_access_key=tenant_conf['aws_secret_access_key']))
        version = version or tenant_conf.get('version')
        equal_tags = equal_tags or tenant_conf.get('equal_tags')
        for image in images:
            if ':' in image:
                local, remote = image.split(':')
                all_remote = remote.split(',')
            else:
                local, remote = local_version, image
                all_remote = [remote]
            if docker_compose_path:
                remote_name = ''.join([image_prefix or '', remote])
                on_tag_exist = on_tag_exist or tenant_conf.get('on_tag_exist')
                release = Release(registry, remote_name, version, equal_tags=equal_tags,
                                  local_name=local,
                                  incr_version=auto_incr_version,
                                  on_tag_exist=on_tag_exist,
                                  on_repo_not_exist=on_repository_not_exist)
                trigger = DockerComposeReleaseTrigger(docker_compose_path, release, compose_services)
                trigger.build(compose_build_cmd)
                releases = [(tenant_conf, release) for release in trigger.get_releases()]
            else:
                for remote in all_remote:
                    remote_name = ''.join([image_prefix or '', remote])
                    on_tag_exist = on_tag_exist or tenant_conf.get('on_tag_exist')
                    release = Release(registry, remote_name, version, equal_tags=equal_tags,
                                      local_name=local,
                                      incr_version=auto_incr_version,
                                      on_tag_exist=on_tag_exist,
                                      on_repo_not_exist=on_repository_not_exist)
                    if not version:
                        release = release.next(remote_sync=True)
                    print(f'Preparing release: {release.name} with version: {release.version}')
                    releases.append((tenant_conf, release))
    for tenant_conf, release in releases:
        check_is_newest_version, check_is_new_hash = tenant_conf.get('check_is_newest_version'), \
                                                     tenant_conf['check_is_new_hash']
        release.validate_push(check_is_next=check_is_newest_version,
                              check_new_hash=check_is_new_hash)

    performed_releases = set()
    for tenant_conf, release in releases:
        release.push()
        performed_releases.add(f"{release.registry_client.registry_name}/{release.name}:{release.version}")
        print(f'Successfully performed release of {release.name} with version: {release.version} on tenant {release.registry_client.registry_name}')

    if not releases_file:
        return None

    with open(releases_file, "w") as f:
        for release in performed_releases:
            f.write(f"{release}\n")
