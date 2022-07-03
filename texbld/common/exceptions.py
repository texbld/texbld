import sys
from jsonschema import ValidationError
from toml import TomlDecodeError
from texbld.config import PROJECT_CONFIG_FILE
import texbld.logger as logger
from docker.errors import ContainerError, BuildError

# tuple of actual and received hashes.


class HashMismatch(Exception):
    pass


# the github tarball url that could not be curled.
class GitHubNotFound(Exception):
    pass


# image name that couldn't be pulled.
class DockerNotFound(Exception):
    pass


# contains the string with the undefined version.
class NoSuchVersion(Exception):
    pass


class NoVersionSpecified(Exception):
    pass


# contains the list of images that have dependency cycles.
class DependencyCycle(Exception):
    pass


# command not found for a project
class CommandNotFound(Exception):
    pass


class TomlParseError(Exception):
    def __init__(self, msg: str, filename: str):
        self.args = (msg, filename)


class PermissionDenied(Exception):
    def __init__(self, path: str):
        self.path = path


def run_with_handlers(f: 'function'):
    try:
        f()
    except HashMismatch as e:
        actual, received = e.args
        logger.error(f"Hash Mismatch: Expected {actual}, got {received}")
        sys.exit(1)
    except GitHubNotFound as e:
        url, = e.args
        logger.error(f"Could not GET GitHub URL {url}")
        sys.exit(1)
    except DockerNotFound as e:
        image, = e.args
        logger.error(f"Could not find Docker image {image}")
        sys.exit(1)
    except NoSuchVersion as e:
        version, = e.args
        logger.error(f"Config version {version} does not exist.")
        sys.exit(1)
    except NoVersionSpecified as e:
        logger.error("No 'version' key specified in a configuration file.")
        sys.exit(1)
    except CommandNotFound as e:
        command, = e.args
        logger.error(
            f"command {command} not found in the local {PROJECT_CONFIG_FILE} file.")
        sys.exit(1)
    except ValidationError as e:
        message = next(iter(e.args))
        logger.error(f"Received a Validation Error: {message}")
        sys.exit(1)
    except FileNotFoundError as e:
        f, = e.args
        if type(f) == list:
            files = '\n'.join(f)
            logger.error(
                f"Could not find any of the following files:\n{files}")
        else:
            logger.error(f"Could not find file {f}.")
        sys.exit(1)
    except FileExistsError as e:
        f, = e.args
        logger.error(f"File {f} already exists. Aborting")
        sys.exit(1)
    except ContainerError as e:
        code = e.exit_status
        message = e.stderr
        logger.error(
            f"Container Error with status {code}: \n{str(message, 'utf-8')}")
        sys.exit(1)
    except BuildError as e:
        logger.error(f"Error while building containers: {e.msg}")
        sys.exit(1)
    except TomlParseError as e:
        msg, filename = e.args
        logger.error(f"Toml error while parsing {filename}:\n{msg}")
    except PermissionDenied as e:
        logger.error(
            f"Prevented arbitrary filesystem access at {e.path}. The image you are using may have malicious intent.")
