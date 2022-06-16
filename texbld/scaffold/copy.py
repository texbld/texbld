import os
import shutil
from texbld.common.exceptions import FsNotFound
from texbld.common.image import Image


def copy_image(image: Image, directory: str):
    if image.is_base():
        return
    dr = image.package_dir()
    for src, _ in image.get_source().project_files:
        src = os.path.join(dr, *src.split('/'))
        if not os.path.exists(src):
            raise FsNotFound(src)
    for src, dest in image.get_source().project_files:
        oldpath = os.path.join(image.package_dir(), *src.split('/'))
        newpath = os.path.join(directory, *dest.split('/'))
        os.makedirs(os.path.dirname(newpath), exist_ok=True)
        if os.path.isdir(oldpath):
            shutil.copytree(oldpath, newpath)
        else:
            shutil.copy(oldpath, newpath)