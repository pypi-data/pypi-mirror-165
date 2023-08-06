from concurrent.futures import Future
import logging
from subprocess import CalledProcessError

from watchdog.events import FileSystemEvent, FileSystemEventHandler  # type: ignore

logger = logging.getLogger(__name__)

from ..util.watchdog import event_type_and_file_names_from_event


class LogEventHandled:
    def __init__(self, event: FileSystemEvent, handler: FileSystemEventHandler):
        self.event = event
        self.handler = handler

    @property
    def prefix(self):
        event_type, file_name, _ = event_type_and_file_names_from_event(self.event)
        return f"{event_type} {file_name}"

    @property
    def handler_name(self):
        return (
            self.handler.name
            if hasattr(self.handler, "name")
            else self.handler.__class__.__name__
        )

    def __call__(self, future: Future):
        try:
            _ = future.result()

        except CalledProcessError as e:
            logger.warning(f"{self.prefix}: error in handler {self.handler_name}: {e}")
            logger.error(e)
            stderr = (
                "(None)"
                if e.stderr is None
                else e.stderr.decode("utf8", errors="ignore")
            )
            stdout = (
                "(None)"
                if e.stdout is None
                else e.stdout.decode("utf8", errors="ignore")
            )
            logger.debug(
                "\n".join(
                    [
                        "",
                        "Captured stderr:",
                        "----------------",
                        stderr,
                        "",
                        "Captured stdout:",
                        "----------------",
                        stdout,
                        "",
                    ]
                )
            )

        except Exception as e:
            logger.warning(f"{self.prefix}: error in handler {self.handler_name}: {e}")
            logger.exception(e)
