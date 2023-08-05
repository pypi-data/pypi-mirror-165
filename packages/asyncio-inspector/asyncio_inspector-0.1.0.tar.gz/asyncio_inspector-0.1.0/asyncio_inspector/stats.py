from typing import Optional

from sortedcollections import ValueSortedDict

from asyncio_inspector.events import ObservableDeque, ObservableHandle


def invert(x):
    return -x


class BaseStatsTracker:
    """"Basic stats tracker""" ""

    ready_queue: Optional[ObservableDeque]
    call_counts: ValueSortedDict
    total_time: ValueSortedDict
    avg_time: ValueSortedDict
    max_time: ValueSortedDict
    min_time: ValueSortedDict

    def __init__(self, ready_queue: ObservableDeque = None) -> None:
        self.ready_queue = ready_queue
        self.call_counts = ValueSortedDict(invert)
        self.total_time = ValueSortedDict(invert)
        self.avg_time = ValueSortedDict(invert)
        self.max_time = ValueSortedDict(invert)
        self.min_time = ValueSortedDict(invert)

    def track_call(
        self,
        handle: ObservableHandle,
        start_timestamp: int,
        end_timestamp: int,
    ) -> None:
        callback = handle.get_callback()
        if callback not in self.call_counts:
            self.call_counts[callback] = 0
            self.total_time[callback] = 0
            self.avg_time[callback] = 0
            self.max_time[callback] = 0
            self.min_time[callback] = 0

        self.call_counts[callback] += 1
        elapsed_time = end_timestamp - start_timestamp
        self.total_time[callback] += elapsed_time
        if elapsed_time > self.max_time[callback]:
            self.max_time[callback] = elapsed_time
        if elapsed_time < self.min_time[callback]:
            self.min_time[callback] = elapsed_time
        self.avg_time[callback] = (
            self.total_time[callback] / self.call_counts[callback]
        )
