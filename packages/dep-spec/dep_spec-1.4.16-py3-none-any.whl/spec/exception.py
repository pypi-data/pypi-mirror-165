"""Spec exceptions."""


class ServiceException(Exception):
    """Service exception."""

    pass


class ASGIException(ServiceException):
    """ASGI Exception."""

    pass


class SpecException(ServiceException):
    """Spec exception."""

    pass


class PyProjectException(SpecException):
    """Pyproject spec exception."""

    pass


class TaskException(ServiceException):
    """Service task exception."""

    pass


class RequestException(ServiceException):
    """Service external request exception."""

    pass


class UnknownException(ServiceException):
    """Service unknown exception."""

    pass


class ModuleException(ServiceException):
    """Service module exception."""

    pass
