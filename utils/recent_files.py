import os

from PyQt6.QtCore import QSettings

MAX_RECENT_FILES = 10
_SETTINGS_ORG = "ParquetExplorer"
_SETTINGS_APP = "ParquetDataExplorer"
_RECENT_KEY = "recent_files"


def _settings():
    return QSettings(_SETTINGS_ORG, _SETTINGS_APP)


def load_recent_files():
    paths = _settings().value(_RECENT_KEY, [])
    if not paths:
        return []
    if isinstance(paths, str):
        paths = [paths]

    recent = []
    seen = set()
    for path in paths:
        if not path:
            continue
        normalized = os.path.abspath(path)
        if normalized in seen:
            continue
        seen.add(normalized)
        recent.append(normalized)
    return recent


def add_recent_file(path):
    if not path:
        return

    normalized = os.path.abspath(path)
    recent = [p for p in load_recent_files() if p != normalized]
    recent.insert(0, normalized)
    _settings().setValue(_RECENT_KEY, recent[:MAX_RECENT_FILES])


def clear_recent_files():
    _settings().remove(_RECENT_KEY)
