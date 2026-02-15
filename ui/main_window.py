from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qdarkstyle # type: ignore
import pandas as pd
from ui.commands import EditCommand

import os
from data.parquet_handler import load_parquet, save_parquet, get_metadata, get_row_count
from ui.visualization_widget import VisualizationWidget

class CustomDelegate(QStyledItemDelegate):
    def setEditorData(self, editor, index):
        if isinstance(editor, QLineEdit):
            # Get full text for editing
            source_index = index.model().mapToSource(index)
            full_value = str(source_index.model().df.iloc[source_index.row(), source_index.column()])
            editor.setText(full_value)

class DataFrameModel(QAbstractTableModel):
    def __init__(self, df, main_df, main_window=None):
        super().__init__()
        self.df = df
        self.main_df = main_df
        self.main_window = main_window

    def rowCount(self, parent):
        return len(self.df)

    def columnCount(self, parent):
        return len(self.df.columns)

    def data(self, index, role):
        value = str(self.df.iloc[index.row(), index.column()])
        if role == Qt.ItemDataRole.DisplayRole:
            if len(value) > 50:  # Truncate long text
                return value[:47] + "..."
            return value
        elif role == Qt.ItemDataRole.EditRole:
            return value  # Return full text for editing
        elif role == Qt.ItemDataRole.ToolTipRole:
            if len(value) > 50:
                return value  # Show full text in tooltip
            return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.df.columns[section]
            return str(section + 1)
        elif role == Qt.ItemDataRole.ToolTipRole:
            if orientation == Qt.Orientation.Horizontal:
                meta = get_metadata(self.df, section)
                return f"Type: {meta['type']}, Nullable: {meta['nullable']}"

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            row_idx = self.df.index[index.row()]
            col = self.df.columns[index.column()]
            dtype = self.main_df[col].dtype
            try:
                if dtype == 'int64':
                    value = int(value)
                elif dtype == 'float64':
                    value = float(value)
                elif dtype == 'object':
                    value = str(value)
                
                # Capture old value for undo
                old_value = self.df.iloc[index.row(), index.column()]
                
                if self.main_window and self.main_window.undo_stack:
                    command = EditCommand(self.main_window, index, old_value, value)
                    self.main_window.undo_stack.push(command)
                    return True
                else:
                    return self.set_data_internal(index, value)

            except ValueError as e:
                QMessageBox.warning(self.window(), "Edit Error", f"Invalid value for {dtype}: {str(e)}")
                return False
        return False

    def set_data_internal(self, index, value):
        row_idx = self.df.index[index.row()]
        col = self.df.columns[index.column()]
        self.main_df.loc[row_idx, col] = value
        self.df.loc[row_idx, col] = value
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parquet Data Explorer")
        # Use absolute path for icon to work in snap environments
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 1200, 800)
        self.df = pd.DataFrame()
        self.filtered_df = self.df
        self.current_file_path = None
        self.proxy = QSortFilterProxyModel()
        self.original_df = None
        self.undo_stack = QUndoStack(self)
        self.create_table()
        self.create_query_widget()
        self.create_stats_widget()
        self.create_menu()
        self.status_bar = self.statusBar()
        self.row_col_label = QLabel()
        self.status_bar.addPermanentWidget(self.row_col_label)
        
        # Pagination controls
        self.page_size = 1000
        self.current_page = 1
        self.total_rows = 0
        self.create_pagination_controls()

        if os.path.exists('sample.parquet'):
            self.load_data('sample.parquet')
        self.status_bar.showMessage("Ready")

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        export_action = QAction("Export", self)
        export_action.triggered.connect(self.export_file)
        file_menu.addAction(export_action)

        edit_menu = menu_bar.addMenu("Edit")
        
        undo_action = self.undo_stack.createUndoAction(self, "Undo")
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)

        redo_action = self.undo_stack.createRedoAction(self, "Redo")
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.copy_selection)
        edit_menu.addAction(copy_action)
        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)

        view_menu = menu_bar.addMenu("View")
        self.query_action = QAction("Query Panel", self)
        self.query_action.setCheckable(True)
        self.query_action.setChecked(True)
        self.query_action.triggered.connect(lambda: self.query_dock.setVisible(self.query_action.isChecked()))
        self.query_dock.visibilityChanged.connect(lambda visible: self.query_action.setChecked(visible))
        view_menu.addAction(self.query_action)
        self.stats_action = QAction("Statistics Panel", self)
        self.stats_action.setCheckable(True)
        self.stats_action.setChecked(True)
        self.stats_action.triggered.connect(lambda: self.stats_dock.setVisible(self.stats_action.isChecked()))
        view_menu.addAction(self.stats_action)

        theme_menu = view_menu.addMenu("Theme")
        
        self.theme_group = QActionGroup(self)
        
        self.theme_group = QActionGroup(self)
        self.theme_group.setExclusive(True)
        
        for theme_name in ["Auto", "Dark", "Light"]:
            action = QAction(theme_name, self, checkable=True)
            if theme_name == "Auto": action.setChecked(True)
            action.triggered.connect(lambda checked, t=theme_name.lower(): self.change_theme(t))
            theme_menu.addAction(action)
            self.theme_group.addAction(action)

    def change_theme(self, theme_name):
        app = QApplication.instance()
        if theme_name == "dark":
            app.setStyleSheet(qdarkstyle.load_stylesheet())
        elif theme_name == "light":
            app.setStyleSheet("") # Reset to default (light)
        else: # Auto
            # Simple logic: default to light or check system (advanced)
            # For now, just reset
            app.setStyleSheet("")

    def copy_selection(self):
        selection = self.table.selectionModel().selectedIndexes()
        if not selection:
            return
        rows = sorted(set(index.row() for index in selection))
        cols = sorted(set(index.column() for index in selection))
        text = ""
        for row in rows:
            row_data = []
            for col in range(len(self.filtered_df.columns)):
                if any(index.row() == row and index.column() == col for index in selection):
                    row_data.append(str(self.filtered_df.iloc[row, col]))
                else:
                    row_data.append("")
            text += "\t".join(row_data) + "\n"
        QApplication.clipboard().setText(text)

    def select_all(self):
        self.table.selectAll()

    def create_table(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.table = QTableView()
        self.table.setSortingEnabled(True)
        
        self.visualization_widget = VisualizationWidget()

        self.tabs.addTab(self.table, "Data")
        self.tabs.addTab(self.visualization_widget, "Visualizations")

    def create_query_widget(self):
        self.query_edit = QLineEdit()
        self.query_edit.setPlaceholderText("Example: age > 25 or city == 'NY'")
        self.query_button = QPushButton("Execute")
        self.query_button.clicked.connect(self.execute_query)
        self.query_button.setMinimumWidth(80)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search text...")
        self.search_edit.setMaximumWidth(150)
        self.search_edit.setMinimumWidth(100)
        self.search_edit.textChanged.connect(self.filter_data)
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Search:"))
        layout.addWidget(self.search_edit)
        layout.addWidget(QLabel("Pandas Query:"))
        layout.addWidget(self.query_edit, 1)  # stretch
        layout.addWidget(self.query_button)
        self.reset_button = QPushButton("Clear")
        self.reset_button.clicked.connect(self.reset_data)
        layout.addWidget(self.reset_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.query_dock = QDockWidget("Query", self)
        self.query_dock.setWidget(widget)
        # Fix the dock position - allow closing but not moving/floating
        self.query_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.query_dock)

    def create_stats_widget(self):
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_dock = QDockWidget("Statistics", self)
        self.stats_dock.setWidget(self.stats_text)
        # Fix the dock position - allow closing but not moving/floating
        self.stats_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.stats_dock)
        # self.tabifyDockWidget(self.query_dock, self.stats_dock)

    def create_pagination_controls(self):
        # Container for all status bar controls
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 10, 0)
        
        # Page Size Selector
        layout.addWidget(QLabel("Page Size:"))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["100", "1000", "5000", "10000"])
        self.page_size_combo.setCurrentText(str(self.page_size))
        self.page_size_combo.currentTextChanged.connect(lambda text: self.set_page_size(int(text)))
        layout.addWidget(self.page_size_combo)
        
        # Spacer
        layout.addSpacing(20)

        # Navigation
        self.prev_btn = QPushButton("<")
        self.prev_btn.setFixedWidth(30)
        self.prev_btn.clicked.connect(lambda: self.change_page(-1))
        
        self.page_label = QLabel("Page 1")
        
        self.next_btn = QPushButton(">")
        self.next_btn.setFixedWidth(30)
        self.next_btn.clicked.connect(lambda: self.change_page(1))
        
        layout.addWidget(self.prev_btn)
        layout.addWidget(self.page_label)
        layout.addWidget(self.next_btn)
        container.setLayout(layout)
        
        self.status_bar.addPermanentWidget(container)
        self.update_pagination_controls()

    def set_page_size(self, size):
        self.page_size = size
        self.current_page = 1
        if self.current_file_path:
            self.load_data(self.current_file_path, reset_page=False)

    def change_page(self, delta):
        self.current_page += delta
        if self.current_file_path:
            self.load_data(self.current_file_path, reset_page=False)

    def update_pagination_controls(self):
        import math
        total_pages = math.ceil(self.total_rows / self.page_size) if self.total_rows > 0 else 1
        
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)
        self.page_label.setText(f"Page {self.current_page} / {total_pages}")

    def filter_data(self):
        text = self.search_edit.text().lower()
        if not text:
            self.filtered_df = self.df
        else:
            self.filtered_df = self.df[self.df.apply(lambda row: text in str(row.values).lower(), axis=1)]
        self.update_table()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Parquet File", "", "Parquet Files (*.parquet)")
        if file_name:
            self.load_data(file_name)

    def load_data(self, file_name, reset_page=True):
        self.status_bar.showMessage("Loading...")
        try:
            self.total_rows = get_row_count(file_name)
            
            if reset_page:
                self.current_page = 1
            
            offset = (self.current_page - 1) * self.page_size
            limit = self.page_size
            
            self.df = load_parquet(file_name, offset=offset, limit=limit)
            self.original_df = self.df.copy()
            self.filtered_df = self.df
            self.current_file_path = file_name
            self.undo_stack.clear() # Clear undo stack on new data load
            self.update_table()
            self.update_pagination_controls()
            self.status_bar.showMessage(f"Loaded {len(self.df)} rows (Total: {self.total_rows})")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
            self.status_bar.showMessage("Error loading file")

    def refresh_view_for_cell(self, row_idx, col_name):
        # row_idx is the DataFrame Index Label, not position
        # col_name is column name
        try:
            # Find the positional index in the CURRENT filtered_df
            if row_idx not in self.filtered_df.index:
                return 
            
            row_pos = self.filtered_df.index.get_loc(row_idx)
            col_pos = self.filtered_df.columns.get_loc(col_name)
            
            # Emit dataChanged for this cell in the source model
            index = self.model.index(row_pos, col_pos)
            self.model.dataChanged.emit(index, index)
        except Exception as e:
            print(f"Error refreshing view: {e}")

    def update_table(self):
        self.model = DataFrameModel(self.filtered_df, self.df, self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.setItemDelegate(CustomDelegate())
        # Set maximum column width to 250 pixels
        max_col_width = 250
        for col in range(len(self.filtered_df.columns)):
            self.table.setColumnWidth(col, min(self.table.columnWidth(col), max_col_width))
        self.row_col_label.setText(f"Rows: {len(self.filtered_df)}, Columns: {len(self.filtered_df.columns)}")
        self.update_stats()
        self.visualization_widget.set_dataframe(self.filtered_df)

    def update_stats(self):
        if self.df.empty:
            self.stats_text.setPlainText("No data loaded.")
            return
        desc = self.df.describe(include='all')
        text = "Column Statistics:\n\n"
        for col in self.df.columns:
            text += f"{col}:\n"
            if col in desc.columns:
                col_desc = desc[col]
                text += f"  Count: {col_desc['count']}\n"
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    text += f"  Mean: {col_desc.get('mean', 'N/A')}\n"
                    text += f"  Std: {col_desc.get('std', 'N/A')}\n"
                    text += f"  Min: {col_desc.get('min', 'N/A')}\n"
                    text += f"  25%: {col_desc.get('25%', 'N/A')}\n"
                    text += f"  50%: {col_desc.get('50%', 'N/A')}\n"
                    text += f"  75%: {col_desc.get('75%', 'N/A')}\n"
                    text += f"  Max: {col_desc.get('max', 'N/A')}\n"
                else:
                    text += f"  Unique: {col_desc.get('unique', 'N/A')}\n"
                    text += f"  Top: {col_desc.get('top', 'N/A')}\n"
                    text += f"  Freq: {col_desc.get('freq', 'N/A')}\n"
            text += "\n"
        self.stats_text.setPlainText(text)

    def save_file(self):
        if self.current_file_path:
            save_parquet(self.df, self.current_file_path)
            self.status_bar.showMessage("Saved")
        else:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Parquet File", "", "Parquet Files (*.parquet)")
            if file_name:
                save_parquet(self.df, file_name)
                self.current_file_path = file_name
                self.status_bar.showMessage("Saved")

    def new_file(self):
        self.df = pd.DataFrame()
        self.original_df = None
        self.filtered_df = self.df
        self.current_file_path = None
        self.update_table()
        self.status_bar.showMessage("New file created")

    def export_file(self):
        formats = ["CSV", "JSON", "Excel"]
        format, ok = QInputDialog.getItem(self, "Export Format", "Choose format:", formats, 0, False)
        if ok:
            ext = format.lower()
            file_name, _ = QFileDialog.getSaveFileName(self, f"Export to {format}", "", f"{format} Files (*.{ext})")
            if file_name:
                if format == "CSV":
                    self.df.to_csv(file_name, index=False)
                elif format == "JSON":
                    self.df.to_json(file_name, orient='records')
                elif format == "Excel":
                    self.df.to_excel(file_name, index=False)
                self.status_bar.showMessage("Exported")

    def execute_query(self):
        query = self.query_edit.text().strip()
        if not query:
            return
        try:
            # Use pandas query method for filtering
            # Example: column_name > 100, column_name == 'value'
            result = self.df.query(query)
            self.filtered_df = result
            self.update_table()
            self.status_bar.showMessage("Query executed")
        except Exception as e:
            QMessageBox.warning(self, "Query Error", f"Invalid pandas query: {str(e)}\n\nExample: column_name > 100 or column_name == 'value'")

    def reset_data(self):
        if self.original_df is not None:
            self.df = self.original_df.copy()
            self.filtered_df = self.df
            self.update_table()
            self.search_edit.clear()
            self.query_edit.clear()
            self.status_bar.showMessage("Data reset to original")