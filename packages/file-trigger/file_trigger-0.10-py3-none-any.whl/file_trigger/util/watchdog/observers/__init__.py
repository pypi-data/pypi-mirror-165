from concurrent.futures import ThreadPoolExecutor, Future
from typing import Optional, Callable

from watchdog.observers import Observer  # type: ignore
from watchdog.observers.api import EventDispatcher  # type: ignore
from watchdog.events import FileSystemEvent, FileSystemEventHandler  # type: ignore

Callback = Callable[[FileSystemEvent, FileSystemEventHandler], Callable[[Future], None]]


class ThreadPoolObserver(Observer):
    def __init__(
        self,
        *args,
        executor: ThreadPoolExecutor,
        done_callback: Optional[Callback] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._executor = executor
        self._done_callback = done_callback

    def dispatch_events(self, event_queue):
        entry = event_queue.get(block=True)
        if entry is EventDispatcher._stop_event:
            return
        event, watch = entry

        with self._lock:
            # To allow unschedule/stop and safe removal of event handlers
            # within event handlers itself, check if the handler is still
            # registered after every dispatch.
            handlers = [
                h
                for h in list(self._handlers.get(watch, []))
                if h
                in self._handlers.get(
                    watch, []
                )  # I don't understand why we need this but ok
            ]
            f_map = {self._executor.submit(h.dispatch, event): h for h in handlers}
            for future in f_map:
                h = f_map[future]
                if self._done_callback is not None:
                    future.add_done_callback(self._done_callback(event, h))

        event_queue.task_done()
