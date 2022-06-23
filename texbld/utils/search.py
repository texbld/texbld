import os
from texbld.common.project.parse import parse_project
from texbld.config import PROJECT_CONFIG_FILE
from texbld.common.project import Project


def search_up_project(dr: str) -> 'Project':
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
