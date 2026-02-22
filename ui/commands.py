from PyQt6.QtGui import QUndoCommand
import pandas as pd

class EditCommand(QUndoCommand):
    def __init__(self, main_window, index, old_value, new_value):
        super().__init__(f"Edit cell {index.row()},{index.column()}")
        self.mw = main_window
        # Store persistent identifiers
        # index.row() is position in current view (filtered_df)
        # We need the actual dataframe index label
        row_pos = index.row()
        self.row_label = self.mw.filtered_df.index[row_pos]
        self.col_name = self.mw.filtered_df.columns[index.column()]
        
        self.old_value = old_value
        self.new_value = new_value

    def redo(self):
        self._update_dataframe(self.new_value)

    def undo(self):
        self._update_dataframe(self.old_value)

    def _update_dataframe(self, value):
        # Update underlying dataframes
        # We must update both df (current page/view) and main_df (if separate, logic in MainWindow suggests main_df is important)
        # But 'set_data_internal' updated both.
        # Here we access them via mw
        
        if self.row_label in self.mw.df.index:
             self.mw.df.at[self.row_label, self.col_name] = value
             
        if hasattr(self.mw.model, 'main_df') and self.mw.model.main_df is not None:
             # If main_df is different object
             if self.row_label in self.mw.model.main_df.index:
                 self.mw.model.main_df.at[self.row_label, self.col_name] = value

        self.mw.refresh_view_for_cell(self.row_label, self.col_name)

class AddRowCommand(QUndoCommand):
    def __init__(self, main_window, row_idx):
        super().__init__("Add Row")
        self.mw = main_window
        self.row_idx = row_idx
        self.new_row_data = None

    def redo(self):
        # Insert a new empty row at row_idx
        new_row = pd.Series([None] * len(self.mw.df.columns), index=self.mw.df.columns)
        if self.new_row_data is not None:
             new_row = self.new_row_data
        
        self.mw.df = pd.concat([self.mw.df.iloc[:self.row_idx], 
                                pd.DataFrame([new_row], columns=self.mw.df.columns), 
                                self.mw.df.iloc[self.row_idx:]]).reset_index(drop=True)
        self.mw.filtered_df = self.mw.df # Simplified for now
        self.mw.update_table()

    def undo(self):
        # Store data before deleting for redo
        self.new_row_data = self.mw.df.iloc[self.row_idx].copy()
        self.mw.df = self.mw.df.drop(self.mw.df.index[self.row_idx]).reset_index(drop=True)
        self.mw.filtered_df = self.mw.df
        self.mw.update_table()

class DeleteRowCommand(QUndoCommand):
    def __init__(self, main_window, row_indices):
        super().__init__("Delete Row(s)")
        self.mw = main_window
        self.row_indices = sorted(row_indices, reverse=True)
        self.deleted_data = []

    def redo(self):
        self.deleted_data = []
        for idx in self.row_indices:
            self.deleted_data.append((idx, self.mw.df.iloc[idx].copy()))
        
        self.mw.df = self.mw.df.drop(self.mw.df.index[self.row_indices]).reset_index(drop=True)
        self.mw.filtered_df = self.mw.df
        self.mw.update_table()

    def undo(self):
        # Restore in reverse order of deletion (which is chronological order of addition because we sorted reverse=True)
        for idx, row_data in reversed(self.deleted_data):
             self.mw.df = pd.concat([self.mw.df.iloc[:idx], 
                                    pd.DataFrame([row_data], columns=self.mw.df.columns), 
                                    self.mw.df.iloc[idx:]]).reset_index(drop=True)
        self.mw.filtered_df = self.mw.df
        self.mw.update_table()

class AddColumnCommand(QUndoCommand):
    def __init__(self, main_window, col_name, dtype='object'):
        super().__init__(f"Add Column '{col_name}'")
        self.mw = main_window
        self.col_name = col_name
        self.dtype = dtype

    def redo(self):
        self.mw.df[self.col_name] = pd.Series([None] * len(self.mw.df), dtype=self.dtype)
        self.mw.filtered_df = self.mw.df
        self.mw.update_table()

    def undo(self):
        self.mw.df = self.mw.df.drop(columns=[self.col_name])
        self.mw.filtered_df = self.mw.df
        self.mw.update_table()

class DeleteColumnCommand(QUndoCommand):
    def __init__(self, main_window, col_indices):
        super().__init__("Delete Column(s)")
        self.mw = main_window
        self.col_indices = col_indices
        self.col_names = [self.mw.df.columns[i] for i in col_indices]
        self.deleted_data = {}

    def redo(self):
        for name in self.col_names:
            self.deleted_data[name] = self.mw.df[name].copy()
        self.mw.df = self.mw.df.drop(columns=self.col_names)
        self.mw.filtered_df = self.mw.df
        self.mw.update_table()

    def undo(self):
        for name in self.col_names:
            self.mw.df[name] = self.deleted_data[name]
        self.mw.filtered_df = self.mw.df
        self.mw.update_table()
