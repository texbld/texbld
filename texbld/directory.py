import os
import sys
from pathlib import Path

CONFIG_BASE = os.path.join(Path.home(), ".config", "texbld")
CACHE_BASE = os.path.join(Path.home(), ".cache", "texbld")
SCAFFOLD_TESTS = ""

# check if the cache is defined.
if cache_environ := os.environ.get("TEXBLD_CACHE"):
    CACHE_BASE = os.path.abspath(cache_environ)

if "pytest" in sys.modules:
    dirname = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "test_files")
    CONFIG_BASE = os.path.join(dirname, "config")
    CACHE_BASE = os.path.join(dirname, "cache")
    SCAFFOLD_TESTS = os.path.join(dirname, "cache", "scaffold")
    os.makedirs(SCAFFOLD_TESTS, exist_ok=True)


CONFIG_DIR = CONFIG_BASE
TARBALL_CACHE_DIR = os.path.join(CACHE_BASE, "tarballs")
PACKAGE_CACHE_DIR = os.path.join(CACHE_BASE, "packages")
BUILD_CACHE_DIR = os.path.join(CACHE_BASE, "builds")

# check if the texbld package directory is defined.
if texbld_packages := os.environ.get("TEXBLD_PACKAGES"):
    LOCALPACKAGES_DIR = os.path.abspath(texbld_packages)
else:
    LOCALPACKAGES_DIR = os.path.join(CONFIG_BASE, "packages")

dirs = [
    CONFIG_DIR, LOCALPACKAGES_DIR, TARBALL_CACHE_DIR, PACKAGE_CACHE_DIR, BUILD_CACHE_DIR
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
