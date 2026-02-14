import sys
import unittest
import pandas as pd
import numpy as np
import os
from PyQt6.QtWidgets import QApplication, QUndoStack
from PyQt6.QtCore import QModelIndex
from ui.commands import EditCommand
from data.parquet_handler import load_parquet, save_parquet, get_row_count
import qdarkstyle

class TestFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a dummy app
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        
        # Create a large parquet file
        cls.large_file = "test_large.parquet"
        df = pd.DataFrame({'A': range(2500)}) # 2.5 pages if size is 1000
        save_parquet(df, cls.large_file)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.large_file):
            os.remove(cls.large_file)

    def test_theme_load(self):
        try:
            # Test loading stylesheet
            sheet = qdarkstyle.load_stylesheet()
            self.assertTrue(len(sheet) > 0)
            print("Theme loading passed")
        except Exception as e:
            self.fail(f"Theme loading failed: {e}")

    def test_pagination(self):
        # Allow reading pages
        total = get_row_count(self.large_file)
        self.assertEqual(total, 2500)
        
        # Page 1 (0-1000)
        df_p1 = load_parquet(self.large_file, offset=0, limit=1000)
        self.assertEqual(len(df_p1), 1000)
        self.assertEqual(df_p1.iloc[0]['A'], 0)
        self.assertEqual(df_p1.iloc[999]['A'], 999)
        
        # Page 3 (2000-3000 -> 2000-2500)
        df_p3 = load_parquet(self.large_file, offset=2000, limit=1000)
        self.assertEqual(len(df_p3), 500)
        self.assertEqual(df_p3.iloc[0]['A'], 2000)
        self.assertEqual(df_p3.iloc[499]['A'], 2499)
        print("Pagination logic passed")

    def test_undo_redo(self):
        stack = QUndoStack()
        
        # Mock model with internal dictionary
        class MockModel:
            def __init__(self):
                self.data = {}
            def set_data_internal(self, index, value):
                self.data[(index.row(), index.column())] = value
        
        model = MockModel()
        index = QModelIndex() # Mock index, won't use methods
        
        # Mock index row/col for our dict
        class MockIndex:
            def row(self): return 0
            def column(self): return 0
        
        idx = MockIndex()
        
        # Initial edit: Set 0,0 to "Value1" (from "Empty")
        cmd1 = EditCommand(model, idx, "Empty", "Value1")
        stack.push(cmd1)
        self.assertEqual(model.data[(0,0)], "Value1")
        
        # Second edit: Set 0,0 to "Value2"
        cmd2 = EditCommand(model, idx, "Value1", "Value2")
        stack.push(cmd2)
        self.assertEqual(model.data[(0,0)], "Value2")
        
        # Undo -> Value1
        stack.undo()
        self.assertEqual(model.data[(0,0)], "Value1")
        
        # Undo -> Empty
        stack.undo()
        self.assertEqual(model.data[(0,0)], "Empty")
        
        # Redo -> Value1
        stack.redo()
        self.assertEqual(model.data[(0,0)], "Value1")
        print("Undo/Redo logic passed")

if __name__ == '__main__':
    unittest.main()
