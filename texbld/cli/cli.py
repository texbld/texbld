import argparse
from texbld.cli.getsha256 import add_sha_args
from texbld.cli.validate import add_validate_args
from texbld.cli.project import add_build_args, add_run_args

from texbld.cli.scaffold import add_scaffold_args
from texbld.common.exceptions import run_with_handlers
from texbld.config import VERSION

parser = argparse.ArgumentParser(
    prog="texbld", description="A dockerized build tool for paper compilation")
parser.set_defaults(func=lambda _: parser.print_help())
parser.add_argument('--version', '-v', action='version',
                    version=f'texbld {VERSION}')
subparsers = parser.add_subparsers()

add_scaffold_args(subparsers.add_parser('generate', aliases=[
                  'g'], help="Scaffold a project based on a TeXbld image"))
add_build_args(subparsers.add_parser('build', aliases=[
               'b'], help="Build the necessary images for a TeXbld project"))
add_run_args(subparsers.add_parser('run', aliases=['r'],
             help="Run a script in the corresponding TeXbld docker container"))
add_validate_args(subparsers.add_parser(
    'validate', aliases=['v'], help="Run validations"))
add_sha_args(subparsers.add_parser('getsha256', aliases=['sha'], help='Get the sha256 of a GitHub Image'))


def execute(cli_args: 'list[str]'):
    args = parser.parse_args(cli_args)
    args.func(args)


def run():
    import sys
    run_with_handlers(lambda: execute(sys.argv[1:]))
