import os.path

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib  # type: ignore
from typing import Any, Optional, Iterable, List, Dict, Set, cast

from ..model.config import Config, FilterConfig, HandlerConfig, Command
from ..model.collector import Collector
from ..util.watchdog import event_type_from_string
from ..util import dict_
from ..util.dataclasses_ import nonoptional_noniterable_fields, nonoptional_fields
from ..util.bool_ import strict_bool
from ..util.importlib_ import import_module_class

TOP_LEVEL_KEY = "file-trigger"
LOGGING_KEY = "logging"


def parse_file(file: str) -> Config:
    raw: Dict[str, Any] = {}
    with open(file, "rb") as f:
        raw = tomllib.load(f)

    assert_config_keys(raw, [TOP_LEVEL_KEY], [LOGGING_KEY])

    logging_data = raw[LOGGING_KEY]
    if not isinstance(logging_data, dict):
        raise ValueError(f"Unknown logging configuration: {logging_data}")

    data = raw[TOP_LEVEL_KEY]
    if not isinstance(data, dict):
        raise ValueError(f"Unknown top-level configuration: {data}")

    assert_config_keys(
        raw,
        *[
            [TOP_LEVEL_KEY, k]
            for k in nonoptional_noniterable_fields(Config)
            if not k == "logging"
        ],
    )

    default_filter = parse_filter(raw, [TOP_LEVEL_KEY]) if "root_dir" in data else None
    notify_logger = data.get("notify_logger", None)
    return Config(
        handlers=parse_handlers(
            raw,
            [TOP_LEVEL_KEY, "handler"],
            default_filter=default_filter,
            default_notify_logger=None if notify_logger is None else str(notify_logger),
        ),
        filter=default_filter,
        notify_logger=None if notify_logger is None else str(notify_logger),
        logging=logging_data,
    )


def parse_filter(data: Dict[str, Any], keys: List[str]) -> FilterConfig:
    assert_config_keys(
        data,
        *[keys + [field] for field in nonoptional_noniterable_fields(FilterConfig)],
    )
    filter_data = dict_.path(keys, data)
    empty_root_dir_aliases: Set[str] = set()
    recursive = filter_data.get("recursive", False)
    case_sensitive = filter_data.get("case_sensitive", False)
    patterns = filter_data.get("patterns", None)
    ignore_patterns = filter_data.get("ignore_patterns", None)
    ignore_directories = filter_data.get("ignore_directories", False)
    events = filter_data.get("events", None)
    root_dir_aliases = filter_data.get("root_dir_aliases", empty_root_dir_aliases)

    return FilterConfig(
        root_dir=parse_root_dir(str(filter_data["root_dir"])),
        recursive=strict_bool("recursive", recursive),
        case_sensitive=strict_bool("case_sensitive", case_sensitive),
        patterns=None if patterns is None else set(str(p) for p in patterns),
        ignore_patterns=(
            None if ignore_patterns is None else set(str(p) for p in ignore_patterns)
        ),
        ignore_directories=strict_bool("ignore_directories", ignore_directories),
        events=(
            None
            if events is None
            else set(event_type_from_string(str(x)) for x in events)
        ),
        root_dir_aliases=set(str(a) for a in root_dir_aliases),
    )


def parse_root_dir(raw: str) -> str:
    return os.path.abspath(raw)


def parse_handlers(
    data: Dict[str, Any],
    keys: List[str],
    default_filter: Optional[FilterConfig],
    default_notify_logger: Optional[str],
) -> List[HandlerConfig]:
    handlers_data = dict_.path(keys, data)
    if not isinstance(handlers_data, dict):
        raise ValueError(f"Unknown handlers configuration: {handlers_data}")
    return [
        parse_handler(
            data,
            keys,
            k,
            default_filter=default_filter,
            default_notify_logger=default_notify_logger,
        )
        for k in handlers_data
    ]


