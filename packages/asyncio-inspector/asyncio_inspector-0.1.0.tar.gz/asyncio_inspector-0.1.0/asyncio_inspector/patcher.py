from asyncio import AbstractEventLoop
from collections import deque
from contextlib import contextmanager
from typing import Any, Iterator, Tuple

from asyncio_inspector.events import ObservableDeque
from asyncio_inspector.stats import BaseStatsTracker


def patch_event_loop_handler_creator(
    event_loop: AbstractEventLoop, stats_tracker: BaseStatsTracker
) -> None:
    obs_deque = ObservableDeque(event_loop._ready)  # type: ignore
    obs_deque.stats_tracker = stats_tracker
    stats_tracker.ready_queue = obs_deque
    event_loop._ready = obs_deque  # type: ignore


def unpatch_event_loop_handler_creator(event_loop: AbstractEventLoop) -> None:
    event_loop._ready = deque(event_loop._ready)  # type: ignore


@contextmanager
def enable_inpection(
    event_loop: AbstractEventLoop,
    *,
    stats_tracker=None,
    reporter=None,
) -> Iterator:
    """Patches the given event loop to enable inspection."""
    stats_tracker, reporter = _wire_reporter_and_stats_tracker(
        stats_tracker, reporter
    )
    patch_event_loop_handler_creator(event_loop, stats_tracker)
    yield stats_tracker
    unpatch_event_loop_handler_creator(event_loop)


def inspect(
    event_loop: AbstractEventLoop, *, stats_tracker=None, reporter=None
) -> BaseStatsTracker:
    stats_tracker, reporter = _wire_reporter_and_stats_tracker(
        stats_tracker, reporter
    )
    patch_event_loop_handler_creator(event_loop, stats_tracker)
    return stats_tracker


def uninspect(event_loop: AbstractEventLoop) -> None:
    unpatch_event_loop_handler_creator(event_loop)


def _wire_reporter_and_stats_tracker(
    stats_tracker, reporter
) -> Tuple[Any, Any]:
    if stats_tracker is None:
        stats_tracker = BaseStatsTracker()
    if reporter is not None:
        reporter.stats_tracker = stats_tracker
    return stats_tracker, reporter
