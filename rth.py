# routine host
from __future__ import annotations

import abc
import time
import threading
import logging

from . import app


class Routine(metaclass=abc.ABCMeta):
    delay: int = 0

    duration: int = 60

    hard: bool = False
    """是否硬计时"""

    ap: app.Application

    def __init__(self, ap: app.Application, delay: int = 0, duration: int = 60, hard: bool = False):
        self.delay = delay
        self.duration = duration
        self.hard = hard
        self.ap = ap

    def loop(self):
        time.sleep(self.delay)

        while True:
            start_time = time.time()

            self.run()

            end_time = time.time()

            spent = end_time - start_time

            if self.hard:
                if spent < self.duration:
                    time.sleep(self.duration - (end_time - start_time))
                else:
                    skipped_periods = int(spent / self.duration)
                    time.sleep(self.duration * (skipped_periods + 1) - spent)
            else:
                time.sleep(self.duration)

    @abc.abstractmethod
    def run(self):
        pass


class RoutineHost:

    routines: list[Routine]

    threads: list[threading.Thread]

    def __init__(self, routines: list[Routine]):
        self.routines = routines
        self.threads = []

    def schedule(self):
        logging.info("[MCBot] 启动定时任务..")
        for routine in self.routines:
            thr = threading.Thread(target=routine.loop)
            thr.start()
            self.threads.append(thr)
