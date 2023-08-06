from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Optional

import guilogger  # type: ignore

logger = logging.getLogger(__name__)

from .common import LogEventHandled
from ..adapter.handler import Handler
from ..model.config import Config
from ..util.watchdog import event_from_type_and_file_names, EVENT_TYPE_PUSHED


def run(*, config: Config, args, timestamp: float, stop):
    if args.gui:
        _gui_run(config, timestamp, args)
    else:
        _run(config, timestamp, args)


def _run(
    config: Config,
    timestamp: float,
    args,
    log_handler: Optional[logging.Handler] = None,
):
    if log_handler is not None:
        root_logger = logging.getLogger()
        root_logger.addHandler(log_handler)

    handlers = [Handler.from_config(h) for h in config.handlers]
    event = event_from_type_and_file_names(EVENT_TYPE_PUSHED, args.file)
    handler_events = [
        (handler, handler.event_as_observed(event)) for handler in handlers
    ]

    executor = ThreadPoolExecutor(thread_name_prefix="file_trigger")
    f_map = {
        executor.submit(h.dispatch, e): h for (h, e) in handler_events if e is not None
    }
    for future in f_map:
        h = f_map[future]
        future.add_done_callback(LogEventHandled(event, h))

    executor.shutdown(wait=True)

    if hasattr(logger, "done"):
        logger.done()  # type: ignore


_gui_run = guilogger.app(
    level=logging.INFO, title="file-trigger", max_steps=10, close_after=True
)(_run)
