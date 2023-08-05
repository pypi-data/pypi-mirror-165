"""Service commands."""

import fire

from ._commands import CommandMixin


class Command(CommandMixin):
    """Service commands."""

    pass


fire.Fire(Command)
