"""Configure."""

import i18n

from logging import getLogger
from typing import Dict, List, Type

from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.logging import LoggingIntegration
from spec import types

from .ext.middleware import HeadersI81n

log = getLogger(__name__)

# Use for service maintenance
# TODO: add modules status later
service_router = types.Router(prefix='/service', tags=['service'])


@service_router.get('/health')
async def health() -> types.JSONResponse:
    """Default health."""
    return types.JSONResponse({'status': 'ok'})


def prepare_routers(
    app: types.App,
    routers: List[types.Router] = None,
    service_routes: bool = True,
):
    """Prepare routers."""

    if service_routes:
        app.router.include_router(service_router)

    if routers:
        for router in routers:
            app.router.include_router(router)


def prepare_openapi(app: types.App, spec: types.Spec):
    """Prepare openapi."""

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = types.get_openapi(
        title=spec.service.name or spec.service.tech_name,
        version=spec.service.tech_version,
        description=spec.service.tech_description,
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema

    return app.openapi_schema


def prepare_i18n(app: types.App, spec: types.Spec):
    """Prepare i18n."""

    if spec.path.i18n.exists():
        i18n.set('filename_format', '{locale}.{format}')
        i18n.set('file_format', 'json')
        i18n.set('enable_memoization', True)

        i18n.set('skip_locale_root_data', True)

        i18n.set('locale', spec.i18n.lang)
        i18n.set('fallback', spec.i18n.lang)
        i18n.set('available_locales', spec.i18n.locales)

        i18n.load_path.append(spec.path.i18n.as_posix())

        app._ = i18n.t


def prepare_sentry(app: types.App, spec: types.Spec):
    """Prepare sentry."""

    if spec.profile.sentry_dsn and spec.status.on_k8s:
        try:
            sentry_init(
                dsn=spec.profile.sentry_dsn,
                server_name=spec.service.tech_name,
                release=spec.service.tech_version,
                environment=spec.environment,
                attach_stacktrace=True,
                integrations=[LoggingIntegration()],
                request_bodies='always',
                with_locals=spec.status.debug,
            )
        except Exception as sentry_exc:
            log.error(f'Prepare sentry: {sentry_exc}', exc_info=True)


def prepare_builtin_middleware(app: types.App, spec: types.Spec):
    """Prepare builtin middleware."""

    app.add_middleware(
        HeadersI81n,
        fallback=spec.i18n.lang,
        allowed=tuple(spec.i18n.all_codes),
    )


def create(
    routers: List[types.Router] = None,
    modules: List[types.Module] = None,
    settings: Type[types.UserSettings] = None,
    kw: Dict = None,
    service_routes: bool = True,
    builtin_middleware: bool = True,
) -> types.App:
    """Create service app."""

    spec = types.load_spec()
    user_settings = settings() if settings else None

    app = types.App(**kw) if kw else types.App()

    app.title = spec.service.name or spec.service.tech_name
    app.version = spec.service.tech_version

    app.spec = spec
    app.settings = user_settings

    prepare_i18n(app=app, spec=spec)
    prepare_sentry(app=app, spec=spec)

    if builtin_middleware:
        prepare_builtin_middleware(app=app, spec=spec)

    prepare_routers(app=app, routers=routers, service_routes=service_routes)
    prepare_openapi(app=app, spec=spec)

    if modules:
        for module in modules:
            try:
                module.inject(app)
            except Exception as _inject_ext:
                log_extra = {'alias': module.name}
                if app.spec.environment.dont_care_secrets():
                    log_extra.update({
                        'spec': spec,
                        'settings': settings,
                        'kw': kw,
                    })
                log.error(
                    f'Inject module {module.name} error: {_inject_ext}',
                    extra=log_extra,
                )
                raise types.exc_type.ModuleException(_inject_ext)

    return app
