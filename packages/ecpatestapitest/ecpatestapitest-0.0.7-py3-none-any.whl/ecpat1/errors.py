"""Define package errors."""


class EcowittError(Exception):
    """Define a base error."""

    pass


class RequestError(EcowittError):
    """Define an error related to invalid requests."""

    pass


class WebsocketError(EcowittError):
    """Define an error related to generic websocket errors."""

    pass
