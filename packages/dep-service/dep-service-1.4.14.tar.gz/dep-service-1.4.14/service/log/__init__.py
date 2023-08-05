from logging import getLogger as new_log  # noqa
from .formatter import JSONFormatter, ServiceFormatter


__all__ = (
    'new_log',
    'JSONFormatter',
    'ServiceFormatter',
)
