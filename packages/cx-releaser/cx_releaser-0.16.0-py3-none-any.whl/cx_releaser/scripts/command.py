from argparse import ArgumentParser

from cx_releaser.scripts.push import args as push_args, push
from cx_releaser.scripts.rollback import args as rollback_args, rollback


def main():
    parser = ArgumentParser()
    parser.add_argument('--tenant', help='Name of tenant (AWS account id) to perform operation')
    parser.add_argument('--images', help='List of images. Could be local_image:remote_image local_image1:remote_image1.'
                                         'If local image not specified will be set to remote_image',
                        nargs='+',
                        required=True)
    parser.add_argument('--image_prefix', help='Common prefix for all pushed images')
    parser.add_argument('--on_tag_exist', help='replace or raise if tag already exist',
                        choices=['replace', 'raise'])
    parser.add_argument('--all_tenants', action='store_true', help='If passed perform operation on all tenants')
    parser.add_argument('--version', help='Version of release')
    parser.add_argument('--local_version', help='Tag of local image to make release for')
    parser.add_argument('--config_path', help='Path to config file')
    subparsers = parser.add_subparsers(dest='command')
    rollback_args(subparsers), push_args(subparsers)
    args = parser.parse_args()
    if args.command == 'push':
        push(args.tenant, args.version, args.config_path, images=args.images,
             equal_tags=args.equal_tags, all_tenants=args.all_tenants, local_version=args.local_version,
             auto_incr_version=args.auto_incr_version,
             on_repository_not_exist=args.on_repository_not_exist,
             docker_compose_path=args.docker_compose_path,
             image_prefix=args.image_prefix, compose_services=args.compose_services,
             compose_build_cmd=args.compose_build_cmd, releases_file=args.releases_file)
    elif args.command == 'rollback':
        rollback(args.tenant, args.version, args.config_path,
                 prev_release_version=args.prev_release, images=args.images,
                 all_tenants=args.all_tenants,
                 local_version=args.local_version,
                 delete_all_equal_tags=args.all_tags,
                 docker_compose_path=args.docker_compose_path,
                 image_prefix=args.image_prefix, compose_services=args.compose_services)
    else:
        raise ValueError('Unknown command. Available push and rollback')


if __name__ == "__main__":
    main()
