# TODO

- Write tests for Dockerfile autogen
- Write methods for moving necessary files + the dockerfile to the build directory.
  - Note: you need to figure out how to generate directories on the fly.
- Build out everything in the dependency chain. (Docker should cache stuff)

# Later

- Implement `project.toml` v1 parsers and scaffolders (based on that
  project.toml)
- The scaffolders should overwrite project files and commands from dependencies.
