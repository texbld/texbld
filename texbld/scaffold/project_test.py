from texbld.common.image.image import DockerImage, GitHubImage, LocalImage
from texbld.scaffold.project import project_toml_gen
from texbld.common.project import Project
from texbld.common.project.parse import parse_project


def test_1():
    image = LocalImage(name="test_gen1")
    ref = Project(name="hello", image=LocalImage(name="test_gen1"), commands=dict(
        compile="pandoc -o main.pdf main.md"
    ))  # note that when we parse a project, the evaluated image is shallow.
    src = project_toml_gen("hello", image)
    assert parse_project(src) == ref


def test_2():
    image = DockerImage(name="alpine")
    ref = Project(name="name", image=DockerImage(name="alpine"), commands=dict(
    ))  # note that when we parse a project, the evaluated image is shallow (dependencies not evaluated).
    src = project_toml_gen("name", image)
    assert parse_project(src) == ref


def test_3():
    def factory():
        return GitHubImage(
            owner="texbld", repository="sample-image", revision="04f2b5a50d65eeb2b42f7329c7eea37d8c880c85",
            sha256="63a8827ae24969d0d829365f54fa4aa3e001a1f2f76b47fd96ac482894c35c00")
    image = factory()
    ref = Project(name="name", image=factory(), commands=dict(
        compile="latexmk -pdf main.tex",
        watch="latexmk -pdf -pvc main.tex",
        clean="rm -rf main.aux main.log",
    ))  # note that when we parse a project, the evaluated image is shallow (dependencies not evaluated).
    src = project_toml_gen("name", image)
    assert parse_project(src) == ref
