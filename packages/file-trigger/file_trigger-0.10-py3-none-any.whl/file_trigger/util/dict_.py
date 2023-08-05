from functools import reduce
from typing import TypeVar, Any, Iterable, List, Dict

K = TypeVar("K")
V = TypeVar("V")


def strict_dict(msg: str, x: Any) -> Dict[Any, Any]:
    if isinstance(x, dict):
        return x
    raise ValueError(f"{msg} is not boolean: {x}")


def merged(a: Dict[K, V], b: Dict[K, V]) -> Dict[K, V]:
    c = a.copy()
    c.update(b)
    return c


def missing_fields(fields: Iterable[K], row: Dict[K, Any]) -> List[K]:
    keys = set(row.keys())
    return [f for f in fields if f not in keys]


def null_fields(fields: Iterable[K], row: Dict[K, Any]) -> List[K]:
    keys = set(row.keys())
    return [f for f in fields if f in keys and row.get(f, None) is None]


def empty_fields(fields: Iterable[K], row: Dict[K, str]) -> List[K]:
    keys = set(row.keys())
    return [f for f in fields if f in keys and len(row.get(f, "")) == 0]


def excluding_fields(fields: Iterable[K], row: Dict[K, V]) -> Dict[K, V]:
    return dict((k, v) for (k, v) in row.items() if k not in fields)


def path(fields: Iterable[K], row: Dict[K, Any]) -> Any:
    def _acc(v, k):
        if isinstance(v, dict):
            return v[k]
        raise KeyError(k)

    return reduce(_acc, fields, row)


def has_path(fields: Iterable[K], row: Dict[K, Any]) -> bool:
    def _acc(pair, k):
        ret, v = pair
        if not ret:
            return (ret, v)
        if isinstance(v, dict):
            if k in v:
                return (True, v[k])
            else:
                return (False, None)
        else:
            return (False, None)

    return reduce(_acc, fields, (True, row))[0]


def assert_has_fields(fields: Iterable[K], msg: str, row: Dict[K, V]) -> None:
    missings = missing_fields(fields, row)
    if len(missings) == 1:
        raise ValueError(f"{msg} missing field: {missings[0]}\n{row}")
    elif len(missings) > 0:
        flds = "\n  ".join([str(m) for m in missings])
        raise ValueError(f"{msg} missing fields:\n  {flds}\n{row}")


def assert_has_field(field: K, msg: str, row: Dict[K, V]) -> None:
    return assert_has_fields([field], msg, row)
