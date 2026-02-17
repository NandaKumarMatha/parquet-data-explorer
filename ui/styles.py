"""
Modern stylesheet definitions for Parquet Viewer
Provides modern, clean UI with proper theming support
"""

# Modern Dark Theme - Professional and clean
DARK_STYLESHEET = """
QMainWindow {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

/* Menu and MenuBar */
QMenuBar {
    background-color: #252525;
    color: #e0e0e0;
    border-bottom: 1px solid #3d3d3d;
    padding: 4px;
}

QMenuBar::item:selected {
    background-color: #3d7efb;
    color: white;
    border-radius: 3px;
}

QMenu {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #3d7efb;
    color: white;
    padding: 4px 20px;
}

/* Dock Widgets */
QDockWidget {
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
}

QDockWidget::title {
    background-color: #252525;
    padding: 8px;
    border: 1px solid #3d3d3d;
    border-radius: 4px 4px 0px 0px;
    font-weight: 600;
    font-size: 11px;
}

QDockWidget::close-button {
    background-color: #252525;
    border-radius: 3px;
    margin: 4px;
}  

QDockWidget::close-button:hover {
    background-color: #3d3d3d;
}

QDockWidget::close-button:pressed {
    background-color: #4a4a4a;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    background-color: #1e1e1e;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #b0b0b0;
    padding: 8px 20px;
    border: 1px solid #3d3d3d;
    border-bottom: none;
    border-radius: 4px 4px 0px 0px;
    margin-right: 2px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #3d7efb;
    color: white;
    border: 1px solid #3d7efb;
}

QTabBar::tab:hover:!selected {
    background-color: #353535;
    color: #e0e0e0;
}

/* Table View */
QTableView {
    background-color: #2a2a2a;
    alternate-background-color: #1f1f1f;
    gridline-color: #3d3d3d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
}

QTableView::item {
    padding: 5px 8px;
    border: none;
    margin: 0px;
    height: 32px;
}

QTableView::item:alternate {
    background-color: #1f1f1f;
}

QTableView::item:selected {
    background-color: #3d7efb;
    color: white;
    border: 1px solid #4a8bff;
}

QTableView::item:hover {
    background-color: #353535;
}

QHeaderView::section {
    background-color: #1f1f1f;
    color: #ffffff;
    padding: 8px 6px;
    border: none;
    border-right: 1px solid #3d3d3d;
    border-bottom: 2px solid #3d7efb;
    font-weight: 700;
    font-size: 11px;
}

QHeaderView::section:hover {
    background-color: #2a4a7e;
}

/* Buttons */
QPushButton {
    background-color: #3d7efb;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    font-weight: 600;
    font-size: 11px;
    min-height: 24px;
}

QPushButton:hover {
    background-color: #4a8bff;
}

QPushButton:pressed {
    background-color: #2a5fd4;
}

QPushButton:disabled {
    background-color: #555555;
    color: #888888;
}

/* Line Edit and Text Input */
QLineEdit, QTextEdit {
    background-color: #252525;
    color: #e0e0e0;
    border: 1px solid #447bed;
    border-radius: 4px;
    padding: 7px 8px;
    selection-background-color: #3d7efb;
    selection-color: white;
    font-size: 11px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #3d7efb;
    padding: 6px 7px;
    background-color: #2d2d2d;
}

/* Combo Box */
QComboBox {
    background-color: #252525;
    color: #e0e0e0;
    border: 1px solid #447bed;
    border-radius: 4px;
    padding: 6px 40px 6px 8px;
    font-size: 11px;
    min-height: 24px;
    appearance: none;
}

QComboBox:hover {
    background-color: #2d2d2d;
    border: 1px solid #4a8bff;
}

QComboBox:focus {
    border: 2px solid #3d7efb;
    padding: 5px 39px 5px 7px;
    background-color: #2d2d2d;
}

QComboBox::drop-down {
    border: none;
    background-color: #3d7efb;
    width: 38px;
    height: 100%;
    border-radius: 0px 3px 3px 0px;
    subcontrol-origin: border;
    subcontrol-position: right;
    border-left: 2px solid #3d7efb;
    margin: 1px 1px 1px 0px;
    padding: 0px 6px;
}

QComboBox::down-arrow {
    width: 16px;
    height: 16px;
    image: url(none);
    background: transparent;
}

QAbstractItemView {
    background-color: #2a2a2a;
    color: #e0e0e0;
    selection-background-color: #3d7efb;
    selection-color: white;
    border: 1px solid #447bed;
    outline: none;
    border-radius: 4px;
    padding: 4px;
    margin: 4px;
}

QAbstractItemView::item {
    padding: 6px 8px;
    border-radius: 3px;
    margin: 2px 0px;
}

QAbstractItemView::item:hover {
    background-color: #353535;
}

QAbstractItemView::item:selected {
    background-color: #3d7efb;
    color: white;
    border-radius: 3px;
}

/* Label */
QLabel {
    color: #e0e0e0;
    font-size: 11px;
    font-weight: 500;
}

/* StatusBar */
QStatusBar {
    background-color: #252525;
    color: #e0e0e0;
    border-top: 1px solid #3d3d3d;
    padding: 4px;
}

/* ScrollBar */
QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #454545;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #555555;
}

QScrollBar:horizontal {
    background-color: #1e1e1e;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #454545;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #555555;
}
"""

