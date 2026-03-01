from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QComboBox, 
                             QCheckBox, QSpinBox, QLabel, QGroupBox)
from PyQt6.QtCore import pyqtSignal

class PlotConfigWidget(QWidget):
    config_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Style Group
        style_group = QGroupBox("Aesthetics")
        style_form = QFormLayout()
        
        self.color_col_combo = QComboBox()
        self.color_col_combo.addItem("None")
        style_form.addRow("Color Column:", self.color_col_combo)
        
        self.size_col_combo = QComboBox()
        self.size_col_combo.addItem("None")
        style_form.addRow("Size Column:", self.size_col_combo)
        
        self.size_max_spin = QSpinBox()
        self.size_max_spin.setRange(10, 200)
        self.size_max_spin.setValue(60)
        style_form.addRow("Max Marker Size:", self.size_max_spin)
        
        style_group.setLayout(style_form)
        layout.addWidget(style_group)

        # Interactivity Group
        interact_group = QGroupBox("Interactivity")
        interact_form = QFormLayout()
        
        self.hover_col_combo = QComboBox()
        self.hover_col_combo.addItem("None")
        interact_form.addRow("Hover Name:", self.hover_col_combo)
        
        interact_group.setLayout(interact_form)
        layout.addWidget(interact_group)

        # Axis Group
        axis_group = QGroupBox("Axis Configuration")
        axis_form = QFormLayout()
        
        self.log_x_cb = QCheckBox("Log X Axis")
        self.log_y_cb = QCheckBox("Log Y Axis")
        axis_form.addRow(self.log_x_cb)
        axis_form.addRow(self.log_y_cb)
        
        self.z_col_combo = QComboBox()
        self.z_col_combo.addItem("None")
        self.z_label = QLabel("Z Column (3D):")
        axis_form.addRow(self.z_label, self.z_col_combo)
        
        axis_group.setLayout(axis_form)
        layout.addWidget(axis_group)

        layout.addStretch()
        self.setLayout(layout)

        # Connect signals
        for cb in [self.color_col_combo, self.size_col_combo, self.hover_col_combo, self.z_col_combo]:
            cb.currentIndexChanged.connect(self.emit_config)
        
        for chk in [self.log_x_cb, self.log_y_cb]:
            chk.toggled.connect(self.emit_config)
            
        self.size_max_spin.valueChanged.connect(self.emit_config)

    def set_columns(self, columns):
        widgets = [self.color_col_combo, self.size_col_combo, self.hover_col_combo, self.z_col_combo]
        for w in widgets:
            current = w.currentText()
            w.clear()
            w.addItem("None")
            w.addItems(columns)
            index = w.findText(current)
            if index >= 0:
                w.setCurrentIndex(index)

    def get_config(self):
        return {
            "color": self.color_col_combo.currentText() if self.color_col_combo.currentText() != "None" else None,
            "size": self.size_col_combo.currentText() if self.size_col_combo.currentText() != "None" else None,
            "size_max": self.size_max_spin.value(),
            "hover_name": self.hover_col_combo.currentText() if self.hover_col_combo.currentText() != "None" else None,
            "log_x": self.log_x_cb.isChecked(),
            "log_y": self.log_y_cb.isChecked(),
            "z": self.z_col_combo.currentText() if self.z_col_combo.currentText() != "None" else None
        }

    def emit_config(self):
        self.config_changed.emit(self.get_config())
