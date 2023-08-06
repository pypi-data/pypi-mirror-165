"""Service."""

from pydantic import BaseSettings as UserSettings  # noqa

from spec import fn, load_spec  # noqa
from spec.types import Any, App, Rpc, Spec  # noqa

from service.log import JSONFormatter, ServiceFormatter  # noqa

from ._configure import create, create_rpc  # noqa
from ._uvicorn import uvicorn_options, uvicorn_run_service


fn.load_env()
spec = load_spec()
