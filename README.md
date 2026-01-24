# Parquet Data Explorer

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

## Requirements
- Python 3.8+
- Dependencies: See requirements.txt

## Installation
1. Clone or download the project.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

## Building for Distribution
Use PyInstaller to create a standalone executable:
- For a single file: `pyinstaller --onefile --windowed main.py`
- For a directory: `pyinstaller --onedir --windowed main.py`

The executable will be in the `dist/` folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.