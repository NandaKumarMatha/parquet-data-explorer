import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

def load_parquet(file_path):
    table = pq.read_table(file_path)
    df = table.to_pandas()
    # Convert string dtypes to object for duckdb compatibility
    for col in df.columns:
        if df[col].dtype == 'string':
            df[col] = df[col].astype('object')
    return df

def save_parquet(df, file_path):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)

def get_metadata(df, col_index):
    col_name = df.columns[col_index]
    dtype = str(df[col_name].dtype)
    nullable = df[col_name].isnull().any()
    return {'type': dtype, 'nullable': nullable}