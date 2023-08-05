#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
# *****************************************************************************#

from __future__ import annotations

import asyncio as aio
import logging

from .base_task import Task

_logger = logging.getLogger(__name__)


class SleepTask(Task):
    def __init__(
        self,
        name: str,
        duration: float,
        dependencies: list[Task] | None = None,
        group_name: str | None = None,
    ) -> None:
        super().__init__(name, dependencies, group_name)

        self.duration = duration

    async def main(self):
        
        _logger.info(f"[{self}] Sleeping for {self.duration} seconds...")
        await aio.sleep(self.duration)
        _logger.info(f"[{self}] Slept for {self.duration} seconds.")
