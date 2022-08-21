from argparse import ArgumentParser
from texbld.cli.resource import ImageResource, image_resource_type
from texbld.scaffold import scaffold_project, scaffold_image


def scaffold_project_cli(args):
    image = ImageResource.get_image(args.resource)
    scaffold_project(image, args.directory)


def scaffold_image_cli(args):
    scaffold_image(args.directory)


def add_scaffold_args(parser: ArgumentParser):
    subparsers = parser.add_subparsers()
    project = subparsers.add_parser(
        'project', help='generate a project', aliases=['p'])
    project.add_argument(
        'resource', help='TeXbld image resource', type=image_resource_type)
    project.add_argument('directory', help='Directory to use for scaffolding')
    project.set_defaults(func=scaffold_project_cli)

    image = subparsers.add_parser(
        'image', help='generate a sample image', aliases=['i'])
    image.add_argument('directory', help='Directory to use for scaffolding')
    image.set_defaults(func=scaffold_image_cli)
