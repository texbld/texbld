import os
import shutil
from texbld.common.exceptions import PermissionDenied
from texbld.common.image import Image
from texbld.scaffold.validate import validate_image_files


def copy_image(image: Image, directory: str):
    if image.is_base():
        return
    validate_image_files(image)
    for src, dest in image.get_source().project_files.items():
        oldpath = os.path.join(image.package_dir(), *src.split('/'))
        newpath = os.path.abspath(os.path.join(directory, *dest.split('/')))
        if not newpath.startswith(directory):
            raise PermissionDenied(path=newpath)
        os.makedirs(os.path.dirname(newpath), exist_ok=True)
        if os.path.isdir(oldpath):
            shutil.copytree(oldpath, newpath)
        else:
            shutil.copy(oldpath, newpath)