# Modern Light Theme - Clean and professional
LIGHT_STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
    color: #333333;
}

QWidget {
    background-color: #f5f5f5;
    color: #333333;
}

/* Menu and MenuBar */
QMenuBar {
    background-color: #ffffff;
    color: #333333;
    border-bottom: 1px solid #e0e0e0;
    padding: 4px;
}

QMenuBar::item:selected {
    background-color: #3d7efb;
    color: white;
    border-radius: 3px;
}

QMenu {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #3d7efb;
    color: white;
    padding: 4px 20px;
}

/* Dock Widgets */
QDockWidget {
    color: #333333;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
}

QDockWidget::title {
    background-color: #ffffff;
    padding: 6px;
    border: 1px solid #e0e0e0;
    border-radius: 4px 4px 0px 0px;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f5f5f5;
}

QTabBar::tab {
    background-color: #eeeeee;
    color: #333333;
    padding: 8px 20px;
    border: 1px solid #e0e0e0;
    border-bottom: none;
    border-radius: 4px 4px 0px 0px;
    margin-right: 2px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #3d7efb;
    color: white;
    border: 1px solid #3d7efb;
}

QTabBar::tab:hover:!selected {
    background-color: #e0e0e0;
    color: #333333;
}

/* Table View */
QTableView {
    background-color: #ffffff;
    alternate-background-color: #f9f9f9;
    gridline-color: #e8e8e8;
    color: #333333;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
}

QTableView::item {
    padding: 4px 6px;
    border: none;
    margin: 0px;
}

QTableView::item:alternate {
    background-color: #f5f5f5;
}

QTableView::item:selected {
    background-color: #3d7efb;
    color: white;
    border: 1px solid #2a5fd4;
}

QTableView::item:hover {
    background-color: #f0f0f0;
}

QHeaderView::section {
    background-color: #f0f0f0;
    color: #000000;
    padding: 8px 6px;
    border: none;
    border-right: 1px solid #e0e0e0;
    border-bottom: 2px solid #3d7efb;
    font-weight: 700;
    font-size: 11px;
}

QHeaderView::section:hover {
    background-color: #e6e6e6;
}

/* Buttons */
QPushButton {
    background-color: #3d7efb;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 7px 15px;
    font-weight: 600;
    font-size: 11px;
}

QPushButton:hover {
    background-color: #4a8bff;
}

QPushButton:pressed {
    background-color: #2a5fd4;
}

QPushButton:disabled {
    background-color: #d0d0d0;
    color: #808080;
}

/* Line Edit and Text Input */
QLineEdit, QTextEdit {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #b0d4ff;
    border-radius: 4px;
    padding: 7px 8px;
    selection-background-color: #3d7efb;
    selection-color: white;
    font-size: 11px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #3d7efb;
    padding: 6px 7px;
    background-color: #fafafa;
}

/* Combo Box */
QComboBox {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #b0d4ff;
    border-radius: 4px;
    padding: 6px 40px 6px 8px;
    font-size: 11px;
    min-height: 24px;
    appearance: none;
}

QComboBox:hover {
    background-color: #fafafa;
    border: 1px solid #3d7efb;
}

QComboBox:focus {
    border: 2px solid #3d7efb;
    padding: 5px 39px 5px 7px;
    background-color: #fafafa;
}

QComboBox::drop-down {
    border: none;
    background-color: #3d7efb;
    width: 38px;
    height: 100%;
    border-radius: 0px 3px 3px 0px;
    subcontrol-origin: border;
    subcontrol-position: right;
    border-left: 2px solid #3d7efb;
    margin: 1px 1px 1px 0px;
    padding: 0px 6px;
}

QComboBox::down-arrow {
    width: 16px;
    height: 16px;
    image: url(none);
    background: transparent;
}

QAbstractItemView {
    background-color: #f5f5f5;
    color: #333333;
    selection-background-color: #3d7efb;
    selection-color: white;
    border: 1px solid #b0d4ff;
    outline: none;
    border-radius: 4px;
    padding: 4px;
    margin: 4px;
}

QAbstractItemView::item {
    padding: 6px 8px;
    border-radius: 3px;
    margin: 2px 0px;
}

QAbstractItemView::item:hover {
    background-color: #e8f0ff;
}

QAbstractItemView::item:selected {
    background-color: #3d7efb;
    color: white;
    border-radius: 3px;
}

/* Label */
QLabel {
    color: #333333;
    font-size: 11px;
    font-weight: 500;
}

/* StatusBar */
QStatusBar {
    background-color: #ffffff;
    color: #333333;
    border-top: 1px solid #e0e0e0;
    padding: 4px;
}

/* ScrollBar */
QScrollBar:vertical {
    background-color: #f5f5f5;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #c0c0c0;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a8a8a8;
}

QScrollBar:horizontal {
    background-color: #f5f5f5;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #c0c0c0;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #a8a8a8;
}
"""

def get_dark_stylesheet():
    """Returns the modern dark theme stylesheet"""
    return DARK_STYLESHEET

def get_light_stylesheet():
    """Returns the modern light theme stylesheet"""
    return LIGHT_STYLESHEET
