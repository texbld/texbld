import os
import sys
from pathlib import Path

CONFIG_BASE = os.path.join(Path.home(), ".config", "texbld")
CACHE_BASE = os.path.join(Path.home(), ".cache", "texbld")


if "pytest" in sys.modules:
    dirname = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "test_files")
    print("works", dirname)
    CONFIG_BASE = os.path.join(dirname, "config")
    CACHE_BASE = os.path.join(dirname, "cache")

CONFIG_DIR = CONFIG_BASE
LOCALPACKAGES_DIR = os.path.join(CONFIG_BASE, "packages")
TARBALL_CACHE_DIR = os.path.join(CACHE_BASE, "tarballs")
PACKAGE_CACHE_DIR = os.path.join(CACHE_BASE, "packages")
BUILD_CACHE_DIR = os.path.join(CACHE_BASE, "builds")

dirs = [
    CONFIG_DIR, LOCALPACKAGES_DIR, TARBALL_CACHE_DIR, PACKAGE_CACHE_DIR, BUILD_CACHE_DIR
]

for d in dirs:
    if not os.path.isdir(d):
        os.makedirs(d)
