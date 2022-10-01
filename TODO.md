# TODO

## Bugs

## To Implement

- [ ] `texbld validate` has inconsistent schemes.
- [ ] Allow singleton image usage for LocalImage (relative paths)
- [ ] Replacing GitHub images with CLI utility (updating revisions, changing
      image repo, ...)
- [ ] Completely broken on an ARM-based RPI?

## Config version 2

- [ ] Automatic package manager deduction
- [ ] Automatically determining packages? (Annoying non-existent errors)
- [ ] Arbitrary Arguments to `texbld run` (e.g. `"compile $" = "pandoc $1 -o output.pdf"`)

## Far

- [ ] API refactor?
- [ ] Official Registry of cached builds
- [ ] Separate Tarball Image?
- [ ] Custom DSL for configuring texbld images (higher-level configuration)
