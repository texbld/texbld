import os
from texbld.common.image import Image
from texbld.common.solver import Solver

# validates that an image has correct files to be scaffolded.


def validate_image_files(image: 'Image'):
    if image.is_base():
        return
    dr = image.package_dir()
    for src, _ in image.get_source().project_files.items():
        src = os.path.join(dr, *src.split('/'))
        if not os.path.exists(src):
            raise FileNotFoundError(src)


# validates that a solver will scaffold correct files.
def validate_solver_files(solver: 'Solver'):
    for image in solver.images():
        validate_image_files(image)
