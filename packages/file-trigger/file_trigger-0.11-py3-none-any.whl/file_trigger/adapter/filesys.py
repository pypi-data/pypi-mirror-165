from functools import reduce
import os
import os.path
import re
from typing import Optional, Dict

from ..util import re_

REGEXP_VAR = re.compile("(\\{[a-zA-Z0-9_]+\\})", flags=re.I + re.A)
REGEXP_VAR_OR_GLOB = re.compile("(\\{[a-zA-Z0-9_]+\\}|\\*\\*|\\*)", flags=re.I + re.A)


class Matcher:
    def __init__(self, expr: str):
        self._expr = compiled_match_expr(expr)
        self.glob = REGEXP_VAR.sub("*", expr)

    def match(self, dir: str) -> Optional[Dict[str, str]]:
        matches = re.match(self._expr, dir)
        if matches is None:
            return None
        return matches.groupdict()

    def matches(self, dir: str) -> bool:
        return self.match(dir) is not None


def compiled_match_expr(expr: str) -> re.Pattern:
    def _build_segment(segment, pair):
        pre, s = pair
        return "".join(
            [segment, re.escape(pre), "" if len(s) == 0 else _parse_var_or_glob(s)]
        )

    def _parse_var_or_glob(s: str) -> str:
        if s == "**":
            return ".+"
        elif s == "*":
            return f"[^{re.escape(os.sep)}]+"
        else:
            return f"(?P<{s[1:-1]}>[^{re.escape(os.sep)}]+)"

    def _parse_segment(s: str) -> str:
        subsegments = re_.find_match_segments(REGEXP_VAR_OR_GLOB, s)
        if len(subsegments) == 0:  # no match in segment, parse as literal
            return re.escape(s)
        else:
            return reduce(_build_segment, subsegments, "")

    segments = expr.split(os.sep)
    parsed_expr = re.escape(os.sep).join(
        [_parse_segment(segment) for segment in segments]
    )
    return re.compile(
        parsed_expr,
        flags=re.A + re.I,
    )
