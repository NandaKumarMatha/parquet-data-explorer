import pytest
from data.parquet_handler import load_parquet, save_parquet
import pandas as pd
import tempfile
import os

def test_parquet_handler():
    # Create test data
    df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
    df['b'] = df['b'].astype('object')  # Ensure object dtype
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
        temp_file = f.name
    
    try:
        save_parquet(df, temp_file)
        loaded_df = load_parquet(temp_file)
        pd.testing.assert_frame_equal(df, loaded_df)
    finally:
        os.unlink(temp_file)