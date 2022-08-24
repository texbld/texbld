# TODO

## Bugs

## To Implement

- [x] Implement an install script for TeXbld (ongoing)
- [ ] Allow singleton image usage for LocalImage (relative paths)
- [ ] Alias system in `~/.config/texbld/aliases.toml`
- [ ] Environment variables for dynamic configuration
- [x] Change Resource Schemes to be more nix-like (Get rid of \# for branch)
- [x] Use the low-level APIClient to stream logs when building images

## Config version 2

- [ ] Automatic package manager deduction (custom ways of dealing with them)
- [ ] Automatically determining packages? (Annoying non-existent errors)
- [ ] Arbitrary Arguments to `texbld run` (e.g. `"compile $" = "pandoc $1 -o output.pdf"`)

## Far

- [ ] API refactor?
- [ ] Official Registry of cached builds
- [ ] Separate Tarball Image?
