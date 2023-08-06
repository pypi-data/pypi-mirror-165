"""
This module contains utilities for staging Resources prior to running experiments.

Resouces can be loaded from .yml config files and can be added and removed on demand.
Only those Resource classes found in Settings().resourcepath can be staged.
The Stage can link up to the Server to retrieve remotely served Resources.
"""

from __future__ import annotations

from pathlib import Path

import Pyro5.api as pyro

from labctrl.instrument import Instrument
from labctrl.logger import logger
from labctrl.resource import locate, Resource
from labctrl.settings import Settings
import labctrl.server as server
import labctrl.yamlizer as yml


class Stage:
    """ """

    def __init__(
        self, name: str, *sources: Path | Resource, remote: bool = True
    ) -> None:
        """ """
        logger.debug(f"Setting up a Stage with {name = }...")

        self._name: str = name
        # self._configpath is where staged Resources without an associated configpath
        # will be saved to by default
        configfolder = Path(Settings().configpath)
        configfolder.mkdir(exist_ok=True)
        self._configpath: Path = configfolder / f"{name}.yml"
        self._configpath.touch(exist_ok=True)

        # _config is a dict with key: configpath, value: list[Resource] used for saving
        self._config: dict[Path, list[Resource]] = {self._configpath: []}
        # _resources is a list of Resource or resource proxy objects
        self._resources: list[Resource | pyro.Proxy] = []

        self._register()

        if sources:
            self.add(*sources)

        self._server, self._proxies = None, []  # will be updated by _link()
        if remote:
            self._link()

        logger.debug(f"Setup Stage '{name}' with config saved at '{self._configpath}'.")

    @property
    def name(self) -> str:
        """ """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """ """
        self._name = str(value)

    def _register(self) -> None:
        """ """
        resourcepath = Settings().resourcepath
        logger.debug(f"Found labctrl setting {resourcepath = }.")
        resource_classes = locate(Path(resourcepath))
        for resource_class in resource_classes:
            yml.register(resource_class)

    def _link(self) -> None:
        """ """
        self._server, self._proxies = server.link()
        for resource_proxy in self._proxies:
            name = resource_proxy.name
            self._resources.append(resource_proxy)
            logger.info(f"Staged remote Resource with {name = }.")

    def __enter__(self) -> Stage:
        """ """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """ """
        self.teardown()

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
                        f"Check the instrument's connection and setup the stage again."
                    )

        if self._server is not None:
            server.unlink(self._server, *self._proxies)

        logger.debug("Tore down the Stage gracefully!")

    def save(self) -> None:
        """ """
        logger.debug(f"Saving the state of staged resources to their configs...")
        for configpath, resources in self._config.items():
            if resources:
                yml.dump(configpath, *resources)

    @property
    def resources(self) -> list[str]:
        """ """
        return [resource.name for resource in self._resources]

    def add(self, *sources: Path | Resource) -> None:
        """ """
        for source in sources:
            if isinstance(source, Resource):  # 'source' is a Resource object
                self._add_resource(source, self._configpath)
            else:  # 'source' is a Path to a yml config file containing Resource objects
                resources = yml.load(source)
                for resource in resources:
                    self._add_resource(resource, source)

    def _add_resource(self, resource: Resource, configpath: Path) -> None:
        """ """
        names = self.resources  # of staged Resources
        name = resource.name  # of Resource to be staged
        if name in names:
            message = (
                f"Unable to stage Resource '{resource}' with {name = } as another "
                f"resource with the same name exists on this stage."
            )
            logger.warning(message)
        else:
            self._resources.append(resource)
            if configpath in self._config:
                self._config[configpath].append(resource)
            else:
                self._config[configpath] = [resource]
            logger.info(f"Staged Resource with {name = }.")

    def remove(self, *names: str) -> None:
        """ """
        staged_resources = {resource.name: resource for resource in self._resources}
        for name in names:
            if name in staged_resources:
                resource = staged_resources[name]
                if resource in self._proxies:  # resource is a Proxy object
                    server.release(resource)
                else:  # resource is a Resource object
                    for config in self._config.values():  # don't save Resource to yml
                        if resource in config:
                            config.remove(resource)
                self._resources.remove(resource)
                logger.info(f"Unstaged resource with {name = }.")
            else:
                logger.warning(f"Resource with '{name = }' does not exist on Stage.")

    def get(self, *names: str) -> Resource | list[Resource]:
        """ """
        if not names:  # return all staged Resources if 'names' is empty
            return self._resources

        staged_resources = {resource.name: resource for resource in self._resources}
        for name in names:
            resources = []
            if name in staged_resources:
                resources.append[staged_resources[name]]
            else:
                message = f"Resource with {name = } does not exist on this stage."
                logger.warning(message)
        return resources if len(resources) != 1 else resources[0]
