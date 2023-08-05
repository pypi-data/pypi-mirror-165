from typing import Iterable, Tuple


class BaseError(Exception):
    pass


class ExecutionErrors(BaseError):
    def __init__(self, errors: Iterable[Tuple[str, str, Exception]]):
        self.errors = errors

    def __str__(self) -> str:
        return "\n".join(
            [
                f"Execution error{'s' if len(self.errors) > 1 else ''} (check logs for details):"
            ]
            + [
                f"  {i+1}. {handler}: Error running command {cmdname}:\n{e}"
                for (i, (handler, cmdname, e)) in enumerate(self.errors)
            ]
        )
