from argparse import ArgumentParser
import os

from texbld.config import PROJECT_CONFIG_FILE
from texbld.common.project import Project
from texbld.common.project.parse import parse_project


def search_up(dr: str) -> 'Project':
    dr = os.path.abspath(dr)
    searched = []
    while True:
        projectpath = os.path.join(dr, PROJECT_CONFIG_FILE)
        if os.path.isfile(projectpath):
            project = parse_project(open(projectpath).read())
            project.directory = dr
            return project
        # we are at root, and there is nothing more to do.
        if os.path.dirname(dr) == dr:
            raise FileNotFoundError(searched)
        searched.append(projectpath)
        dr = os.path.dirname(dr)


# requires --cache in argument.
def build_deps(args):
    cache = args.cache
    project = search_up(os.getcwd())
    project.build(cache=cache)


# requires command in positional.
def run(args):
    project = search_up(os.getcwd())
    project.image.pull()
    project.run(args.command)


def add_build_args(parser: ArgumentParser):
    parser.add_argument('--cache', '-c', action='store_true',
                        help="Use cache when building")
    parser.set_defaults(func=build_deps)


def add_run_args(parser: ArgumentParser):
    parser.add_argument('command', help="Command to run")
    parser.set_defaults(func=run)
