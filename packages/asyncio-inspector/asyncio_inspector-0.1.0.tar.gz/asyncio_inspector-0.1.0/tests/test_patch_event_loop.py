import asyncio

from asyncio_inspector import enable_inpection, inspect, uninspect
from asyncio_inspector.events import ObservableDeque


async def do_nothing() -> int:
    """Async function that only sleeps(0) and return"""
    await asyncio.sleep(0)
    return 1


def test_patch_even_loop() -> None:
    """Makes sure we can patch an event loop and track call_soon calls"""
    loop = asyncio.get_event_loop()
    try:
        stats_tracker = inspect(loop)
        assert isinstance(loop._ready, ObservableDeque)
        loop.call_soon(do_nothing)
        loop.call_soon(loop.stop)
        loop.run_forever()
    finally:
        uninspect(loop)
        assert not isinstance(loop._ready, ObservableDeque)
    assert "do_nothing" in stats_tracker.call_counts
    assert stats_tracker.call_counts["do_nothing"] == 1


def test_patch_event_loop_context_manager() -> None:
    """ "Makes sure we can patch even loop with a context manager"""
    loop = asyncio.get_event_loop()
    with enable_inpection(loop) as stats_tracker:
        assert isinstance(loop._ready, ObservableDeque)
        loop.call_soon(do_nothing)
        loop.call_soon(loop.stop)
        loop.run_forever()

    assert "do_nothing" in stats_tracker.call_counts
    assert stats_tracker.call_counts["do_nothing"] == 1
    assert not isinstance(loop._ready, ObservableDeque)


def test_patch_event_loop_from_within() -> None:
    async def main():
        loop = asyncio.get_event_loop()
        with enable_inpection(loop) as stats_tracker:
            assert isinstance(loop._ready, ObservableDeque)
            await do_nothing()
        assert not isinstance(loop._ready, ObservableDeque)
        return stats_tracker

    stats_tracker = asyncio.run(main())
    method_name = "test_patch_event_loop_from_within.<locals>.main"
    assert method_name in stats_tracker.call_counts
    assert stats_tracker.call_counts[method_name] == 1
