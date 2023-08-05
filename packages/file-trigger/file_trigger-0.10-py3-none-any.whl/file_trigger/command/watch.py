from concurrent.futures import ThreadPoolExecutor
import logging
from time import sleep
from threading import Event

logger = logging.getLogger(__name__)

from .common import LogEventHandled
from ..adapter.handler import Handler
from ..model.config import Config
from ..util.watchdog.observers import ThreadPoolObserver, Observer  # type: ignore


def run(*, config: Config, args, timestamp: float, stop: Event):
    executor = ThreadPoolExecutor(thread_name_prefix="file_trigger")
    observer = ThreadPoolObserver(executor=executor, done_callback=LogEventHandled)
    for h in config.handlers:
        logger.debug(f"Watch scheduling handler {h.name} on {h.filter.root_dir}")
        observer.schedule(
            Handler.from_config(h), h.filter.root_dir, recursive=h.filter.recursive
        )
        logger.info(f"Watch scheduled handler {h.name} on {h.filter.root_dir}")

    logger.debug("Watch starting")
    observer.start()
    logger.info("Watch started")
    try:
        main_loop(observer, stop)

    except Exception as e:
        """
        Note: this is an error handler of last resort, most errors are handled
        by LogEventHandled instances.
        """
        logger.exception(e)
        raise e

    finally:
        logger.debug("Watch stopping")
        observer.stop()
        observer.join()
        logger.info("Watch stopped")
        logger.debug("Executor waiting for jobs to finish and shutting down")
        executor.shutdown()
        logger.info("Executor shut down")


def main_loop(observer: Observer, stop: Event):
    try:
        while not stop.is_set():
            sleep(1)
    except KeyboardInterrupt:
        stop.set()
    finally:
        if stop.is_set():
            observer.stop()
