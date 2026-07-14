# Parquet Explorer

[![parquet-explorer](https://snapcraft.io/parquet-explorer/badge.svg)](https://snapcraft.io/parquet-explorer)
[![parquet-explorer](https://snapcraft.io/parquet-explorer/trending.svg?name=0)](https://snapcraft.io/parquet-explorer)
[![CI](https://github.com/NandaKumarMatha/parquet-data-explorer/actions/workflows/ci.yml/badge.svg)](https://github.com/NandaKumarMatha/parquet-data-explorer/actions/workflows/ci.yml)

**Official product:** Parquet Explorer  
**Official Snap package:** [`parquet-explorer`](https://snapcraft.io/parquet-explorer)  
**Publisher:** [Nanda Kumar Matha (`n-incognito`)](https://snapcraft.io/publisher/n-incognito)  
**Source:** [github.com/NandaKumarMatha/parquet-data-explorer](https://github.com/NandaKumarMatha/parquet-data-explorer)

A cross-platform desktop app for viewing, editing, filtering, and visualizing Parquet files.

Supported platforms: **Windows** · **Linux**

---

## Official channels only

Use only these sources for the **official** Parquet Explorer:

| Channel | Official location |
|---------|-------------------|
| Linux Snap | [`snap install parquet-explorer`](https://snapcraft.io/parquet-explorer) — publisher **n-incognito** |
| GitHub Releases | [NandaKumarMatha/parquet-data-explorer/releases](https://github.com/NandaKumarMatha/parquet-data-explorer/releases) |
| Source repository | [NandaKumarMatha/parquet-data-explorer](https://github.com/NandaKumarMatha/parquet-data-explorer) |

Any other Snap name, store listing, website, or binary that claims to be “Parquet Explorer” but is not from the publisher/repo above is **unofficial**.

---

## Brand and naming

**Parquet Explorer**, the **`parquet-explorer`** Snap name, and the project logo/icon are the brand identity of this official product.

You are welcome to:

- Fork the repository
- Contribute improvements via pull requests
- Study and modify the code under the license

Please **do not**:

- Publish a Snap, store listing, or distribution under the name **Parquet Explorer** or **`parquet-explorer`**
- Use this project’s logo/icon in a way that suggests you are the official product
- Impersonate the official publisher (**n-incognito** / Nanda Kumar Matha)

---

## Features

- Open, view, save, and create Parquet files
- Paginated browsing for large files
- Inline editing with undo / redo
- Sort, search, and pandas query filtering
- Column statistics and Plotly visualizations
- Export to CSV, JSON, and Excel
- Dark / light / auto themes

---

## Installation

### Windows

1. Open the official [GitHub Releases](https://github.com/NandaKumarMatha/parquet-data-explorer/releases).
2. Download `parquet-explorer-Windows.exe`.
3. Run the executable.

### Linux

**Option A — Official Snap (recommended)**

```bash
sudo snap install parquet-explorer
```

Confirm the publisher is **n-incognito** on [snapcraft.io/parquet-explorer](https://snapcraft.io/parquet-explorer).

Edge channel (pre-release builds from this project):

```bash
sudo snap install parquet-explorer --edge
```

**Option B — Official GitHub Releases**

1. Open [GitHub Releases](https://github.com/NandaKumarMatha/parquet-data-explorer/releases).
2. Download `parquet-explorer-Linux`.
3. Make it executable and run:

```bash
chmod +x parquet-explorer-Linux
./parquet-explorer-Linux
```

---

## Run from Source

Works on both Windows and Linux.

### Requirements

- Python 3.12+
- Git

### Setup

```bash
git clone https://github.com/NandaKumarMatha/parquet-data-explorer.git
cd parquet-data-explorer
python -m venv .venv
```

**Windows**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

**Linux**

```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

You can also open a file directly:

```bash
python main.py path/to/file.parquet
```

### Tests

```bash
pip install pytest
python -m pytest tests/
```

---

## Build Standalone Apps

### Windows

```powershell
pip install pyinstaller
pyinstaller main.spec
```

Output: `dist\parquet-explorer.exe`

### Linux

```bash
pip install pyinstaller
pyinstaller --onefile -n parquet-explorer main.py
```

Output: `dist/parquet-explorer`

### Linux Snap (maintainers of this project only)

```bash
snapcraft pack
```

The official Snap name **`parquet-explorer`** is reserved for this project’s publisher. Forks must not reuse that package name.

---

## Releases (Maintainers)

Product metadata (name, version, URLs, Snap description) lives in **`utils/app_info.py`** only.
After editing it, sync packaging files:

```bash
python3 scripts/sync_app_info.py
```

That updates `snap/snapcraft.yaml`, AppStream metainfo, desktop entry, and `setup.py`.

1. Open **Releases** on GitHub → **Draft a new release**.
2. Tag the version (for example `v1.0.0`).
3. Publish the release.

CI builds Windows and Linux binaries and uploads them to the release. Official Snap publishing is handled by this repository’s snap workflow on `master` / `main`.

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests when needed
5. Open a pull request against **this** repository

Thanks for helping improve the official Parquet Explorer. Please keep forks clearly named as separate projects if you redistribute them.

---

## Roadmap

### Done

- File operations (open, save, new)
- Sortable table view and inline editing
- Search, filter, and pandas queries
- Statistics panel and visualizations
- Undo / redo
- Pagination for large files
- Themes (dark / light / auto)
- Windows & Linux builds + Snap packaging
- CI/CD and basic unit tests

### Planned

- Advanced filtering UX
- Plugin system for custom transformations
- Further performance and accessibility improvements
- Streaming save/export for very large files

---

## License

MIT — see [LICENSE](LICENSE).

The license covers the **source code**. Name, Snap package identity, and visual branding for the official product are separate — see [Brand and naming](#brand-and-naming).
