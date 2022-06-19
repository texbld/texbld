import argparse
from texbld.cli.project import add_build_args, add_run_args

from texbld.cli.scaffold import add_scaffold_args
from texbld.config import VERSION

parser = argparse.ArgumentParser(
    prog="texbld", description="A dockerized build tool for paper compilation")
parser.set_defaults(func=lambda _: parser.print_help())
parser.add_argument('--version', '-v', action='version', version=f'texbld {VERSION}')
subparsers = parser.add_subparsers()

add_scaffold_args(subparsers.add_parser('generate', aliases=[
                  'g'], help="Scaffold a project based on a TeXbld image"))
add_build_args(subparsers.add_parser('build', aliases=[
               'b'], help="Build the necessary images for a TeXbld project"))
add_run_args(subparsers.add_parser('run', aliases=['r'],
             help="Run a script in the corresponding TeXbld docker container"))


def execute(cli_args: 'list[str]'):
    args = parser.parse_args(cli_args)
    args.func(args)


def run():
    import sys
    execute(sys.argv[1:])
