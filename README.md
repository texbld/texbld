# texbld

Although we expect LaTeX compilation to be a declarative process (source to
PDF), the compilations for large projects eventually require external programs
and dependencies that can't just be installed in a new computer. For example, a
compilation step might require running a script written in haskell, piping that
output into pandoc, then putting everything into a LaTeX file for compilation
with `pdflatex`. How will one ever get around to installing all of those
programs in a production system, which should never break?

Furthermore, different LaTeX distributions will have ever so slightly different
outputs (especially when working with biblatex), which is an issue for
reproducibility.

The first take on these problems was
[mktex](https://github.com/junikimm717/mktex). Although it solves some
dependency issues, it suffers from the various fragility and reproducibility
issues that come with using pre-built docker images. Furthermore, because of its
design, these images were forced to be monolithic, bloated, and ultimately
inflexible. Each build should have exactly the dependencies that it requires,
and nothing more!

`texbld` aims to solve these problems by providing an environment where build images
are fully reproducible and shareable. It uses docker for absolute system
reproducibility and for usage across all platforms which it supports (MacOS,
Windows, and its native Linux).

Image hashes are used to ensure that any docker image is **completely immutable**,
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

The project configuration file should be in `(project root)/texbld.toml`, while
local image configurations should be in `$HOME/.config/texbld/packages`.

## TODO

- [ ] Documentation at texbld.github.io

### Possible new Features

- [ ] Alias system in `~/.config/texbld/aliases.toml`
- [ ] Testing that an image builds properly without creating a project.
- [ ] Automatic package manager deduction in a v2 sourceimage parser
- Creating a custom registry? (Not likely due to stability issues)
