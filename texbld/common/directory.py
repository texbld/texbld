import os
from pathlib import Path

CONFIG_DIR = os.path.join(Path.home(), ".config", "texbld")
PACKAGES_DIR = os.path.join(Path.home(), ".config", "texbld", "packages")
TARBALL_CACHE_DIR = os.path.join(Path.home(), ".cache", "texbld", "tarballs")
PACKAGE_CACHE_DIR = os.path.join(Path.home(), ".cache", "texbld", "packages")
DOCKERFILE_CACHE_DIR = os.path.join(Path.home(), ".cache", "texbld", "dockerfiles")


dirs = [
    CONFIG_DIR, PACKAGES_DIR, TARBALL_CACHE_DIR, PACKAGE_CACHE_DIR, DOCKERFILE_CACHE_DIR
]

for d in dirs:
    if not os.path.isdir(d):
        os.makedirs(d)
