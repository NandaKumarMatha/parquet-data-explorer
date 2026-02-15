from PyQt6.QtGui import QUndoCommand

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
