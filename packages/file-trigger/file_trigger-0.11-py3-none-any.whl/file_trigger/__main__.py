from argparse import ArgumentParser
import logging.config
import logging
import sys
from time import time
from threading import Event

from .adapter import config_file
from .model.config import Config


def main(args=sys.argv[1:], stop: Event = Event()):
    t = time()
    program = ArgumentParser(description="Trigger actions on file changes")
    program.add_argument(
        "-c",
        "--config",
        default=f"{sys.argv[0]}.toml",
        help="Configuration file (TOML)",
    )
    commands = program.add_subparsers(help="commands")
    build_push_parser(commands, [])
    build_watch_parser(commands, [])

    args = program.parse_args(args)
    config = config_file.parse_file(args.config)
    logging.config.dictConfig(config.logging)

    logger = logging.getLogger(__name__)
    logger.info(f"Using configuration file: {args.config}")
    logger.debug(f"Arguments:\n  {args}")
    logger.debug(f"Configuration:\n  {config}")

    try:
        args.func(config=config, args=args, timestamp=t, stop=stop)
    except Exception as e:
        logger.exception(e)
        raise e


def build_push_parser(root, parents):
    cmd = root.add_parser(
        "push",
        description="Push single file change through trigger",
        parents=parents,
    )
    cmd.add_argument("--gui", action="store_true", help="Show GUI log")
    cmd.add_argument(
        "--no-gui", action="store_false", dest="gui", help="Don't show GUI log"
    )
    cmd.add_argument("file", help="Path to file")
    cmd.set_defaults(gui=False, func=push_run)


def build_watch_parser(root, parents):
    cmd = root.add_parser(
        "watch",
        description="Trigger on watched file changes",
        parents=parents,
    )
    cmd.set_defaults(func=watch_run)


# Note: late imports to avoid initializing loggers until after argument parsing


def push_run(config: Config, args, timestamp: float, stop: Event):
    from file_trigger.command import push

    return push.run(config=config, args=args, timestamp=timestamp, stop=stop)


def watch_run(config: Config, args, timestamp: float, stop: Event):
    from file_trigger.command import watch

    return watch.run(config=config, args=args, timestamp=timestamp, stop=stop)
