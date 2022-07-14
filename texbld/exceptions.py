import sys
from jsonschema import ValidationError
from texbld.config import PROJECT_CONFIG_FILE
import texbld.logger as logger
from docker.errors import ContainerError, BuildError, DockerException

# tuple of actual and received hashes.


class HashMismatch(Exception):
    def __init__(self, expected: str, received: str) -> None:
        super().__init__(expected, received)


# the github tarball url that could not be curled.
class GitHubNotFound(Exception):
    def __init__(self, url: str) -> None:
        super().__init__(url)


# image name that couldn't be pulled.
class DockerNotFound(Exception):
    def __init__(self, image: str) -> None:
        super().__init__(image)
    pass


# contains the string with the undefined version.
class NoSuchVersion(Exception):
    def __init__(self, version: str) -> None:
        super().__init__(version)


class NoVersionSpecified(Exception):
    def __init__(self) -> None:
        super().__init__()


# contains the list of images that have dependency cycles.
class DependencyCycle(Exception):
    def __init__(self, images: list) -> None:
        super().__init__(images)


# command not found for a project
class CommandNotFound(Exception):
    def __init__(self, command: str) -> None:
        super().__init__(command)


class TomlParseError(Exception):
    def __init__(self, msg: str, filename: str):
        super().__init__(msg, filename)


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
        fle, = e.args
        if type(fle) == list:
            files = '\n'.join(fle)
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
        logs = e.container.logs()
        logger.error(
            f"Container Error with status {code}:\n{str(message,'utf-8')}\n\n{logs.decode()}")
        e.container.remove()
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
    except DockerException as e:
        msg, = e.args
        logger.error(
            str(msg)
        )
