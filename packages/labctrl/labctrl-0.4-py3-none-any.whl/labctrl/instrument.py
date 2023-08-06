""" """

from typing import Any

from labctrl.logger import logger
from labctrl.resource import Resource


class ConnectionError(Exception):
    """ """


class Instrument(Resource):
    """ """

    def __init__(self, id: Any, **parameters) -> None:
        """ """
        self._id = id
        self.connect()
        super().__init__(**parameters)

    def __repr__(self) -> str:
        """ """
        return f"{self.__class__.__name__} #{self._id}"

    @property
    def id(self) -> Any:
        """ """
        return self._id

    @property
    def status(self) -> bool:
        """ """
        raise NotImplementedError("Subclasses must implement 'status'.")

    def connect(self) -> None:
        """ """
        raise NotImplementedError("Subclasses must implement 'connect()'.")

    def disconnect(self) -> None:
        """ """
        raise NotImplementedError("Subclasses must implement 'disconnect()'.")

    def configure(self, **parameters) -> None:
        """ """
        if not self.status:
            message = f"Unable to configure {self} as it has disconnected. "
            logger.error(message)
            raise ConnectionError(message)

        super().configure(**parameters)

    def snapshot(self) -> dict[str, Any]:
        """ """
        if not self.status:
            message = f"{self} has disconnected, returning a minimal snapshot..."
            logger.error(message)
            return {"id": self.id, "name": self.name}

        return super().snapshot()
