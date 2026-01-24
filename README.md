# Parquet Data Explorer

[![CI](https://github.com/NandaKumarMatha/parquet-data-explorer/actions/workflows/ci.yml/badge.svg)](https://github.com/NandaKumarMatha/parquet-data-explorer/actions/workflows/ci.yml)

A cross-platform desktop application for viewing, editing, and manipulating Parquet files.

## Author

This is an open-source project. Contributions welcome.

## Features
- Open and view Parquet files
- Display column metadata with tooltips
- Edit data inline or via SQL queries/updates
- Sort, filter, and query data using DuckDB SQL
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
- For a single file: `pyinstaller --onefile --windowed main.py`
- For a directory: `pyinstaller --onedir --windowed main.py`

The executable will be in the `dist/` folder.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.