def parse_handler(
    data: Dict[str, Any],
    keys: List[str],
    name: str,
    default_filter: Optional[FilterConfig],
    default_notify_logger: Optional[str],
) -> HandlerConfig:
    assert_config_keys(
        data,
        *[
            keys + [name, field]
            for field in nonoptional_noniterable_fields(HandlerConfig)
            if not field == "name" and not field == "filter"
        ],
    )
    handler_data = dict_.path(keys + [name], data)
    if not isinstance(handler_data, dict):
        raise ValueError(f"Unknown handler configuration {name}: {handler_data}")

    filter_name: Optional[str] = handler_data.get("filter", None)
    collector_names: List[str] = handler_data.get("collectors", [])
    notify_logger = handler_data.get("notify_logger", None)

    filter: FilterConfig
    if filter_name is not None:
        filter = parse_filter(data, [TOP_LEVEL_KEY, "filter", str(filter_name)])
    else:
        if default_filter is None:
            raise ValueError(
                f"Either a default filter, or a handler-specific filter must be specified: {name}"
            )
        filter = default_filter

    return HandlerConfig(
        name=name,
        template=str(handler_data["template"]),
        command=parse_command(
            data, [TOP_LEVEL_KEY, "command"], handler_data["command"]
        ),
        collectors=parse_collectors(data, [TOP_LEVEL_KEY], collector_names),
        filter=filter,
        notify_logger=default_notify_logger
        if notify_logger is None
        else str(notify_logger),
    )


def parse_command(data: Dict[str, Any], keys: List[str], name: str) -> Command:
    assert_config_keys(
        data,
        *[
            keys + [name, field]
            for field in nonoptional_fields(Command)
            if not field == "name"
        ],
    )
    command_data = dict_.path(keys + [name], data)
    if not isinstance(command_data, dict):
        raise ValueError(f"Unknown command configuration {name}: {command_data}")
    cwd = command_data.get("cwd", None)
    shell = command_data.get("shell", None)
    timeout = command_data.get("timeout", None)
    error_rc = command_data.get("error_rc", None)
    warning_rc = command_data.get("warning_rc", None)
    notify = command_data.get("notify", None)
    params: Dict[str, Any] = {
        "name": name,
        "command": list(str(x) for x in command_data["command"]),
        "cwd": None if cwd is None else str(cwd),
    }
    if shell is not None:
        params["shell"] = strict_bool("shell", shell)
    if timeout is not None:
        params["timeout"] = float(timeout)
    if error_rc is not None:
        params["error_rc"] = int(error_rc)
    if warning_rc is not None:
        params["warning_rc"] = int(warning_rc)
    if notify is not None:
        params["notify"] = dict_.strict_dict("notify", notify)

    return Command(**params)  # type: ignore


def parse_collectors(
    data: Dict[str, Any], keys: List[str], collector_names: List[str]
) -> List[Collector]:
    empty: List[Collector] = []
    parent_data = dict_.path(keys, data)
    if not "collector" in parent_data:
        return empty
    collectors_data = parent_data["collector"]
    if not isinstance(collectors_data, dict):
        raise ValueError(f"Unknown collectors configuration: {collectors_data}")
    return [parse_collector(data, keys, k) for k in collector_names]


def parse_collector(data: Dict[str, Any], keys: List[str], name: str) -> Collector:
    assert_config_keys(data, keys + ["collector", name, "class"])
    collector_data = dict_.path(keys + ["collector", name], data)
    if not isinstance(collector_data, dict):
        raise ValueError(f"Unknown collector configuration {name}: {collector_data}")

    klass = import_module_class(str(collector_data["class"]))
    collector = klass(
        **{k: collector_data[k] for k in collector_data if not k == "class"}
    )
    collector.name = name
    return cast(Collector, collector)


def assert_config_keys(d: Dict[str, Any], *paths: Iterable[str]) -> None:
    missings = []
    for path in paths:
        try:
            v = dict_.path(path, d)
            if v is None:
                missings.append(path)
        except KeyError:
            missings.append(path)
    if len(missings) == 1:
        msg = ".".join(missings[0])
        raise ValueError(f"Missing configuration: {msg}")
    if len(missings) > 1:
        msg = "\n  ".join([".".join(m) for m in missings])
        raise ValueError(f"Missing configurations:\n  {msg}")
