# Parquet Data Explorer

[![parquet-explorer](https://snapcraft.io/parquet-explorer/badge.svg)](https://snapcraft.io/parquet-explorer)
[![parquet-explorer](https://snapcraft.io/parquet-explorer/trending.svg?name=0)](https://snapcraft.io/parquet-explorer)
[![CI](https://github.com/NandaKumarMatha/parquet-data-explorer/actions/workflows/ci.yml/badge.svg)](https://github.com/NandaKumarMatha/parquet-data-explorer/actions/workflows/ci.yml)

A cross-platform desktop application for viewing, editing, and manipulating Parquet files.

## Author

This is an open-source project. Contributions welcome.

## Features
- Open and view Parquet files
- Display column metadata with tooltips
- Edit data inline or via pandas queries
- Sort, filter, and query data using pandas expressions
- Search rows by text
- View column statistics (mean, min, max, etc.)
- Convert to other formats (CSV, JSON, Excel)
- Create new Parquet files

## Installation

Download the latest release from [GitHub Releases](https://github.com/NandaKumarMatha/parquet-data-explorer/releases).

Or install from source:
1. Clone: `git clone https://github.com/NandaKumarMatha/parquet-data-explorer.git`
2. Install: `pip install -r requirements.txt`
3. Run: `python main.py`

## Building for Distribution
Use PyInstaller to create a standalone executable:
`pyinstaller main.spec`

The executable will be in the `dist/` folder.

## Creating a Release (Maintainers)
To create a new release on GitHub:
1. Go to the "Releases" section on GitHub.
2. Click "Draft a new release".
3. Tag the release (e.g., v1.0.0).
4. Click "Publish release".
This will trigger the workflow to build and upload the executables.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Roadmap

### ✅ Completed Features
- File operations (open, save, new Parquet files)
- Data viewing with sortable table
- Inline data editing with validation
- Data filtering using pandas query expressions
- Real-time search and filtering
- Column statistics panel
- Export to CSV, JSON, Excel
- Cross-platform builds (Windows, Linux)
- CI/CD with automated testing and releases
- Unit tests for core functionality

### 🚧 Upcoming Features
- Data visualization (charts for numeric columns)
- Undo/Redo functionality
- Large file support (pagination/virtual scrolling)
- Advanced filtering options
- Plugin system for custom transformations
- Dark/light theme support
- Performance optimizations
- Accessibility improvements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
