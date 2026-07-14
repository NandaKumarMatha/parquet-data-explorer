#!/usr/bin/env python3
"""Deprecated alias — forwards to scripts/sync_app_info.py."""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("sync_app_info.py")), run_name="__main__")
