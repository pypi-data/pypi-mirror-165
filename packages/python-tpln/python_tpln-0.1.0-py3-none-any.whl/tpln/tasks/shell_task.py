#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
# *****************************************************************************#

from __future__ import annotations

import asyncio as aio
import logging

from .base_task import Task

_logger = logging.getLogger(__name__)


class ShellTask(Task):
    def __init__(
        self,
        name: str,
        command: str,
        dependencies: list[Task] | None = None,
    ) -> None:
        super().__init__(name, dependencies)

        self.cmd = command

    async def main(self):
        _logger.info(f"[{self}] Running command {self.cmd}...")

        proc = await aio.create_subprocess_shell(self.cmd)
        await proc.wait()

        level = logging.INFO if proc.returncode == 0 else logging.ERROR
        _logger.log(
            msg=f"[{self}] Command {self.cmd} exited with code {proc.returncode}.",
            level=level,
        )
