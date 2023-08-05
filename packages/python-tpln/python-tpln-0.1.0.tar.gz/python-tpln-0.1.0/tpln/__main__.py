#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
# *****************************************************************************#

import logging
from time import sleep

from .flow import Flow
from .tasks import ShellTask, SleepTask


def example_flow():
    logging.basicConfig(level=logging.INFO, format="### %(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    pipe = Flow()
    pipe.create_task_group("workers", 2)

    preprocess_task = ShellTask(name="Preprocess", dependencies=[], command="ls -la")

    a_task = SleepTask(
        name="A", dependencies=[preprocess_task], duration=10, group_name="workers"
    )
    b_task = SleepTask(
        name="B", dependencies=[preprocess_task], duration=15, group_name="workers"
    )
    c_task = SleepTask(
        name="C", dependencies=[preprocess_task], duration=20, group_name="workers"
    )
    d_task = SleepTask(name="D", dependencies=[a_task], duration=7)

    post_process_task = SleepTask(
        name="post_process", dependencies=[a_task, b_task, c_task, d_task], duration=3
    )

    pipe.register_tasks(
        preprocess_task,
        a_task,
        b_task,
        c_task,
        d_task,
        post_process_task,
    )

    logger.info("Graph iteration order:")
    for i, task in enumerate(pipe.iter_graph(), start=1):
        logger.info(f"{i}. {task}")

    subproc = pipe.visualize()

    sleep(2)

    logger.info("Running Flow")
    pipe.run()

    subproc.join()

if __name__ == "__main__":
    example_flow()
