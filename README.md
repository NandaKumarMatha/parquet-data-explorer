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

### GitHub Release (Windows + Linux binaries)

Chained after a successful Snap publish on `master` / `main`:

1. Bump `APP_VERSION` in `utils/app_info.py` and run `python3 scripts/sync_app_info.py`
2. Merge / push to `master`
3. Snap workflow builds, publishes to the store, then:
   - Creates git tag `v{APP_VERSION}` (if it does not exist)
   - Dispatches the **Release** workflow
4. Release workflow uploads `parquet-explorer-Windows.exe` and `parquet-explorer-Linux`

If the tag already exists but release binaries are missing, Snap publish will
still dispatch the Release workflow. It only skips when both Windows and Linux
assets are already attached.

Optional manual run: Actions → **Release** → **Run workflow**.

### Snap

Official Snap publishing is handled by the snap workflow on `master` / `main` pushes.

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

- File operations (open, save, new) and export (CSV / JSON / Excel)
- Sortable table view, inline editing, undo / redo
- Search, filter, and pandas queries
- Column statistics (page-scoped) and Plotly visualizations (sampled)
- Pagination for large files (streaming reads, editable page jump)
- Background page / full-data loading with progress and large-file warnings
- Safe paginated save / export / query (edit tracking + full-data merge)
- Themes (dark / light / auto) and font zoom
- Recent files menu
- Help → About dialog (version and official product info)
- Startup splash / loader and single-instance focus (avoids double launches)
- Terminal launch banner
- Centralized app metadata (`utils/app_info.py` → packaging sync)
- Official branding / Snap identity documented
- Windows & Linux builds, Snap packaging, CI/CD, unit tests

### Planned

- Streaming save / export without loading the full file into RAM
- Advanced filtering UX (column filters, saved filters)
- Plugin system for custom transformations
- Lazy-load WebEngine / lighter viz path for faster cold start
- Accessibility improvements (keyboard, screen reader)
- Optional macOS builds

---

## License

MIT — see [LICENSE](LICENSE).

The license covers the **source code**. Name, Snap package identity, and visual branding for the official product are separate — see [Brand and naming](#brand-and-naming).
