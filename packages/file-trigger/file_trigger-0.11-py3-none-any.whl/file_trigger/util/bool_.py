from typing import Any


def strict_bool(msg: str, x: Any) -> bool:
    if isinstance(x, bool):
        return x
    raise ValueError(f"{msg} is not boolean: {x}")
