from typing import Any, Protocol, Dict


class Collector(Protocol):
    name: str

    def collect(self, captures: Dict[str, str]) -> Any:
        ...
