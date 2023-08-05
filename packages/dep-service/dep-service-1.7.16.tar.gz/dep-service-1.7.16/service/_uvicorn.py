"""Uvicorn runner."""

import uvicorn

from typing import Dict
from spec import Spec, load_spec, fn
from logging import getLogger

fn.load_env()

log = getLogger(__name__)


def uvicorn_options(spec: Spec) -> Dict:
    """Uvicorn options by spec."""

    options = {
        'app': spec.service.entrypoint,
        'host': spec.service.uri.host,
        'port': spec.service.uri.port,
        'use_colors': not spec.status.on_k8s,
        'log_level': spec.profile.log_level.lower(),
        'access_log': spec.status.debug,
        'workers': spec.policies.service_workers,
        'lifespan': 'auto',
    }

    # TODO: Reload dir for non k8s

    if spec.path.log_config_path and spec.path.log_config_path.exists():
        options['log_config'] = spec.path.log_config_name

    return options


def uvicorn_run_service():
    """Run app with uvicorn by spec."""
    spec = load_spec()
    options = uvicorn_options(spec)

    uvicorn.run(**options)
