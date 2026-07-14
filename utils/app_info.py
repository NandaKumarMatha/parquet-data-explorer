"""
Canonical product metadata for Parquet Explorer.

Edit this file only when name, version, URLs, or branding change.
Then run:  python3 scripts/sync_app_info.py
to update snapcraft, AppStream, setup.py, and desktop entry.
"""

APP_NAME = "Parquet Explorer"
APP_VERSION = "0.2.53"
APP_SUMMARY = "Official Parquet Explorer — view and edit Parquet files"
APP_DESCRIPTION = (
    "Official desktop app for viewing, editing, filtering, and visualizing Parquet files."
)
APP_AUTHOR = "Nanda Kumar Matha"
APP_CONTACT_EMAIL = "nandakumarmatha98@gmail.com"
APP_PUBLISHER = "n-incognito"
APP_LICENSE = "MIT"
APP_WEBSITE = "https://nandakumarmatha.github.io/"
APP_SOURCE = "https://github.com/NandaKumarMatha/parquet-data-explorer"
APP_ISSUES = "https://github.com/NandaKumarMatha/parquet-data-explorer/issues"
APP_SNAP = "https://snapcraft.io/parquet-explorer"
SNAP_PACKAGE_NAME = "parquet-explorer"

# Multi-line text used in Snap Store / packaging descriptions.
SNAP_DESCRIPTION = """\
Official Parquet Explorer by {author} (Snap publisher: {publisher}).

This is the official Snap for Parquet Explorer. Source and releases:
{source}

A PyQt6 desktop app to open, browse, edit, filter, and visualize Parquet files.
Features include pagination for large files, inline editing, search/query,
statistics, export (CSV/JSON/Excel), and charts.

Unofficial forks or lookalike packages are not affiliated with this project.
Please install only from this package name: {snap_name}.
""".format(
    author=APP_AUTHOR,
    publisher=APP_PUBLISHER,
    source=APP_SOURCE,
    snap_name=SNAP_PACKAGE_NAME,
)

METAINFO_DESCRIPTION_HTML = """\
    <p>
      Official Parquet Explorer by {author}. This is the authoritative
      desktop app for opening, browsing, editing, filtering, and visualizing
      Apache Parquet files.
    </p>
    <p>
      Install only the official package named {snap_name}. Unofficial forks
      or lookalike listings are not affiliated with this project.
    </p>
""".format(author=APP_AUTHOR, snap_name=SNAP_PACKAGE_NAME)


def about_text() -> str:
    return (
        f"<h2>{APP_NAME}</h2>"
        f"<p><b>Version</b> {APP_VERSION}</p>"
        f"<p>{APP_DESCRIPTION}</p>"
        f"<p>"
        f"<b>Author</b> {APP_AUTHOR}<br>"
        f"<b>Snap publisher</b> {APP_PUBLISHER}<br>"
        f"<b>License</b> {APP_LICENSE}<br>"
        f"<b>Official Snap</b> {SNAP_PACKAGE_NAME}"
        f"</p>"
        f"<p>"
        f'<a href="{APP_WEBSITE}">Website</a> · '
        f'<a href="{APP_SOURCE}">Source</a> · '
        f'<a href="{APP_ISSUES}">Issues</a> · '
        f'<a href="{APP_SNAP}">Snap Store</a>'
        f"</p>"
        f"<p><i>This is the official Parquet Explorer. "
        f"Forks should use a different product name.</i></p>"
    )
