# texbld

Although we expect LaTeX compilation to be a declarative process (source to
PDF), the compilations for large projects eventually require a large number of
custom external programs and dependencies. For example, a compilation step might
require running a script written in haskell, piping that output into pandoc,
then putting everything into a LaTeX file for compilation with `pdflatex`. Good
luck installing all of those programs (ESPECIALLY the pesky ghc dependencies) in
a production system!

Furthermore, different LaTeX distributions will have ever so slightly different
outputs (especially when working with biblatex), which is an issue for
reproducibility.

The first take on these problems was
[mktex](https://github.com/junikimm717/mktex). Although it solves some
dependency issues, it suffers from the various fragility and reproducibility
issues that come with using pre-built docker images. Furthermore, because of its
design, these images were forced to be monolithic, bloated, and ultimately
inflexible. Each build should have exactly the dependencies that it requires
and nothing more!

`texbld` aims to solve these problems by providing an environment where build images
are fully reproducible and shareable. It uses docker for absolute system
reproducibility and for usage across all platforms which it supports (MacOS,
Windows, and its native Linux).

Image hashes are used to ensure that any docker image is **completely immutable**,
preventing dependency modification issues.

Users can specify their build image in a simple TOML file (along with associated
files) and upload them to github, from which it can be inherited and used by
other people in their own projects.

Images can be inherited from packages in the local filesystem, GitHub, or Docker.

## Installation

The project is live on [pypi](https://pypi.org/project/texbld/).
Run `pip install -U texbld`.

### NixOS

Check the nix expressions in the release branch and configure accordingly.

In order to build the master branch, run `nix-build`.

## Setting Up This Project

### NixOS

Running `nix-shell` **should** set up everything. Note, however, that the
resulting poetry virtual environment will be installed in
`~/.cache/pypoetry/virtualenvs`, so it's not completely nix-based.

### Non-NixOS

This project uses poetry as its dependency manager. Simply run `poetry install`
and `poetry shell` inside the project directory, and you should land in a
virtual environment with all of your dependencies.

### Testing

In order to run tests in the virtual environment, run `pytest`.

## The Local Environment

The project configuration file should be in `(project root)/texbld.toml`, while
local image configurations should be in `$HOME/.config/texbld/packages`.
