import os
import shutil
import pytest
from texbld.cli.cli import execute
from texbld.directory import SCAFFOLD_TESTS
from texbld.common.exceptions import CommandNotFound, DependencyCycle, GitHubNotFound


def test_github_1():
    os.chdir(SCAFFOLD_TESTS)
    dr = os.path.join(SCAFFOLD_TESTS, "cli_github_1")
    if os.path.isdir(dr):
        shutil.rmtree(dr)
    args = 'generate project github:texbld/sample-image#master --config markdown.toml cli_github_1'
    execute(args.split())
    assert os.path.isfile(os.path.join(dr, "main.md"))
    assert os.path.isfile(os.path.join(dr, "texbld.toml"))
    assert not os.path.isfile(os.path.join(dr, "main.tex"))


def test_github_2():
    os.chdir(SCAFFOLD_TESTS)
    dr = os.path.join(SCAFFOLD_TESTS, "cli_github_2")
    if os.path.isdir(dr):
        shutil.rmtree(dr)
    args = 'generate project github:texbld/sample-image#nonexistent cli_github_2'
    with pytest.raises(GitHubNotFound):
        execute(args.split())


def test_github_3():
    os.chdir(SCAFFOLD_TESTS)
    dr = os.path.join(SCAFFOLD_TESTS, "cli_github_3")
    if os.path.isdir(dr):
        shutil.rmtree(dr)
    args = 'generate p github:texbld/sample-image --config markdown.toml cli_github_3'
    execute(args.split())
    assert os.path.isfile(os.path.join(dr, "main.md"))
    assert os.path.isfile(os.path.join(dr, "texbld.toml"))
    assert not os.path.isfile(os.path.join(dr, "main.tex"))


def test_docker():
    os.chdir(SCAFFOLD_TESTS)
    dr = os.path.join(SCAFFOLD_TESTS, "cli_docker_1")
    if os.path.isdir(dr):
        shutil.rmtree(dr)
    args = 'g p docker:alpine cli_docker_1'
    execute(args.split())
    assert len(os.listdir(dr)) == 1
    assert os.path.isfile(os.path.join(dr, "texbld.toml"))


def test_image_1():
    os.chdir(SCAFFOLD_TESTS)
    dr = os.path.join(SCAFFOLD_TESTS, "cli_image_1")
    if os.path.isdir(dr):
        shutil.rmtree(dr)
    args = 'generate image cli_image_1'
    execute(args.split())
    assert len(os.listdir(dr)) == 1
    assert os.path.isfile(os.path.join(dr, "image.toml"))
    assert "cli_image_1" in open(os.path.join(dr, "image.toml")).read()


def test_local_1():
    with pytest.raises(DependencyCycle):
        execute('validate image test_dep2_1'.split())


def test_local_depcycle():
    with pytest.raises(DependencyCycle):
        execute('validate image test_dep2_1'.split())


def test_local_full():
    os.chdir(SCAFFOLD_TESTS)
    dr = os.path.join(SCAFFOLD_TESTS, "cli_local_full")
    if os.path.isdir(dr):
        shutil.rmtree(dr)
    execute('generate p local:test_sc1_2 cli_local_full'.split())
    assert len(os.listdir(dr)) == 4
    assert os.path.isfile(os.path.join(dr, "texbld.toml"))
    os.chdir(dr)
    execute('build'.split())
    with pytest.raises(CommandNotFound):
        args = 'run nonexistent'
        execute(args.split())
    args = 'run clean'
    execute(args.split())
