from texbld.parser.v1.project import schema, to_project
from jsonschema import Draft7Validator, ValidationError
import toml
import pytest

v = Draft7Validator(schema)


def test_full_example():
    source = """
name = "myproject"
version = "1"

[image]
github = { owner = "texbld", repository = "base", revision = "rev", sha256 = "sha256" }

[commands]
compile = "latexmk -pdf main.tex"
watch = "latexmk -pdf -pvc main.tex"
clean = "rm -rf main.tex"
    """
    instance = toml.loads(source)
    assert v.is_valid(instance=toml.loads(source))
    # pprint.pprint(to_source_image(source))


def test_minimal_example():
    source = """
name = "myimage"
version = "1"

[image]
docker = "alpine"
    """
    instance = toml.loads(source)
    assert v.is_valid(instance=toml.loads(source))


def test_minimal_example_2():
    source = """
name = "myimage"
version = "1"

# inheritance patterns (all of them are mutually exclusive)
[image]
local = "dependency"
    """
    instance = toml.loads(source)
    assert v.is_valid(instance=toml.loads(source))


def test_exclusion_fail():
    source = """
name = "myimage"
version = "1"

[image]
docker = "alpine"
github = { owner = "owner", repository = "repository", revision = "rev", sha256 = "sha256" }
    """
    instance = toml.loads(source)
    with pytest.raises(ValidationError):
        to_project(source)
