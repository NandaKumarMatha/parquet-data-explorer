from setuptools import setup, find_packages

setup(
    name="parquet-explorer",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "PyQt6>=6.0.0",
        "pyarrow>=10.0.0",
        "pandas>=1.5.0",
        "duckdb>=0.8.0",
    ],
    entry_points={
        "console_scripts": [
            "parquet-explorer=main:main",
        ],
    },
)
