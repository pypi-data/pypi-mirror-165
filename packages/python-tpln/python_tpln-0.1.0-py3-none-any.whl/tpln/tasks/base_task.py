#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
# *****************************************************************************#

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from .flow import Flow


class TaskState(IntEnum):
    pending = auto()
    running = auto()
    done = auto()


class Task(ABC):
    def __init__(
        self,
        name: str,
        dependencies: list["Task"] | None = None,
        group_name: str | None = None,
    ) -> None:
        """Initialize a task with a name, a list of dependencies and a task_group name"""

        self.id = uuid4()
        self.name = name
        self.dependencies = [] if dependencies is None else dependencies
        self.group_name = group_name
        self.state = TaskState.pending

    async def run(self, pipe: Flow, **kwargs):
        """
        This method runs the task, taking care of setup and teardown between
        which we call the main() method.
        """

        if self.group_name:
            await pipe.task_groups[self.group_name].acquire()

        self.state = TaskState.running

        await self.main(**kwargs)

        self.state = TaskState.done

        if self.group_name:
            pipe.task_groups[self.group_name].release()

    @abstractmethod
    async def main(self, **kwargs):
        """User-overriden method in which we define what the task does"""
        ...

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"{self.name}<{classname}>"
