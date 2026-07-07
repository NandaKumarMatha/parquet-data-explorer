import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

FULL_LOAD_WARN_ROWS = 100_000
VIZ_SAMPLE_MAX_ROWS = 10_000


class LoadCancelled(Exception):
    """Raised when a background load is cancelled by the user."""


def _normalize_string_columns(df):
    for col in df.columns:
        if df[col].dtype == 'string':
            df[col] = df[col].astype('object')
    return df


def apply_edited_cells(df, edited_cells):
    if not edited_cells:
        return df
    for row_idx, updates in edited_cells.items():
        if row_idx not in df.index and 0 <= row_idx < len(df):
            target_idx = row_idx
        elif row_idx in df.index:
            target_idx = row_idx
        else:
            continue
        for col_name, value in updates.items():
            if col_name in df.columns:
                df.at[target_idx, col_name] = value
    return df

def load_parquet(file_path, offset=None, limit=None):
    if offset is not None and limit is not None:
        pf = pq.ParquetFile(file_path)
        batches = []
        rows_to_skip = max(0, offset)
        rows_to_take = max(0, limit)
        collected = 0

        # Stream row batches and extract only requested window.
        for batch in pf.iter_batches(batch_size=min(max(limit, 1024), 65536)):
            batch_rows = batch.num_rows
            if rows_to_skip >= batch_rows:
                rows_to_skip -= batch_rows
                continue

            start = rows_to_skip
            take = min(rows_to_take - collected, batch_rows - start)
            if take > 0:
                batches.append(batch.slice(start, take))
                collected += take
            rows_to_skip = 0

            if collected >= rows_to_take:
                break

        if batches:
            table = pa.Table.from_batches(batches)
            df = table.to_pandas()
        else:
            # Keep a consistent empty DataFrame shape.
            df = pf.schema_arrow.empty_table().to_pandas()

        # Preserve global row positions so edits can be merged safely.
        df.index = range(offset, offset + len(df))
    else:
        table = pq.read_table(file_path)
        df = table.to_pandas()
    
    # Convert string dtypes to object for duckdb compatibility / general display
    return _normalize_string_columns(df)


def load_parquet_full(file_path, edited_cells=None, cancel_check=None, on_progress=None):
    pf = pq.ParquetFile(file_path)
    total_rows = pf.metadata.num_rows or 0
    chunks = []
    collected = 0

    for batch in pf.iter_batches(batch_size=65536):
        if cancel_check and cancel_check():
            raise LoadCancelled("Load cancelled by user")
        chunks.append(batch)
        collected += batch.num_rows
        if on_progress:
            on_progress(collected, total_rows)

    if chunks:
        table = pa.Table.from_batches(chunks)
        df = table.to_pandas()
    else:
        df = pf.schema_arrow.empty_table().to_pandas()

    df = _normalize_string_columns(df)
    return apply_edited_cells(df, edited_cells or {})

def get_row_count(file_path):
    pf = pq.ParquetFile(file_path)
    return pf.metadata.num_rows

def save_parquet(df, file_path):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)

def get_metadata(df, col_index):
    col_name = df.columns[col_index]
    dtype = str(df[col_name].dtype)
    nullable = df[col_name].isnull().any()
    return {'type': dtype, 'nullable': nullable}