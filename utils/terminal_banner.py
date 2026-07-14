"""Terminal launch banner for interactive CLI starts."""

from __future__ import annotations

import sys

from utils.app_info import APP_AUTHOR, APP_NAME, APP_VERSION, APP_WEBSITE, SNAP_PACKAGE_NAME

# Block-style banner shown when launched from a real terminal.
BANNER = r"""
██████╗  █████╗ ██████╗  ██████╗ ██╗   ██╗███████╗████████╗
██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██║   ██║██╔════╝╚══██╔══╝
██████╔╝███████║██████╔╝██║   ██║██║   ██║█████╗     ██║
██╔═══╝ ██╔══██║██╔══██╗██║▄▄ ██║██║   ██║██╔══╝     ██║
██║     ██║  ██║██║  ██║╚██████╔╝╚██████╔╝███████╗   ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝   ╚═╝
███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗██████╗
██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗
█████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  ██████╔╝
██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
""".strip("\n")


def print_launch_banner() -> None:
    """Print the product banner when stdout is an interactive terminal."""
    if not sys.stdout.isatty():
        return

    print(BANNER)
    print(f"  {APP_NAME}  v{APP_VERSION}")
    print(f"  by {APP_AUTHOR}  ·  snap: {SNAP_PACKAGE_NAME}")
    print(f"  {APP_WEBSITE}\n")
    # print()
