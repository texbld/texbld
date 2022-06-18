# texbld

Although we expect LaTeX compilation to be a declarative process, the truth is
that it often requires external programs and dependencies that, by their nature,
can't be packaged together with LaTeX Packages. Furthermore, different LaTeX
distributions will sometimes have different outputs (especially when working
with tools like biber), which is an issue for reproducibility.

texbld aims to solve this problem by providing an environment where build images
are fully reproducible and shareable. It uses docker for absolute system
reproducibility and for usage across all platforms which it supports (MacOS,
Windows, and its native Linux).

Image hashes are used to ensure that any build is completely immutable,
preventing dependency modification issues.

Users can specify their build image in a simple TOML file (along with associated
files) and upload them to github, from which it can be inherited and used by
other people in their own projects. _Extensive Documentation will be released in the future._

Images can be inherited from packages in the local filesystem, GitHub, or Docker.

## Setting Up This Project

This project uses poetry as its dependency manager. Simply run `poetry install`
and `poetry shell` inside the project directory, and you should land in a
virtual environment with all of your dependencies.

In order to run tests in the virtual environment, run `pytest`.

## The Local Environment

Project configurations should be located at `(your project root)/texbld.toml`,
while local image configurations should be located at
`$XDG_CONFIG_DIR/texbld/images/$name.toml`.

# Pre-release TODO

- [x] Dockerfile generation
- [x] Building out docker images from a dependency chain
- [x] Write Project Parsers
- [x] Tests for generating project
- [x] Revert images back into toml files.
- [x] Write Tests for the scaffolders
- [x] TeXbld CLI
- [ ] TeXbld CLI Tests
