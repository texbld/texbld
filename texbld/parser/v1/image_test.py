from texbld.parser.v1.image import schema, to_source_image
from jsonschema import Draft7Validator, ValidationError
import toml
import pytest

v = Draft7Validator(schema)


def test_full_example():
    source = """
name = "myimage"
version = "1"

# optional, but apk is the default.
install = "apk add"
update = "apk update"

packages = [
  "biber", "python3"
]

# other commands to run.
setup = [
  "pip install pygments",
  "echo 'hello' > /hello/something.txt"
]

# inheritance patterns (all of them are mutually exclusive)
[inherit]
github = { owner = "texbld", repository = "base", revision = "rev", sha256 = "sha256" }

[files]
"script.sh" = "/script.sh"

[project.files]
"main.tex" = "main.tex"
"Makefile" = "Makefile"

[project.commands]
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

# inheritance patterns (all of them are mutually exclusive)
[inherit]
docker = "alpine"
    """
    instance = toml.loads(source)
    assert v.is_valid(instance=toml.loads(source))
    # pprint.pprint(to_source_image(source))


def test_github_example():
    source1 = """
name = "myimage"
version = "1"

[inherit]
github = { owner = "owner", repository = "repository", revision = "rev" }
    """
    source2 = """
name = "myimage"
version = "1"

[inherit]
github = { owner = "owner", repository = "repository", revision = "rev", sha256 = "sha256" }
    """
    to_source_image(source1)
    to_source_image(source2)


def test_exclusion_fail():
    source = """
name = "myimage"
version = "1"

[inherit]
docker = "alpine"
github = { owner = "owner", repository = "repository", revision = "rev", sha256 = "sha256" }
    """
    instance = toml.loads(source)
    with pytest.raises(ValidationError):
        to_source_image(source)
