from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from typing import Optional, Iterable, List, Tuple

from ..adapter import subprocess_
from ..model.command import Command
from ..model.exceptions import ExecutionErrors


class CommandExecutor:
    def __init__(self, notify_logger: Optional[str], **kwargs):
        self.notify_logger = notify_logger
        self._executor = ThreadPoolExecutor(**kwargs)
        self._errors: List[Tuple[str, str, Exception]] = []
        self.logger = logging.getLogger(__name__)

    def submit_commands(self, cmds: Iterable[Tuple[str, Command]], *, prefix: str = ""):
        f_map = {
            self._executor.submit(
                run_command,
                cmd,
                handler,
                notify_logger=self.notify_logger,
                prefix=prefix,
            ): (handler, cmd)
            for (handler, cmd) in cmds
        }
        for f in as_completed(f_map):
            handler, cmd = f_map[f]
            try:
                f.result()
            except Exception as e:
                self.logger.error(
                    f"{prefix}: {handler}: Error running command {cmd.name}"
                )
                self.logger.exception(e)
                self._errors.append((handler, cmd.name, e))

    def shutdown(self):
        self.logger.debug("Shutting down executor")
        self._executor.shutdown(wait=True)
        if len(self._errors) > 0:
            self.logger.debug(f"Shut down executor: {len(self._errors)} errors raised")
            raise ExecutionErrors(self._errors)
        else:
            self.logger.info("Shut down executor.")


def run_command(
    cmd: Command, handler: str, *, notify_logger: Optional[str], prefix: str
):
    logger = logging.getLogger(__name__)
    logger.debug(f"{prefix}: {handler}: Running command {cmd.name}")
    subprocess_.run_command(cmd, notify_logger=notify_logger)
    logger.info(f"{prefix}: {handler}: Ran command {cmd.name}")
