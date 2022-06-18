# tuple of actual and received hashes.
class HashMismatch(Exception):
    pass


# the github tarball url that could not be curled.
class GitHubNotFound(Exception):
    pass


# image name that couldn't be pulled.
class DockerNotFound(Exception):
    pass


# contains a string with the undefined version.
class NoSuchImageVersion(Exception):
    pass


class NoVersionSpecified(Exception):
    pass


# contains the list of images that have dependency cycles.
class DependencyCycle(Exception):
    pass


# command not found for a project
class CommandNotFound(Exception):
    pass
