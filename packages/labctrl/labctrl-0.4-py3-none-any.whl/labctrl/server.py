"""
This module contains utilities to serve resource classes remotely

Instantiated resources can be added or removed on demand.
Resources can be instantiated from .yml config files as well.
"""

import argparse
from pathlib import Path

import Pyro5.api as pyro
import Pyro5.errors

from labctrl.instrument import Instrument
from labctrl.logger import logger
from labctrl.resource import locate, Resource
from labctrl.settings import Settings
import labctrl.yamlizer as yml


class ServerError(Exception):
    """ """


@pyro.expose
class Server:
    """ """

    NAME = "SERVER"
    PORT = 9090  # port to bind a remote server on, used to initialize Pyro Daemon
    URI = f"PYRO:{NAME}@localhost:{PORT}"  # unique resource identifier (URI)

    def __init__(self, configpath: Path, daemon: pyro.Daemon) -> None:
        """ """
        logger.debug("Initializing the remote Server...")

        self._configpath: Path = configpath
        self._resources: list[Resource] = None
        self._daemon = daemon
        # self._services is a dict with key: resource name, value: remote resource URI
        self._services = {}  # will be updated by _serve()

        self._register()  # locate and register resource classes with yaml and pyro
        self._load()
        self._serve()

        logger.debug("Done initializing the remote Server.")

    @property
    def services(self) -> dict[str, str]:
        """ """
        return self._services.copy()

    def _register(self) -> None:
        """ """
        resourcepath = Settings().resourcepath
        logger.debug(f"Found labctrl setting {resourcepath = }.")
        resource_classes = locate(Path(resourcepath))
        for resource_class in resource_classes:
            yml.register(resource_class)
            pyro.expose(resource_class)
            logger.debug(f"Registered '{resource_class}' with yaml and pyro.")

    def _load(self) -> None:
        """ """
        self._resources = yml.load(self._configpath)
        logger.info(f"Found {len(self._resources)} resource(s) in {self._configpath}.")

        for resource in self._resources:
            self._services[resource.name] = resource
            logger.info(f"Staged Resource named '{resource.name}'.")

        if len(self._resources) != len(self._services):
            message = (
                f"Two or more resources in '{self._configpath}' share a name. "
                f"All resources must have unique names to be staged."
            )
            logger.error(message)
            raise ServerError(message)

    def _serve(self) -> None:
        """ """
        for name, resource in self._services.items():
            uri = self._daemon.register(resource, objectId=name)
            self._services[name] = uri
            logger.info(f"Served '{resource}' remotely at '{uri}'.")

    def teardown(self) -> None:
        """ """
        self.save()

        for resource in self._resources:
            if isinstance(resource, Instrument):
                try:
                    resource.disconnect()
                except ConnectionError:
                    logger.warning(
                        f"Can't disconnect '{resource}' due to a connection error. "
                        f"Check the instrument's connection and restart the Server."
                    )

        self._daemon.shutdown()
        logger.debug("Tore down the Server gracefully!")

    def save(self) -> None:
        """ """
        logger.debug(f"Saving the state of served Resources to {self._configpath}...")
        for resource in self._resources:
            yml.dump(self._configpath, resource)


def link() -> tuple[pyro.Proxy, list[pyro.Proxy]]:
    """ """
    logger.info("Linking up to the remote Server...")

    server_proxy = pyro.Proxy(Server.URI)
    try:
        remote_services = server_proxy.services
    except Pyro5.errors.CommunicationError:
        message = f"Did not find the remote Server at {Server.URI}."
        logger.error(message)
        raise ServerError(message) from None
    else:
        resource_proxies = [pyro.Proxy(uri) for uri in remote_services.values()]
        return server_proxy, resource_proxies


def unlink(server: pyro.Proxy, *resources: pyro.Proxy) -> None:
    """ """
    server.save()
    release(server)
    for resource in resources:
        release(resource)

    logger.info("Released the link to the remote Server.")

def release(proxy: pyro.Proxy) -> None:
    """ """
    proxy._pyroRelease()

def setup(configpath: Path) -> None:
    """ """
    logger.info("Setting up the remote Server...")

    daemon = pyro.Daemon(port=Server.PORT)
    server = Server(configpath, daemon)
    server_uri = daemon.register(server, objectId=Server.NAME)
    logger.info(f"Registered the remote Server at '{server_uri}'.")

    with daemon:
        logger.info("Remote Server daemon is now listening for requests...")
        daemon.requestLoop()
        logger.info("Exited remote Server daemon request loop.")


def teardown() -> None:
    """ """
    try:
        with pyro.Proxy(Server.URI) as server:
            server.teardown()
    except Pyro5.errors.CommunicationError:
        message = f"No remote Server to teardown at {Server.URI}. "
        logger.error(message)
        raise ServerError(message) from None
    else:
        logger.info(f"Tore down the remote Server at '{Server.URI}'.")


if __name__ == "__main__":

    # command line argument definition
    parser = argparse.ArgumentParser(description="Setup or Teardown the remote Server")
    parser.add_argument(
        "--run",
        help="--run to setup & --no-run to teardown the remote Server",
        action=argparse.BooleanOptionalAction,
        required=True,
    )
    parser.add_argument(
        "configpath",
        help="path to the yml config file to serve Resources remotely from",
        type=Path,
    )
    args = parser.parse_args()

    # command line argument handling
    if args.run:  # setup remote Server with resources from user supplied configpath
        setup(args.configpath)
    else:  # teardown remote Server
        teardown()
