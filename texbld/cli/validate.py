from argparse import ArgumentParser
from texbld.utils.search import search_up_project
from texbld.common.image import LocalImage
from texbld.common.solver import Solver
from texbld.docker.build import build
from texbld.cli.resource import ImageResource
from texbld.scaffold.validate import validate_solver_files


# takes an image and validates it.
def validate_image(args):
    s = Solver(ImageResource.get_image(args.name))
    build(s, cache=args.cache)
    validate_solver_files(s)


# validate the texbld.toml file.
def validate_project(args):
    search_up_project(args.directory)


def add_validate_args(parser: ArgumentParser):
    subparsers = parser.add_subparsers()
    image = subparsers.add_parser(
        'image', aliases=['i'], help="Validate a local image")
    image.add_argument('name', help='TeXbld image resource scheme')
    image.add_argument('--cache', action='store_true',
                       help="Use cache when validating")
    image.set_defaults(func=validate_image)
    project = subparsers.add_parser(
        'project', aliases=['p'], help="Validate a project")
    project.add_argument(
        'directory', help='Path of the directory where the texbld project is')
    project.set_defaults(func=validate_project)
