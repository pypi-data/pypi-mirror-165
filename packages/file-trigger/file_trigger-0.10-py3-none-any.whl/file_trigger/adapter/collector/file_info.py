from dataclasses import dataclass
from enum import Enum
from glob import glob
import os.path
import os
from typing import Union, Optional, Dict, List

from ...model.collector import Collector


@dataclass
class FileInfo:
    root_dir: Optional[str]
    path: str
    created: float
    modified: float
    size: int

    @property
    def relative_file_path(self):
        return (
            self.path
            if self.root_dir is None
            else os.path.relpath(self.path, self.root_dir)
        )

    @property
    def dir_path(self):
        return os.path.dirname(self.path)

    @property
    def relative_dir_path(self):
        return os.path.dirname(self.relative_file_path)

    @property
    def file_name(self):
        return os.path.basename(self.path)

    @property
    def file_ext(self):
        return os.path.splitext(self.path)[1][1:]


class Order(Enum):
    PATH = "path"
    CREATED = "created"
    MODIFIED = "modified"
    SIZE = "size"


class FileInfoCollector(Collector):
    name = "file info"

    def __init__(
        self,
        *,
        pattern: str,
        order: Union[str, Order],
        root_dir: Optional[str] = None,
        reverse: bool = False,
    ):
        self.pattern = pattern
        if isinstance(order, Order):
            self.order = order
        elif isinstance(order, str):
            self.order = Order(order.lower())
        else:
            raise ValueError(f"Unexpected type for order parameter: '{type(order)}'")
        self.root_dir = root_dir
        self.reverse = reverse

    def collect(self, captures: Dict[str, str]) -> FileInfo:
        pattern = self.pattern.format(**captures)
        root_dir = None if self.root_dir is None else self.root_dir.format(**captures)
        matches = [
            fetch_file_info(root_dir, fname)
            for fname in glob(
                os.path.join("" if root_dir is None else root_dir, pattern)
            )
        ]
        if len(matches) == 0:
            raise IndexError(
                f"No files found matching pattern '{pattern}'"
                + ("" if root_dir is None else f" in {root_dir}")
                + f" in collector '{self.name}'"
            )
        return self.sorted(matches)[0]

    def sorted(self, file_infos: List[FileInfo]) -> List[FileInfo]:
        def _sortfunc(file_info: FileInfo):
            if self.order == Order.PATH:
                return file_info.path
            elif self.order == Order.CREATED:
                return file_info.created
            elif self.order == Order.MODIFIED:
                return file_info.modified
            elif self.order == Order.SIZE:
                return file_info.size

        return sorted(file_infos, key=_sortfunc, reverse=self.reverse)


def fetch_file_info(root_dir: Optional[str], file_name: str):
    stat = os.stat(file_name)
    return FileInfo(
        root_dir=root_dir,
        path=file_name,
        created=float(stat.st_ctime),
        modified=float(stat.st_mtime),
        size=stat.st_size,
    )
