import os.path
from typing import Optional, Tuple

from watchdog.events import (
    FileSystemEvent,
    FileSystemMovedEvent,
    DirMovedEvent,
    DirDeletedEvent,
    DirCreatedEvent,
    DirModifiedEvent,
    FileMovedEvent,
    FileDeletedEvent,
    FileCreatedEvent,
    FileModifiedEvent,
    FileClosedEvent,
    EVENT_TYPE_MOVED,
    EVENT_TYPE_DELETED,
    EVENT_TYPE_CREATED,
    EVENT_TYPE_MODIFIED,
    EVENT_TYPE_CLOSED,
)

# The 'pushed' pseudo-event used with push command

EVENT_TYPE_PUSHED = "pushed"


class FilePushedPseudoEvent(FileSystemEvent):
    event_type = EVENT_TYPE_PUSHED


EVENT_TYPES = {
    EVENT_TYPE_MOVED,
    EVENT_TYPE_DELETED,
    EVENT_TYPE_CREATED,
    EVENT_TYPE_MODIFIED,
    EVENT_TYPE_CLOSED,
    EVENT_TYPE_PUSHED,
}


def event_type_from_string(event_type: str) -> str:
    if event_type.lower() == EVENT_TYPE_MOVED:
        return EVENT_TYPE_MOVED
    elif event_type.lower() == EVENT_TYPE_DELETED:
        return EVENT_TYPE_DELETED
    elif event_type.lower() == EVENT_TYPE_CREATED:
        return EVENT_TYPE_CREATED
    elif event_type.lower() == EVENT_TYPE_MODIFIED:
        return EVENT_TYPE_MODIFIED
    elif event_type.lower() == EVENT_TYPE_CLOSED:
        return EVENT_TYPE_CLOSED
    elif event_type.lower() == EVENT_TYPE_PUSHED:
        return EVENT_TYPE_PUSHED
    else:
        raise ValueError(f"Unknown event type: '{event_type}'")


def event_from_type_and_file_names(
    event_type: str,
    file_name: str,
    dest_file_name: Optional[str] = None,
) -> FileSystemEvent:
    is_dir = os.path.isdir(file_name)
    event_type = event_type_from_string(event_type)
    if event_type == EVENT_TYPE_MOVED.lower():
        return (
            DirMovedEvent(file_name, dest_file_name)
            if is_dir
            else FileMovedEvent(file_name, dest_file_name)
        )
    elif event_type == EVENT_TYPE_DELETED.lower():
        return DirDeletedEvent(file_name) if is_dir else FileDeletedEvent(file_name)
    elif event_type == EVENT_TYPE_CREATED.lower():
        return DirCreatedEvent(file_name) if is_dir else FileCreatedEvent(file_name)
    elif event_type == EVENT_TYPE_MODIFIED.lower():
        return DirModifiedEvent(file_name) if is_dir else FileModifiedEvent(file_name)
    elif event_type == EVENT_TYPE_CLOSED.lower():
        return FileClosedEvent(file_name)
    elif event_type == EVENT_TYPE_PUSHED.lower():
        return FilePushedPseudoEvent(file_name)

    else:
        raise ValueError(f"Unknown event type: '{event_type}'")


def event_type_and_file_names_from_event(
    event: FileSystemEvent,
) -> Tuple[str, str, Optional[str]]:
    if isinstance(event, FileSystemMovedEvent):
        return (event.event_type, event.src_path, event.dest_path)
    else:
        return (event.event_type, event.src_path, None)
