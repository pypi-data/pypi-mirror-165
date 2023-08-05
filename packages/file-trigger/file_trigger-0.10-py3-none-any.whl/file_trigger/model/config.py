from dataclasses import dataclass, field
import json
from typing import Any, Optional, List, Set, Dict

from ..model.command import Command
from ..model.collector import Collector


@dataclass
class FilterConfig:
    root_dir: str
    recursive: bool = False
    case_sensitive: bool = False
    patterns: Optional[Set[str]] = None
    ignore_patterns: Optional[Set[str]] = None
    ignore_directories: bool = False
    events: Optional[Set[str]] = None
    root_dir_aliases: Set[str] = field(default_factory=set)

    def __str__(self) -> str:
        events_str = (
            "None"
            if self.events is None
            else f"{{ {', '.join([e for e in self.events])} }}"
        )
        patterns_str = (
            "None"
            if self.patterns is None
            else f"{{ {', '.join([p for p in self.patterns])} }}"
        )
        ignore_patterns_str = (
            "None"
            if self.ignore_patterns is None
            else f"{{ {', '.join([p for p in self.ignore_patterns])} }}"
        )
        return "\n".join(
            [
                f"  root_dir = {self.root_dir}",
                f"  root_dir_aliases = [{', '.join(self.root_dir_aliases)}]",
                f"  recursive = {self.recursive}",
                f"  case_sensitive = {self.case_sensitive}",
                f"  patterns = {patterns_str}",
                f"  ignore_patterns = {ignore_patterns_str}",
                f"  ignore_directories = {self.ignore_directories}",
                f"  events = {events_str}",
            ]
        )


@dataclass
class HandlerConfig:
    name: str
    template: str
    command: Command
    filter: FilterConfig
    collectors: List[Collector] = field(default_factory=list)
    notify_logger: Optional[str] = None

    def __str__(self) -> str:
        return "\n".join(
            [
                f"{self.name}:",
                "-" * (len(self.name) + 1),
                str(self.filter),
                f"  template = {self.template}",
                f"  notify_logger = {self.notify_logger}",
                "",
                f"{self.name} Command:",
                "-" * (len(self.name) + 9),
                str(self.command),
                "",
                f"{self.name} Collectors:",
                "-" * (len(self.name) + 12),
            ]
            + [str(c) for c in self.collectors]
        )


@dataclass
class Config:
    handlers: List[HandlerConfig]
    filter: Optional[FilterConfig] = None
    notify_logger: Optional[str] = None
    logging: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return "\n".join(
            [
                "Configuration:",
                "==============",
            ]
            + []
            if self.filter is None
            else [str(self.filter)]
            + [
                f"  notify_logger = {self.notify_logger}",
                "",
                "Handlers:",
                "=========",
            ]
            + [str(h) for h in self.handlers]
            + [
                "",
                "Logging:",
                "========",
                json.dumps(self.logging, indent=2),
            ]
        )
