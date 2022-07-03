from argparse import ArgumentParser
import os

from texbld.utils.search import search_up_project


# requires --cache in argument.
def build_deps(args):
    cache = args.cache
    project = search_up_project(os.getcwd())
    project.build(cache=cache)


# requires command in positional.
def run(args):
    project = search_up_project(os.getcwd())
    project.image.pull()
    project.run(args.command)


def add_build_args(parser: ArgumentParser):
    parser.add_argument('--cache', action='store_true',
                        help="Use cache when building")
    parser.set_defaults(func=build_deps)


def add_run_args(parser: ArgumentParser):
    parser.add_argument('command', help="Command to run")
    parser.set_defaults(func=run)
