"""Command helpers."""

import subprocess

from typing import Sequence
from logging import getLogger

from spec import fn, loader

from ._uvicorn import uvicorn_run_service


log = getLogger(__name__)


def execute(command: Sequence[str]) -> bool:
    """Execute."""
    try:
        if subprocess.call(command) == 0:
            return True
    except Exception as _any_exc:
        log.error(f'Cant execute [{" ".join(command)}] cause: {_any_exc}')
    return False


def create_locale_dot_gen() -> None:
    """Create locale.gen file."""
    params = loader.load_i18n()

    with open(fn.locale_dot_gen().as_posix(), 'w') as gen_file:
        for locale in params.locales:
            gen_file.write(f'{locale}.UTF-8 UTF-8\n')


class CommandMixin():
    """Base command mixin."""

    @staticmethod
    def run() -> None:
        """Run service."""
        uvicorn_run_service()

    @staticmethod
    def linter() -> None:
        """Linter runner."""
        execute(['flakehell', 'lint'])

    @staticmethod
    def tests() -> None:
        """Pytest runner."""
        execute(['pytest', 'tests'])

    @staticmethod
    def locale_gen() -> None:
        """Export locale.gen locales file from spec."""
        create_locale_dot_gen()

    @staticmethod
    def migrate():
        """Alembic migrate."""
        execute(['python', '-m', 'alembic', 'upgrade', 'head'])

    @staticmethod
    def make_migration(name: str):
        """Alembic make migration."""
        execute(['python', '-m', 'alembic', 'revision', '-m', name])

    @staticmethod
    def rollback(name: str):
        """Alembic rollback to exact revision."""
        execute(['python', '-m', 'alembic', 'downgrade', name])
