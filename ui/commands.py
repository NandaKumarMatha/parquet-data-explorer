from PyQt6.QtGui import QUndoCommand

class EditCommand(QUndoCommand):
    def __init__(self, model, index, old_value, new_value):
        super().__init__(f"Edit cell {index.row()},{index.column()}")
        self.model = model
        self.index = index
        self.old_value = old_value
        self.new_value = new_value

    def redo(self):
        self.model.set_data_internal(self.index, self.new_value)

    def undo(self):
        self.model.set_data_internal(self.index, self.old_value)
