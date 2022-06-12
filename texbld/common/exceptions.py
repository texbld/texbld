# tuple of actual and received hashes.
class HashMismatch(Exception):
    pass


# the github tarball url that could not be curled.
class GitHubNotFound(Exception):
    pass


# image name that couldn't be pulled.
class DockerNotFound(Exception):
    pass


# contains the file path that was not found.
class FsNotFound(Exception):
    pass


# contains a string with the undefined version.
class NoSuchImageVersion(Exception):
    pass


class NoVersionSpecified(Exception):
    pass


# contains the list of images that have dependency cycles.
class DependencyCycle(Exception):
    pass
