import time
from abc import ABCMeta, abstractmethod
from logging import Logger
from threading import Thread
from typing import Optional

from asyncio_inspector.stats import BaseStatsTracker


class BaseReporter(metaclass=ABCMeta):
    stats_tracker: Optional[BaseStatsTracker] = None

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...


class LoggerReporter(Thread, BaseReporter):
    """Reporter that returns"""

    logger: Logger
    running: bool
    sleep_period: int
    show_top_n: int

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self.logger = logger
        self.running = True
        self.sleep_period = 1
        self.daemon = True
        self.show_top_n = 10

    def _get_line(self, data) -> str:
        """ "Returns the top-n itens in data as a string"""
        return " | ".join(
            f"{k}: {v}" for k, v in data.items()[: self.show_top_n]
        )

    def run(self) -> None:
        while self.running:
            if self.stats_tracker is None:
                time.sleep(self.sleep_period)
                continue
            ready_queue_size = (
                len(self.stats_tracker.ready_queue)
                if self.stats_tracker.ready_queue is not None
                else 0
            )
            fmt = self._get_line
            self.logger.debug(
                f"Queue size: {ready_queue_size}\n"
                f"Call counts: {fmt(self.stats_tracker.call_counts)}\n"
                f"Max exec times: {fmt(self.stats_tracker.max_time)}\n"
                f"Total exec times: {fmt(self.stats_tracker.total_time)}\n"
                f"Avg exec times: {fmt(self.stats_tracker.avg_time)}"
            )
            time.sleep(self.sleep_period)

    def start(self) -> None:
        super().start()

    def stop(self):
        self.running = False
