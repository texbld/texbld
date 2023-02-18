# CHANGELOG

## 0.5 (Under Development)

- Fixed inconsistent schemes
- Added TEXBLD_HOOK

## 0.4

- Removed requests dependency
- Build as a .pyz file (no python dependencies)
- Build logs for images are shown
- Cleaner Resource schemes (`github:owner/repo/branch#configpath`, `local:package#configpath`)
- Environmental variables (TEXBLD_CACHE, TEXBLD_PACKAGES)

## 0.3

- Container shows error logs
- Nix expressions for development

## 0.2

- Validation commands added
- Custom logging added (prettier error messages)
- Error handling added (including for TOML errors)
- Using Nix-inspired schemes for image names in the CLI instead of subparsers.
- FS access security vulnerability patched
- Utilities for pegging sha256 and revision of GitHub repositories.
