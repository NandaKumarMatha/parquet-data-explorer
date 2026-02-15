import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

def load_parquet(file_path, offset=None, limit=None):
    if offset is not None and limit is not None:
        pf = pq.ParquetFile(file_path)
        # Read the whole table into Arrow memory (efficient), then slice and convert to Pandas (expensive part minimized)
        # For massive files larger than RAM, we would need iter_batches, but this suffices for V1 pagination
        table = pf.read()
        df = table.slice(offset, limit).to_pandas()
    else:
        table = pq.read_table(file_path)
        df = table.to_pandas()
    
    # Convert string dtypes to object for duckdb compatibility / general display
    for col in df.columns:
        if df[col].dtype == 'string':
            df[col] = df[col].astype('object')
    return df

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