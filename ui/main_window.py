from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import pandas as pd
from ui.commands import EditCommand, AddRowCommand, DeleteRowCommand, AddColumnCommand, DeleteColumnCommand
from ui.styles import get_dark_stylesheet, get_light_stylesheet

import os
from data.parquet_handler import load_parquet, save_parquet, get_metadata, get_row_count
from ui.visualization_widget import VisualizationWidget

class StyledComboBox(QComboBox):
    """Custom combo box with visible dropdown arrow indicator"""
    def paintEvent(self, event):
        """Paint the combo box with a visible dropdown arrow"""
        super().paintEvent(event)

class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        """Custom painting for table cells with improved styling"""
        painter.save()
        
        # Draw background
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            text_color = option.palette.highlightedText().color()
        else:
            # Handle alternating background colors
            if index.row() % 2 == 1:
                painter.fillRect(option.rect, option.palette.alternateBase())
            else:
                painter.fillRect(option.rect, option.palette.base())
            text_color = option.palette.text().color()
        
        # Draw text
        painter.setPen(text_color)
        painter.setFont(option.font)
        
        # Draw cell text with proper padding
        text = str(index.data(Qt.ItemDataRole.DisplayRole) or "")
        margin = 4
        text_rect = option.rect.adjusted(margin, 0, -margin, 0)
        painter.drawText(text_rect, Qt.TextFlag.TextDontClip | Qt.AlignmentFlag.AlignVCenter, text)
        painter.restore()
    
    def createEditor(self, parent, option, index):
        """Create editor widget with better styling"""
        editor = QLineEdit(parent)
        return editor
    
    def setEditorData(self, editor, index):
        """Set editor data with full text for editing"""
        if isinstance(editor, QLineEdit):
            # Get full text for editing
            source_index = index.model().mapToSource(index)
            full_value = str(source_index.model().df.iloc[source_index.row(), source_index.column()])
            editor.setText(full_value)
            editor.selectAll()  # Select all text for convenience
    
    def setModelData(self, editor, model, index):
        """Set model data after editing, ensuring we reach the source model"""
        if isinstance(editor, QLineEdit):
            # If the model is a proxy, we want to call setData on the source model
            if hasattr(model, 'sourceModel'):
                source_model = model.sourceModel()
                source_index = model.mapToSource(index)
                source_model.setData(source_index, editor.text(), Qt.ItemDataRole.EditRole)
            else:
                model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)

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
            if self.main_window:
                self.main_window._manual_dirty = True

            row_idx = self.df.index[index.row()]
            col = self.df.columns[index.column()]
            dtype = self.df[col].dtype # Use df dtype as fallback
            if self.main_df is not None and col in self.main_df.columns:
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
                    self.main_window.update_window_title()
                    return True
                else:
                    return self.set_data_internal(index, value)

            except ValueError as e:
                QMessageBox.warning(self.main_window, "Edit Error", f"Invalid value for {dtype}: {str(e)}")
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
    def __init__(self, file_path=None):
        super().__init__()
        self.setWindowTitle("Parquet Explorer [*]")
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
        self.undo_stack.cleanChanged.connect(lambda _: self.update_window_title())
        self.undo_stack.indexChanged.connect(lambda _: self.update_window_title())
        # Add a property to track if there were EVER changes (backup logic)
        self._manual_dirty = False 
        self.base_font_size = 11
        self.current_theme = "auto"
        self.create_table()
        self.create_query_widget()
        self.create_stats_widget()
        self.create_menu()
        self.status_bar = self.statusBar()
        self.row_col_label = QLabel()
        self.status_bar.addPermanentWidget(self.row_col_label)
        
        # Compact Font Zoom Controls in Status Bar
        zoom_in_btn = QPushButton("A+")
        zoom_in_btn.setObjectName("zoomButton")
        zoom_in_btn.setToolTip("Zoom In Data Font")
        zoom_in_btn.clicked.connect(lambda: self.change_font_size(1))
        
        zoom_out_btn = QPushButton("A-")
        zoom_out_btn.setObjectName("zoomButton")
        zoom_out_btn.setToolTip("Zoom Out Data Font")
        zoom_out_btn.clicked.connect(lambda: self.change_font_size(-1))
        
        self.status_bar.addPermanentWidget(zoom_out_btn)
        self.status_bar.addPermanentWidget(zoom_in_btn)
        
        # Connect header signals for selection
        self.table.horizontalHeader().setSectionsClickable(True)
        self.table.verticalHeader().setSectionsClickable(True)
        self.table.horizontalHeader().sectionClicked.connect(self.on_horizontal_header_clicked)
        self.table.verticalHeader().sectionClicked.connect(self.on_vertical_header_clicked)
        
        # Header Context Menus
        self.table.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.verticalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.horizontalHeader().customContextMenuRequested.connect(self.show_column_context_menu)
        self.table.verticalHeader().customContextMenuRequested.connect(self.show_row_context_menu)
        
        # Pagination controls
        self.page_size = 1000
        self.current_page = 1
        self.total_rows = 0
        self.create_pagination_controls()

        if file_path and os.path.exists(file_path):
            self.load_data(file_path)
        elif os.path.exists('sample.parquet'):
            self.load_data('sample.parquet')
        
        self.apply_current_style()
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
        self.theme_group.setExclusive(True)
        
        for theme_name in ["Auto", "Dark", "Light"]:
            action = QAction(theme_name, self, checkable=True)
            if theme_name == "Auto": action.setChecked(True)
            action.triggered.connect(lambda checked, t=theme_name.lower(): self.change_theme(t))
            theme_menu.addAction(action)
            self.theme_group.addAction(action)

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_current_style()

    def change_font_size(self, delta):
        """Update the base font size and re-apply stylesheet"""
        new_size = self.base_font_size + delta
        if 8 <= new_size <= 24:
            self.base_font_size = new_size
            self.apply_current_style()
            self.status_bar.showMessage(f"Font size set to {self.base_font_size}px", 2000)

    def apply_current_style(self):
        """Helper to apply current theme with dynamic font size"""
        app = QApplication.instance()
        if self.current_theme == "dark":
            app.setStyleSheet(get_dark_stylesheet(font_size=self.base_font_size))
        elif self.current_theme == "light":
            app.setStyleSheet(get_light_stylesheet(font_size=self.base_font_size))
        else: # Auto
            # Default to dark theme for modern appearance
            app.setStyleSheet(get_dark_stylesheet(font_size=self.base_font_size))

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
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.PenStyle.SolidLine)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Improve margins and spacing
        self.table.verticalHeader().setDefaultSectionSize(32)
        self.table.horizontalHeader().setDefaultSectionSize(100)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionsClickable(True)
        self.table.verticalHeader().setSectionsClickable(True)
        
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
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(12)
        
        # Page Size Selector
        size_label = QLabel("Page Size:")
        layout.addWidget(size_label)
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["100", "1000", "5000", "10000"])
        self.page_size_combo.setCurrentText(str(self.page_size))
        self.page_size_combo.currentTextChanged.connect(lambda text: self.set_page_size(int(text)))
        self.page_size_combo.setMinimumWidth(80)
        layout.addWidget(self.page_size_combo)
        
        # Spacer
        layout.addSpacing(20)

        # Navigation
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(30, 24)
        self.prev_btn.setToolTip("Previous Page")
        self.prev_btn.clicked.connect(lambda: self.change_page(-1))
        
        self.page_label = QLabel("Page 1")
        
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(30, 24)
        self.next_btn.setToolTip("Next Page")
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
            self.undo_stack.setClean()
            self._manual_dirty = False
            self.update_table()
            self.update_window_title()
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

    def on_horizontal_header_clicked(self, logical_index):
        """Select entire column when header is clicked, supporting multi-selection"""
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            # Use MultiSelection mode temporarily to toggle without clearing others
            old_mode = self.table.selectionMode()
            self.table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
            self.table.selectColumn(logical_index)
            self.table.setSelectionMode(old_mode)
        elif modifiers == Qt.KeyboardModifier.ShiftModifier:
            self.table.selectColumn(logical_index)
        else:
            self.table.selectColumn(logical_index)

    def on_vertical_header_clicked(self, logical_index):
        """Select entire row when vertical header is clicked, supporting multi-selection"""
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            # Use MultiSelection mode temporarily to toggle without clearing others
            old_mode = self.table.selectionMode()
            self.table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
            self.table.selectRow(logical_index)
            self.table.setSelectionMode(old_mode)
        else:
            self.table.selectRow(logical_index)

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
        try:
            if self.current_file_path:
                save_parquet(self.df, self.current_file_path)
                self.undo_stack.setClean()
                self._manual_dirty = False
                self.status_bar.showMessage("Saved", 3000)
                self.update_window_title()
                return True
            else:
                file_name, _ = QFileDialog.getSaveFileName(self, "Save Parquet File", "", "Parquet Files (*.parquet)")
                if file_name:
                    save_parquet(self.df, file_name)
                    self.current_file_path = file_name
                    self.undo_stack.setClean()
                    self.status_bar.showMessage("Saved", 3000)
                    self.update_window_title()
                    return True
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save file: {str(e)}")
        return False

    def update_window_title(self, *args):
        try:
            # Atomic safety check for C++ object destruction
            if not hasattr(self, 'undo_stack') or self.undo_stack is None:
                return
            # Force check if it's actually alive
            _foo = self.undo_stack.isClean()
        except (RuntimeError, AttributeError):
            return

        title = "Parquet Explorer"
        if self.current_file_path:
            title += f" - {os.path.basename(self.current_file_path)}"
        
        is_modified = not self.undo_stack.isClean() or self._manual_dirty
        
        if is_modified:
            title += " [Modified]"
        
        # Restore placeholder for setWindowModified logic
        full_title = title + " [*]"
        if self.windowTitle() != full_title:
            self.setWindowTitle(full_title)
            
        self.setWindowModified(is_modified)

    def new_file(self):
        self.df = pd.DataFrame()
        self.original_df = None
        self.filtered_df = self.df
        self.current_file_path = None
        self.undo_stack.clear()
        self.update_table()
        self.update_window_title()
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

    def show_row_context_menu(self, pos):
        menu = QMenu(self)
        
        add_row_act = QAction("Add Row", self)
        add_row_act.triggered.connect(self.add_row)
        menu.addAction(add_row_act)
        
        delete_row_act = QAction("Delete Selected Row(s)", self)
        delete_row_act.triggered.connect(self.delete_selected_rows)
        menu.addAction(delete_row_act)
        
        menu.exec(self.table.verticalHeader().viewport().mapToGlobal(pos))

    def show_column_context_menu(self, pos):
        menu = QMenu(self)
        
        add_col_act = QAction("Add Column", self)
        add_col_act.triggered.connect(self.add_column)
        menu.addAction(add_col_act)
        
        delete_col_act = QAction("Delete Selected Column(s)", self)
        delete_col_act.triggered.connect(self.delete_selected_columns)
        menu.addAction(delete_col_act)
        
        menu.exec(self.table.horizontalHeader().viewport().mapToGlobal(pos))

    def add_row(self):
        selection = self.table.selectionModel().selectedRows()
        row_idx = selection[0].row() if selection else len(self.df)
        command = AddRowCommand(self, row_idx)
        self.undo_stack.push(command)
        self._manual_dirty = True
        self.update_window_title()

    def delete_selected_rows(self):
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            return
        row_indices = [idx.row() for idx in selection if idx.row() < len(self.df)]
        if not row_indices:
            return
            
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                     f"Are you sure you want to delete {len(row_indices)} row(s)?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            command = DeleteRowCommand(self, row_indices)
            self.undo_stack.push(command)
            self._manual_dirty = True
            self.update_window_title()

    def add_column(self):
        name, ok = QInputDialog.getText(self, "Add Column", "Column Name:")
        if ok and name:
            if name in self.df.columns:
                QMessageBox.warning(self, "Error", "Column already exists")
                return
            
            types = ["object", "int64", "float64"]
            dtype, ok = QInputDialog.getItem(self, "Column Type", "Select type:", types, 0, False)
            if ok:
                command = AddColumnCommand(self, name, dtype)
                self.undo_stack.push(command)
                self._manual_dirty = True
                self.update_window_title()

    def delete_selected_columns(self):
        selection = self.table.selectionModel().selectedColumns()
        if not selection:
            # Check if cells are selected and get columns from them
            selected_indexes = self.table.selectionModel().selectedIndexes()
            col_indices = list(set(idx.column() for idx in selected_indexes))
        else:
            col_indices = [idx.column() for idx in selection]
            
        if not col_indices:
            return
            
        col_names = [self.df.columns[i] for i in col_indices]
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                     f"Are you sure you want to delete column(s): {', '.join(col_names)}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            command = DeleteColumnCommand(self, col_indices)
            self.undo_stack.push(command)
            self._manual_dirty = True
            self.update_window_title()

    def closeEvent(self, event):
        # Force any active edit to commit
        if self.table.model():
            self.table.clearFocus() 
            QApplication.processEvents()
            
        is_modified = False
        try:
            is_modified = not self.undo_stack.isClean() or self._manual_dirty
        except RuntimeError:
            pass
        
        if is_modified:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Unsaved Changes")
            msg_box.setText("The data has been modified.")
            msg_box.setInformativeText("Do you want to save your changes before closing?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Save | 
                                      QMessageBox.StandardButton.Discard | 
                                      QMessageBox.StandardButton.Cancel)
            msg_box.setDefaultButton(QMessageBox.StandardButton.Save)
            msg_box.setIcon(QMessageBox.Icon.Question)

            ret = msg_box.exec()
            
            if ret == QMessageBox.StandardButton.Save:
                if self.save_file():
                    # Disconnect signals before accepting to prevent RuntimeError
                    self._safe_disconnect()
                    event.accept()
                else:
                    event.ignore()
            elif ret == QMessageBox.StandardButton.Discard:
                self._safe_disconnect()
                event.accept()
            else: # Cancel
                event.ignore()
        else:
            self._safe_disconnect()
            event.accept()

    def _safe_disconnect(self):
        """Safely disconnect signals before destruction"""
        try:
            self.undo_stack.cleanChanged.disconnect()
            self.undo_stack.indexChanged.disconnect()
        except:
            pass
