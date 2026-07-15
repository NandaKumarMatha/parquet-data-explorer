#!/usr/bin/env python3
"""
Push product metadata from utils/app_info.py into packaging files.

Source of truth: utils/app_info.py
Targets:
  - snap/snapcraft.yaml
  - snap/gui/parquet-explorer.metainfo.xml
  - snap/gui/parquet-explorer.desktop
  - setup.py

Usage:
  python3 scripts/sync_app_info.py
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils import app_info  # noqa: E402

SNAPCRAFT = ROOT / "snap" / "snapcraft.yaml"
METAINFO = ROOT / "snap" / "gui" / "parquet-explorer.metainfo.xml"
DESKTOP = ROOT / "snap" / "gui" / "parquet-explorer.desktop"
SETUP_PY = ROOT / "setup.py"


def _yaml_block(text: str, indent: int = 2) -> str:
    pad = " " * indent
    lines = text.strip("\n").splitlines()
    return "\n".join(f"{pad}{line}" if line else "" for line in lines)


def sync_snapcraft() -> None:
    text = SNAPCRAFT.read_text(encoding="utf-8")
    if "plugs:" not in text:
        raise SystemExit(f"Could not find plugs: section in {SNAPCRAFT}")

    rest = text.split("plugs:", 1)[1]
    description = _yaml_block(app_info.SNAP_DESCRIPTION, indent=2)
    header = (
        f"name: {app_info.SNAP_PACKAGE_NAME}\n"
        f"title: {app_info.APP_NAME}\n"
        f"base: core24\n"
        f"version: '{app_info.APP_VERSION}'\n"
        f"summary: {app_info.APP_SUMMARY}\n"
        f"description: |\n"
        f"{description}\n"
        f"\n"
        f"grade: stable\n"
        f"confinement: strict\n"
        f"license: {app_info.APP_LICENSE}\n"
        f"website: \n"
        f"  - {app_info.APP_WEBSITE}\n"
        f"source-code: \n"
        f"  - {app_info.APP_SOURCE}\n"
        f"issues: \n"
        f"  - {app_info.APP_ISSUES}\n"
        f"icon: snap/gui/icon.png\n"
        f"contact: \n"
        f"  - {app_info.APP_CONTACT_EMAIL}\n"
        f"\n"
        f"plugs:"
    )
    SNAPCRAFT.write_text(header + rest, encoding="utf-8")
    print(f"Synced {SNAPCRAFT.relative_to(ROOT)}")


def sync_metainfo(release_date: str | None = None) -> None:
    release_date = release_date or date.today().isoformat()
    desc = app_info.METAINFO_DESCRIPTION_HTML.rstrip() + "\n"
    content = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>{app_info.SNAP_PACKAGE_NAME}</id>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>{app_info.APP_LICENSE}</project_license>
  <name>{app_info.APP_NAME}</name>
  <summary>{app_info.APP_SUMMARY}</summary>
  <developer_name>{app_info.APP_AUTHOR}</developer_name>
  <description>
{desc}  </description>
  <url type="homepage">{app_info.APP_WEBSITE}</url>
  <url type="bugtracker">{app_info.APP_ISSUES}</url>
  <url type="vcs-browser">{app_info.APP_SOURCE}</url>
  <categories>
    <category>Development</category>
    <category>Utility</category>
    <category>Database</category>
  </categories>
  <launchable type="desktop-id">{app_info.SNAP_PACKAGE_NAME}.desktop</launchable>
  <releases>
    <release version="{app_info.APP_VERSION}" date="{release_date}" />
  </releases>
</component>
"""
    METAINFO.write_text(content, encoding="utf-8")
    print(
        f"Synced {METAINFO.relative_to(ROOT)} "
        f"(version={app_info.APP_VERSION}, date={release_date})"
    )


def sync_desktop() -> None:
    content = f"""\
[Desktop Entry]
Name={app_info.APP_NAME}
Exec={app_info.SNAP_PACKAGE_NAME} %F
Icon=${{SNAP}}/meta/gui/icon.png
Type=Application
Categories=Development;Utility;Database;
Comment={app_info.APP_SUMMARY}
Terminal=false
StartupNotify=true
"""
    DESKTOP.write_text(content, encoding="utf-8")
    print(f"Synced {DESKTOP.relative_to(ROOT)}")


def sync_setup_py() -> None:
    text = SETUP_PY.read_text(encoding="utf-8")
    text, n_name = re.subn(
        r'name\s*=\s*"[^"]*"',
        f'name="{app_info.SNAP_PACKAGE_NAME}"',
        text,
        count=1,
    )
    text, n_ver = re.subn(
        r'version\s*=\s*"[^"]*"',
        f'version="{app_info.APP_VERSION}"',
        text,
        count=1,
    )
    if n_name != 1 or n_ver != 1:
        raise SystemExit(f"Could not update name/version in {SETUP_PY}")
    SETUP_PY.write_text(text, encoding="utf-8")
    print(f"Synced {SETUP_PY.relative_to(ROOT)}")


def main() -> None:
    sync_snapcraft()
    sync_metainfo()
    sync_desktop()
    sync_setup_py()
    print(f"Done — source: utils/app_info.py ({app_info.APP_NAME} v{app_info.APP_VERSION})")


if __name__ == "__main__":
    main()
