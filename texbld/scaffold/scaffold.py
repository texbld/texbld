import os
from texbld.common.image import Image
from texbld.config import PROJECT_CONFIG_FILE
from texbld.scaffold.copy import copy_image
from texbld.scaffold.project import project_toml_gen
from texbld.common.solver import Solver


def scaffold(image: Image, directory: str):
    directory = os.path.abspath(directory)
    name = os.path.basename(directory)
    if os.path.exists(directory):
        raise FileExistsError(directory)
    os.makedirs(directory)
    for img in reversed(Solver(image).images()):
        copy_image(image, directory)
    configpath = os.path.join(directory, PROJECT_CONFIG_FILE)
    with open(configpath, "w") as w:
        w.write(project_toml_gen(name, image))
