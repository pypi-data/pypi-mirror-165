import dataclasses
import re
from typing import List

REGEX_OPTIONAL_TYPE = re.compile(
    r"^typing\.Optional\[.+\]$|^typing\.Union\[.+, NoneType\]$"
)
REGEX_LIST_TYPE = re.compile(r"^typing\.List\[.+\]$")
REGEX_SET_TYPE = re.compile(r"^typing\.Set\[.+\]$")
REGEX_DICT_TYPE = re.compile(r"^typing\.Dict\[.+\]$")
REGEX_ITERABLE_TYPE = re.compile(r"^typing\.Iterable\[.+\]$")


def nonoptional_fields(klass: type) -> List[str]:
    # kludgy, yes
    return [
        f.name
        for f in dataclasses.fields(klass)
        if f.default == dataclasses.MISSING
        and REGEX_OPTIONAL_TYPE.match(str(f.type)) is None
    ]


def nonoptional_nonlist_fields(klass: type) -> List[str]:
    # kludgy, yes
    return [
        f.name
        for f in dataclasses.fields(klass)
        if (
            f.default == dataclasses.MISSING
            and REGEX_OPTIONAL_TYPE.match(str(f.type)) is None
            and REGEX_LIST_TYPE.match(str(f.type)) is None
        )
    ]


def nonoptional_noniterable_fields(klass: type) -> List[str]:
    # kludgy, yes
    return [
        f.name
        for f in dataclasses.fields(klass)
        if (
            f.default == dataclasses.MISSING
            and REGEX_OPTIONAL_TYPE.match(str(f.type)) is None
            and REGEX_LIST_TYPE.match(str(f.type)) is None
            and REGEX_SET_TYPE.match(str(f.type)) is None
            and REGEX_DICT_TYPE.match(str(f.type)) is None
            and REGEX_ITERABLE_TYPE.match(str(f.type)) is None
        )
    ]
