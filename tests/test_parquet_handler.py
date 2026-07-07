import pytest
from data.parquet_handler import (
    load_parquet, save_parquet, apply_edited_cells, load_parquet_full, LoadCancelled,
)
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

def test_parquet_pagination_slice():
    df = pd.DataFrame({
        'a': list(range(20)),
        'b': [f"v{i}" for i in range(20)],
    })

    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
        temp_file = f.name

    try:
        save_parquet(df, temp_file)
        paged_df = load_parquet(temp_file, offset=5, limit=7)

        expected = df.iloc[5:12].copy()
        expected['b'] = expected['b'].astype('object')
        expected.index = range(5, 12)
        pd.testing.assert_frame_equal(expected, paged_df)
    finally:
        os.unlink(temp_file)

def test_apply_edited_cells():
    df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
    edited = {1: {'b': 'edited'}, 99: {'a': 9}}
    result = apply_edited_cells(df.copy(), edited)
    assert result.at[1, 'b'] == 'edited'
    assert result.at[1, 'a'] == 2

def test_load_parquet_full_applies_edits():
    df = pd.DataFrame({'a': [10, 20, 30], 'b': ['p', 'q', 'r']})
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
        temp_file = f.name
    try:
        save_parquet(df, temp_file)
        loaded = load_parquet_full(temp_file, edited_cells={1: {'a': 99}})
        assert loaded.at[1, 'a'] == 99
        assert loaded.at[0, 'a'] == 10
    finally:
        os.unlink(temp_file)

def test_load_parquet_full_cancelled():
    df = pd.DataFrame({'a': list(range(1000))})
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as f:
        temp_file = f.name
    try:
        save_parquet(df, temp_file)
        with pytest.raises(LoadCancelled):
            load_parquet_full(temp_file, cancel_check=lambda: True)
    finally:
        os.unlink(temp_file)