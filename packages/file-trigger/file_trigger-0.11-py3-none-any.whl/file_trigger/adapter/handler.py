import logging
import os.path
import os
from time import time
from typing import Any, Optional, Iterable, List, Set, Dict, cast

from watchdog.events import FileSystemEvent, FileSystemEventHandler  # type: ignore
from watchdog.utils.patterns import match_any_paths  # type: ignore

logger = logging.getLogger(__name__)

from ..adapter.filesys import Matcher
from ..adapter import subprocess_
from ..model.command import Command
from ..model.collector import Collector
from ..model.config import HandlerConfig
from ..util import datetime_
from ..util.watchdog import (
    event_type_and_file_names_from_event,
    EVENT_TYPE_PUSHED,
)


class Handler(FileSystemEventHandler):
    @classmethod
    def from_config(cls, h: HandlerConfig) -> "Handler":
        return cls(
            name=h.name,
            root_dir=h.filter.root_dir,
            template=h.template,
            command=h.command,
            events=h.filter.events,
            collectors=h.collectors,
            recursive=h.filter.recursive,
            case_sensitive=h.filter.case_sensitive,
            patterns=h.filter.patterns,
            ignore_patterns=h.filter.ignore_patterns,
            ignore_directories=h.filter.ignore_directories,
            root_dir_aliases=h.filter.root_dir_aliases,
            notify_logger=h.notify_logger,
        )

    def __init__(
        self,
        *,
        name: str,
        root_dir: str,
        template: str,
        command: Command,
        events: Optional[Set[str]] = None,
        collectors: List[Collector] = [],
        recursive: bool = False,
        case_sensitive: bool = False,
        patterns: Set[str] = set(),
        ignore_patterns: Set[str] = set(),
        ignore_directories: bool = False,
        root_dir_aliases: Set[str] = set(),
        notify_logger: Optional[str] = None,
    ):
        super().__init__()
        self.root_dir = root_dir
        self.recursive = recursive
        self.case_sensitive = case_sensitive
        self.patterns = patterns
        self.ignore_patterns = ignore_patterns
        self.ignore_directories = ignore_directories
        self.name = name
        self.template = template
        self.command = command
        self.events = events
        self.collectors = collectors
        self.root_dir_aliases = root_dir_aliases
        self.notify_logger = notify_logger

    def event_as_observed(self, event: FileSystemEvent) -> Optional[FileSystemEvent]:
        """Note: this mimics watchdog behavior, for push command"""
        src_path: Optional[str] = None
        dest_path: Optional[str] = None
        if event.src_path is not None:
            src_path = os.fsdecode(event.src_path)
        if hasattr(event, "dest_path") and event.dest_path is not None:
            dest_path = os.fsdecode(event.dest_path)

        if src_path is None:
            return None

        root_dir = self.root_dir
        if not os.path.isabs(root_dir):
            root_dir = os.path.abspath(root_dir)

        if not os.path.isabs(src_path):
            src_path = os.path.abspath(src_path)

        src_path_u = unaliased_file(src_path, root_dir, self.root_dir_aliases)
        if not src_path == src_path_u:
            logger.debug(f"Unaliasing file: {src_path} -> {src_path_u}")

        rel_path = relative_path_or_none(src_path_u, root_dir)

        if rel_path is None:
            logger.debug(f"Unaliased file is not under root: {src_path_u}")
            return None

        if not self.recursive and not rel_path == os.path.basename(src_path_u):
            logger.debug(f"Unaliased file is not directly within root: {src_path_u}")
            return None

        return replace_event_paths(event, src_path=src_path_u, dest_path=dest_path)

    def dispatch(self, event: FileSystemEvent):
        ts = time()
        if self.ignore_directories and event.is_directory:
            return

        src_path: Optional[str] = None
        if event.src_path is not None:
            src_path = os.fsdecode(event.src_path)

        if src_path is None:
            return

        logger.debug(f"Received event: {event}")
        rel_src_path = relative_path_or_none(file_path=src_path, root_dir=self.root_dir)

        if rel_src_path is None:
            logger.debug(f"Event ignored because not relative to {self.root_dir}")
            return

        if not self.match_path(src_path):
            logger.debug("Event ignored because file excluded by filter")
            return

        if not self.handles_event_type(event):
            logger.debug("Event ignored because event type excluded by filter")
            return

        event_data = self.event_data(
            event, root_dir=self.root_dir, rel_file_name=rel_src_path, timestamp=ts
        )
        command = self.build_command(rel_src_path, event_data)

        if command is not None:
            logger.debug(
                "%(EVENT_TYPE)s %(RELATIVE_FILE_PATH)s: "
                f"Running command: {command.name}",
                event_data,
            )
            self.run_command(command)
            logger.info(
                "%(EVENT_TYPE)s %(RELATIVE_FILE_PATH)s: "
                f"Ran command: {command.name}",
                event_data,
            )

    def build_command(
        self, rel_file: str, event_data: Dict[str, Any]
    ) -> Optional[Command]:
        captures = self.captures_for_file(rel_file)
        if captures is None:
            logger.debug(
                "%(EVENT_TYPE)s %(RELATIVE_FILE_PATH)s: "
                f"Ignoring because file didn't match template: {rel_file}",
                event_data,
            )
            return None

        logger.debug(
            "%(EVENT_TYPE)s %(RELATIVE_FILE_PATH)s: " "Collecting context data",
            event_data,
        )
        data = self.collected_data(captures, event_data)
        logger.debug(
            "%(EVENT_TYPE)s %(RELATIVE_FILE_PATH)s: " "Collected context data",
            event_data,
        )

        logger.debug(
            (
                "%(EVENT_TYPE)s %(RELATIVE_FILE_PATH)s: "
                "Context data for command:\n  "
                + "\n  ".join([f"{k} = {data[k]!r}" for k in data])
                + "\n"
            ),
            event_data,
        )

        logger.debug(
            "%(EVENT_TYPE)s %(RELATIVE_FILE_PATH)s: "
            f"Rendering command: {self.command.name}",
            event_data,
        )
        command = self.render_command(data)
        logger.debug(
            "%(EVENT_TYPE)s %(RELATIVE_FILE_PATH)s: "
            f"Rendered command: {self.command.name}",
            event_data,
        )
        return command

    def match_path(self, file_path: str) -> bool:
        return cast(
            bool,
            match_any_paths(
                [file_path], self.patterns, self.ignore_patterns, self.case_sensitive
            ),
        )

    def handles_event_type(self, event: FileSystemEvent) -> bool:
        event_type, _, _ = event_type_and_file_names_from_event(event)
        return (
            event_type == EVENT_TYPE_PUSHED
            or self.events is None
            or event_type in self.events
        )

    def event_data(
        self,
        event: FileSystemEvent,
        *,
        root_dir: str,
        rel_file_name: str,
        timestamp: float,
    ) -> Dict[str, Any]:
        event_type, file_name, _ = event_type_and_file_names_from_event(event)
        data: Dict[str, Any] = {}
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
        return data

    def captures_for_file(self, file_name: str) -> Optional[Dict[str, str]]:
        return Matcher(self.template).match(file_name)

    def collected_data(
        self, captures: Dict[str, str], event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        data.update(captures)
        data.update(event_data)
        for collector in self.collectors:
            logger.debug(f"Collecting {collector.name} for handler {self.name}", data)
            data[collector.name] = collector.collect(data)
            logger.debug(f"Collected {collector.name} for handler {self.name}", data)
        return data

    def render_command(self, data) -> Command:
        c = self.command
        return Command(
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

    def run_command(self, command: Command):
        subprocess_.run_command(command, notify_logger=self.notify_logger)


def unaliased_file(file: str, root_dir: str, aliases: Iterable[str]) -> str:
    file_lc = file.lower()
    try:
        return next(
            root_dir + file.replace(alias, "", 1)
            for alias in aliases
            if file_lc.startswith(alias.lower())
        )
    except StopIteration:
        return file


def replace_event_paths(
    event: FileSystemEvent, src_path: str, dest_path: Optional[str]
) -> FileSystemEvent:
    if hasattr(event, "dest_path"):
        return event.__class__(src_path=src_path, dest_path=dest_path)
    else:
        return event.__class__(src_path=src_path)


def relative_path_or_none(file_path: str, root_dir: str):
    try:
        return os.path.relpath(file_path, root_dir)
    except ValueError:
        return None
