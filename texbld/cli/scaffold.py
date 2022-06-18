from argparse import ArgumentParser
import json

import urllib3
from texbld.common.exceptions import GitHubNotFound
from texbld.common.image.image import DockerImage, GitHubImage, LocalImage
from texbld.directory import LOCALPACKAGES_DIR
from texbld.scaffold import scaffold

http = urllib3.PoolManager()


def scaffold_github(args):
    api_url = f"https://api.github.com/repos/{args.owner}/{args.repository}/commits/{args.rev}"
    with http.request('GET', api_url) as res:
        if res.status == 404:
            raise GitHubNotFound(f'https://github.com/{args.owner}/{args.repository}/commits/{args.rev}')
        data = json.loads(res.data.decode('utf-8'))
        args.rev = data['sha']
        print(f'Got revision {args.rev} from the GitHub API')
    if args.sha256 is None:
        image = GitHubImage(owner=args.owner, repository=args.repository,
                            revision=args.rev, sha256=args.sha256, config=args.config)
        image.pull()
        args.sha256 = image.client.getsha256()
    image = GitHubImage(owner=args.owner, repository=args.repository,
                        revision=args.rev, sha256=args.sha256, config=args.config)
    scaffold(image, args.directory)


def scaffold_local(args):
    image = LocalImage(name=args.image, config=args.config)
    scaffold(image, args.directory)


def scaffold_docker(args):
    image = DockerImage(name=args.image)
    scaffold(image, args.directory)


def add_scaffold_args(parser: ArgumentParser):
    subparsers = parser.add_subparsers()
    # arguments for github
    github = subparsers.add_parser('github', help='Use a TeXbld image from GitHub', aliases=['gh', 'g'])
    github.set_defaults(func=scaffold_github)
    github.add_argument('owner', help='owner of the GitHub repository')
    github.add_argument('repository', help='GitHub repository name')
    github.add_argument('directory', help='Directory to use while scaffolding')
    github.add_argument('--rev', '-r', default='master', help='commit of the repository to use')
    github.add_argument('--sha256', '-s', default=None, help='sha256 of the tarball (can be automatically generated)')
    github.add_argument('--config', '-c', default='image.toml', help='where the image configuration resides')
    # arguments for local
    local = subparsers.add_parser('local', help='Use a local TeXbld image', aliases=['l'])
    local.add_argument('image', help=f'TeXbld local image name (relative path from {LOCALPACKAGES_DIR})')
    local.add_argument('directory', help='Directory to use while scaffolding')
    local.add_argument('--config', '-c', default='image.toml', help='where the image configuration resides')
    # arguments for docker
    fromdocker = subparsers.add_parser('docker', help='Use a docker TeXbld image (blank)', aliases=['d'])
    fromdocker.add_argument('image', help=f'Docker image tag from registry')
    fromdocker.add_argument('directory', help='Directory to use while scaffolding')
