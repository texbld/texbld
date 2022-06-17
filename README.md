# texbld

**Note: Under Development**

Although we expect LaTeX compilation to be a declarative process, the truth is
that it often requires external programs and dependencies that, by their nature,
can't be packaged together with LaTeX Packages. Furthermore, different LaTeX
distributions will sometimes have different outputs (especially when working
with tools like biber), which is an issue for reproducibility.

texbld aims to solve this problem by providing an environment where build images
are fully reproducible and shareable. It uses docker for absolute system
reproducibility and for usage across all platforms which it supports (MacOS,
Windows, and its native Linux).

## Functions of the texbld program

- Pull/building images
- build/watch latex templates
- Dependency solver for images (so that ppl can inherit and use other people's
  texbld images).
- Scaffold a project based on image and user preferences.

## Expected Local Environment

- Project configurations at `$PROJECT/texbld.toml`
- Personal image configurations at `$XDG_CONFIG_DIR/texbld/images/$name.toml`

# TODO

- [x] Dockerfile generation
- [x] Building out docker images from a dependency chain
- [x] Write Project Parsers
- [x] Tests for generating project
- [x] Revert images back into toml files.
- [ ] Scaffolders for a project
- [ ] TeXbld CLI
