import os
import shutil
from texbld.common.image import Image
from texbld.config import PROJECT_CONFIG_FILE
from texbld.scaffold.copy import copy_image
from texbld.scaffold.project import project_toml_gen
from texbld.common.solver import Solver


def scaffold_project(image: Image, directory: str):
    directory = os.path.abspath(directory)
    name = os.path.basename(directory)
    if os.path.exists(directory):
        raise FileExistsError(directory)
    os.makedirs(directory)
    for img in reversed(Solver(image).images()):
        print("copying image", img.package_dir())
        if not img.is_base():
            copy_image(img, directory)
    configpath = os.path.join(directory, PROJECT_CONFIG_FILE)
    with open(configpath, "w") as w:
        w.write(project_toml_gen(name, image))


def scaffold_image(directory: str):
    directory = os.path.abspath(directory)
    name = os.path.basename(directory)
    if os.path.exists(directory):
        raise FileExistsError(directory)
    os.makedirs(os.path.dirname(directory), exist_ok=True)
    src = os.path.join(os.path.dirname(__file__), "sample_image")
    shutil.copytree(src, directory)
    text = open(os.path.join(directory, "image.toml")).read()
    open(os.path.join(directory, "image.toml"), "w").write(text.replace("image_name", name))
