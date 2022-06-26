from argparse import ArgumentParser

from texbld.common.image.image import DockerImage, GitHubImage, LocalImage
from texbld.directory import LOCALPACKAGES_DIR
from texbld.scaffold import scaffold_project, scaffold_image
import texbld.logger as logger
from texbld.utils.github import get_github_rev


def scaffold_github(args):
    args.rev = get_github_rev(args.owner, args.repository, args.rev)
    if args.sha256 is None:
        image = GitHubImage(owner=args.owner, repository=args.repository,
                            revision=args.rev, sha256=args.sha256, config=args.config)
        image.pull()
        args.sha256 = image.client.getsha256()
    image = GitHubImage(owner=args.owner, repository=args.repository,
                        revision=args.rev, sha256=args.sha256, config=args.config)
    scaffold_project(image, args.directory)


def scaffold_local(args):
    image = LocalImage(name=args.image, config=args.config)
    scaffold_project(image, args.directory)


def scaffold_docker(args):
    image = DockerImage(name=args.image)
    scaffold_project(image, args.directory)


def scaffold_sample_image(args):
    scaffold_image(args.directory)


def add_scaffold_args(parser: ArgumentParser):
    subparsers = parser.add_subparsers()
    # arguments for github
    github = subparsers.add_parser(
        'github', help='Use a TeXbld image from GitHub', aliases=['gh', 'g'])
    github.set_defaults(func=scaffold_github)
    github.add_argument('owner', help='owner of the GitHub repository')
    github.add_argument('repository', help='GitHub repository name')
    github.add_argument('directory', help='Directory to use for scaffolding')
    github.add_argument('--rev', '-r', default='master',
                        help='commit of the repository to use')
    github.add_argument('--sha256', '-s', default=None,
                        help='sha256 of the tarball (can be automatically generated)')
    github.add_argument('--config', '-c', default='image.toml',
                        help='where the image configuration resides')
    # arguments for local
    local = subparsers.add_parser(
        'local', help='Use a local TeXbld image', aliases=['l'])
    local.set_defaults(func=scaffold_local)
    local.add_argument(
        'image', help=f'TeXbld local image name (relative path from {LOCALPACKAGES_DIR})')
    local.add_argument('directory', help='Directory to use for scaffolding')
    local.add_argument('--config', '-c', default='image.toml',
                       help='where the image configuration resides')
    # arguments for docker
    fromdocker = subparsers.add_parser(
        'docker', help='Use a docker TeXbld image (blank)', aliases=['d'])
    fromdocker.set_defaults(func=scaffold_docker)
    fromdocker.add_argument('image', help=f'Docker image tag from registry')
    fromdocker.add_argument(
        'directory', help='Directory to use for scaffolding')
    # arguments for image
    image = subparsers.add_parser(
        'image', help='generate a sample image', aliases=['i'])
    image.set_defaults(func=scaffold_sample_image)
    image.add_argument('directory', help='Directory to use for scaffolding')
