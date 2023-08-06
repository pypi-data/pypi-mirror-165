import logging
import subprocess
from time import time
from typing import Optional

from ..model.command import Command


def run_command(
    cmd: Command, *, notify_logger: Optional[str]
) -> subprocess.CompletedProcess:
    logger = logging.getLogger(__name__)
    notifier = None if notify_logger is None else logging.getLogger(notify_logger)

    ret: subprocess.CompletedProcess

    logger.debug(
        f"""Running command:
  cmd     = {cmd.command}
  cwd     = {cmd.cwd}
  shell   = {cmd.shell}
  timeout = {cmd.timeout}
    """
    )
    with subprocess.Popen(
        cmd.command,
        cwd=cmd.cwd,
        shell=cmd.shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as p:
        t0 = time()
        if notifier is not None:
            notifier.info(f"Starting {cmd.name}", start_notify_data(cmd, p, t0))

        adj_timeout = (
            None if cmd.timeout is None else max(0, cmd.timeout - (time() - t0))
        )
        try:
            stdout, stderr = p.communicate(timeout=adj_timeout)
        except subprocess.TimeoutExpired as e:
            t1 = time()
            if notifier is not None:
                notifier.error(
                    f"Timeout in {cmd.name}", timeout_notify_data(cmd, p, t0, t1)
                )
            p.kill()  # note: kill + final communicate recommended after timeout
            p.communicate()
            raise e

        t1 = time()
        rc = abs(p.returncode)
        if rc >= cmd.error_rc:
            if notifier is not None:
                notifier.error(
                    f"Error in {cmd.name}", error_notify_data(cmd, p, t0, t1)
                )
            raise subprocess.CalledProcessError(
                returncode=p.returncode,
                cmd=cmd.command,
                stderr=stderr,
                output=stdout,
            )

        elif cmd.warning_rc is not None and rc >= cmd.warning_rc:
            if notifier is not None:
                notifier.warning(
                    f"Warning in {cmd.name}", warning_notify_data(cmd, p, t0, t1)
                )
            logger.warning(f"Command ran with warning(s): {cmd.command}")

        else:
            if notifier is not None:
                notifier.info(
                    f"Finished {cmd.name}", success_notify_data(cmd, p, t0, t1)
                )

        ret = subprocess.CompletedProcess(
            args=p.args,
            returncode=p.returncode,
            stderr=stderr,
            stdout=stdout,
        )

    logger.info(
        f"""Ran command successfully:
  cmd     = {cmd.command}
  cwd     = {cmd.cwd}
  shell   = {cmd.shell}
  timeout = {cmd.timeout}
  rc      = {ret.returncode}
    """
    )
    return ret


def start_notify_data(cmd: Command, p: subprocess.Popen, t0: float):
    data = {} if cmd.notify is None else cmd.notify.copy()
    data["RECORD_TYPE"] = "START"
    data["COMMAND_NAME"] = cmd.name
    data["PID"] = p.pid
    data["TIMESTAMP"] = t0
    return data


def timeout_notify_data(cmd: Command, p: subprocess.Popen, t0: float, t1: float):
    data = {} if cmd.notify is None else cmd.notify.copy()
    data["RECORD_TYPE"] = "TIMEOUT"
    data["COMMAND_NAME"] = cmd.name
    data["PID"] = p.pid
    data["TIMESTAMP_START"] = t0
    data["TIMESTAMP"] = t1
    data["RETURNCODE"] = "" if p.returncode is None else str(p.returncode)
    data["TIMEOUT"] = cmd.timeout
    return data


def warning_notify_data(cmd: Command, p: subprocess.Popen, t0: float, t1: float):
    data = {} if cmd.notify is None else cmd.notify.copy()
    data["RECORD_TYPE"] = "WARNING"
    data["COMMAND_NAME"] = cmd.name
    data["PID"] = p.pid
    data["TIMESTAMP_START"] = t0
    data["TIMESTAMP"] = t1
    data["RETURNCODE"] = "" if p.returncode is None else str(p.returncode)
    return data


def error_notify_data(cmd: Command, p: subprocess.Popen, t0: float, t1: float):
    data = {} if cmd.notify is None else cmd.notify.copy()
    data["RECORD_TYPE"] = "ERROR"
    data["COMMAND_NAME"] = cmd.name
    data["PID"] = p.pid
    data["TIMESTAMP_START"] = t0
    data["TIMESTAMP"] = t1
    data["RETURNCODE"] = "" if p.returncode is None else str(p.returncode)
    return data


def success_notify_data(cmd: Command, p: subprocess.Popen, t0: float, t1: float):
    data = {} if cmd.notify is None else cmd.notify.copy()
    data["RECORD_TYPE"] = "SUCCESS"
    data["COMMAND_NAME"] = cmd.name
    data["PID"] = p.pid
    data["TIMESTAMP_START"] = t0
    data["TIMESTAMP"] = t1
    data["RETURNCODE"] = "" if p.returncode is None else str(p.returncode)
    return data
