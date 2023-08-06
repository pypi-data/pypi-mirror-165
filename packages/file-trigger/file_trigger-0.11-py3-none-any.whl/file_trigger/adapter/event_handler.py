import logging
import os.path
from time import time
from typing import Any, Optional, Dict, Tuple, List

from watchdog.events import (
    FileSystemEvent,
    PatternMatchingEventHandler,
    EVENT_TYPE_CREATED,
    EVENT_TYPE_MODIFIED,
)  # type: ignore

from ..adapter.executor import CommandExecutor
from ..adapter.filesys import Matcher
from ..model.command import Command
from ..model.config import Config, HandlerConfig
from ..util import datetime_
from ..util.watchdog import event_type_and_file_names_from_event


class EventHandler(PatternMatchingEventHandler):
    def __init__(self, config: Config, executor: CommandExecutor):
        super().__init__(
            patterns=config.patterns,
            ignore_patterns=config.ignore_patterns,
            ignore_directories=config.ignore_directories,
        )
        self.last_event: Optional[FileSystemEvent] = None
        self.last_timestamp: Optional[float] = None
        self.config: Config = config
        self._executor: CommandExecutor = executor

    def on_any_event(self, event: FileSystemEvent):
        ts = time()
        logger = logging.getLogger(__name__)
        logger.debug(f"Received event: {event}")
        if self.ignore_event(event=event, timestamp=ts):
            logger.debug(f"Ignored event as duplicate: {event}")
        else:
            self.handle_event_on_thread(event=event, timestamp=ts)
        self.last_event = event
        self.last_timestamp = ts

    def ignore_event(self, event: FileSystemEvent, timestamp: float) -> bool:
        """filter out duplicate-ish events thrown up by Windows"""
        if self.last_timestamp is None or self.last_event is None:
            return False

        if (
            event == self.last_event
            and event.src_path == self.last_event.src_path
            and (timestamp - self.last_timestamp < 1)
        ):
            return True

        return False

    def handle_event_on_thread(self, event: FileSystemEvent, timestamp: float):
        prefix = f"{event.event_type.upper()} {event.src_path}"
        self._executor.submit_commands(
            commands_triggered_by_handlers(
                self.config,
                event=event,
                last_event=self.last_event,
                prefix=prefix,
                timestamp=timestamp,
                last_timestamp=self.last_timestamp,
            ),
            prefix=prefix,
        )


def commands_triggered_by_handlers(
    config: Config,
    *,
    event: FileSystemEvent,
    last_event: Optional[FileSystemEvent],
    prefix: str,
    timestamp: float,
    last_timestamp: Optional[float],
) -> List[Tuple[str, Command]]:
    logger = logging.getLogger(__name__)

    cmds: List[Tuple[str, Command]] = []
    rel_file = relative_file_name_for_event(config.root_dir, event)
    if rel_file is None:
        logger.debug(f"{prefix}: Ignoring because file not relative to root")
        return cmds

    for h in config.handlers:
        if ignore_handler_for_event_type(h, event):
            logger.debug(f"{prefix}: Ignoring event for handler {h.name}")
            continue

        if ignore_handler_for_event_sequence(
            h,
            event=event,
            last_event=last_event,
            timestamp=timestamp,
            last_timestamp=last_timestamp,
        ):
            logger.debug(f"{prefix}: Ignoring event sequence for handler {h.name}")
            continue

        captures = handler_captures_for_file(h, rel_file)
        if captures is None:
            logger.debug(
                f"{prefix}: Ignoring handler {h.name} because file didn't match template"
            )
            continue

        matched_cmds = render_commands(
            h,
            event=event,
            root_dir=config.root_dir,
            rel_file_name=rel_file,
            captures=captures,
            timestamp=timestamp,
        )
        n_cmds = len(matched_cmds)
        if n_cmds == 0:
            logger.warning(
                f"{prefix}: Matched handler {h.name} has no commands defined"
            )
        else:
            logger.info(
                f"{prefix}: Handled by {h.name}: "
                f"triggering {n_cmds} command{'s' if n_cmds>1 else ''}"
            )
        for cmd in matched_cmds:
            cmds.append((h.name, cmd))
    return cmds


def render_commands(
    handler: HandlerConfig,
    *,
    event: FileSystemEvent,
    captures: Dict[str, str],
    rel_file_name: str,
    root_dir: str,
    timestamp: float,
) -> List[Command]:
    event_type, file_name, _ = event_type_and_file_names_from_event(event)

    data: Dict[str, Any] = {}
    for k in captures:
        data[k] = captures[k]
    data["ROOT_DIR"] = root_dir
    data["TIMESTAMP_POSIX"] = timestamp
    data["TIMESTAMP"] = datetime_.from_posix(timestamp)
    data["TIMESTAMP_UTC"] = datetime_.utc_from_posix(timestamp)
    data["FILE_PATH"] = file_name
    data["RELATIVE_FILE_PATH"] = rel_file_name
    data["DIR_PATH"] = os.path.dirname(file_name)
    data["RELATIVE_DIR_PATH"] = os.path.dirname(rel_file_name)
    data["FILE_NAME"] = os.path.basename(file_name)
    data["FILE_EXT"] = os.path.splitext(file_name)[1][1:]
    data["EVENT_TYPE"] = event_type

    try:
        return [
            Command(
                name=c.name,
                command=[token.format(**data) for token in c.command],
                cwd=None if c.cwd is None else c.cwd.format(**data),
                shell=c.shell,
                timeout=c.timeout,
                error_rc=c.error_rc,
                warning_rc=c.warning_rc,
                notify=(
                    None
                    if c.notify is None
                    else {k: c.notify[k].format(**data) for k in c.notify}
                ),
            )
            for c in handler.commands
        ]

    except KeyError as e:
        raise ValueError(f"Unknown variable in command: {e}")


def relative_file_name_for_event(
    root_dir: str, event: FileSystemEvent
) -> Optional[str]:
    _, file, _ = event_type_and_file_names_from_event(event)
    try:
        return os.path.relpath(file, root_dir)
    except ValueError:
        return None


def ignore_handler_for_event_type(
    handler: HandlerConfig, event: FileSystemEvent
) -> bool:
    event_type, _, _ = event_type_and_file_names_from_event(event)
    return handler.events is not None and event_type not in handler.events


def ignore_handler_for_event_sequence(
    handler: HandlerConfig,
    *,
    event: FileSystemEvent,
    last_event: Optional[FileSystemEvent],
    timestamp: float,
    last_timestamp: Optional[float],
) -> bool:
    if last_event is None or last_timestamp is None:
        return False
    event_type, file, _ = event_type_and_file_names_from_event(event)
    last_event_type, last_file, _ = event_type_and_file_names_from_event(last_event)
    return (
        file == last_file
        and (timestamp - last_timestamp < 1)
        and event_type == EVENT_TYPE_MODIFIED
        and last_event_type == EVENT_TYPE_CREATED
        and (
            handler.events is None
            or (
                EVENT_TYPE_MODIFIED in handler.events
                and EVENT_TYPE_CREATED in handler.events
            )
        )
    )


def handler_captures_for_file(handler: HandlerConfig, file_name: str) -> Dict[str, str]:
    return Matcher(handler.template).match(file_name)
