from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Command:
    name: str
    command: List[str]
    cwd: Optional[str]
    shell: bool = False
    timeout: Optional[float] = None
    error_rc: int = 1
    warning_rc: Optional[int] = None
    notify: Optional[Dict[str, str]] = None

    def __str__(self) -> str:
        command_tokens = [repr(t) for t in self.command]
        cwd_str = "(parent)" if self.cwd is None else self.cwd
        return "\n".join(
            [
                f"{self.name}:",
                "-" * (len(self.name) + 1),
                f"  command = [ {', '.join(command_tokens)} ]",
                f"  cwd = {cwd_str}",
                f"  shell = {self.shell}",
                f"  timeout = {self.timeout}",
                f"  error_rc = {self.error_rc}",
                f"  warning_rc = {self.warning_rc}",
            ]
        )
