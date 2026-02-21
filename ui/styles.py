# Professional Corporate Stylesheet for Parquet Viewer
# Adheres to the 60-30-10 Rule:
# - 60% Neutrals (Main Backgrounds)
# - 30% Secondary (Component Backgrounds/Panels)
# - 10% Accent (Action Colors/Focus)

# Modern Corporate Dark Theme Template
DARK_STYLESHEET_TEMPLATE = """
/* [60% BASE] - Main Application Window Background */
QMainWindow, QWidget#centralWidget {{
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-size: 11px;
}}

/* [30% SECONDARY] - Side Panels, Docks, and Toolbars */
QDockWidget, QMenuBar, QStatusBar, QTabWidget::pane {{
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    font-size: 11px;
}}

QLabel {{
    color: #e0e0e0;
}}

QMessageBox, QDialog {{
    background-color: #1e1e1e;
    color: #e0e0e0;
}}

QMessageBox QLabel {{
    color: #e0e0e0;
}}

/* [REFINED] Dock Widget Title and Buttons */
QDockWidget::title {{
    background-color: #353535;
    padding: 8px;
    font-weight: bold;
    border-bottom: 1px solid #3d3d3d;
}}

QDockWidget::close-button, QDockWidget::float-button {{
    background: #444444;
    border-radius: 3px;
    padding: 2px;
}}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
    background: #0078d4;
}}

/* [REFINED] Modern Streamlined Tabs */
QTabBar::tab {{
    background-color: transparent;
    color: #b0b0b0;
    padding: 6px 20px;
    border-bottom: 2px solid transparent;
    margin-right: 2px;
    font-weight: 500;
}}

QTabBar::tab:hover {{
    background-color: #3d3d3d;
    color: #ffffff;
}}

QTabBar::tab:selected {{
    background-color: #353535;
    color: #0078d4;
    border-bottom: 2px solid #0078d4;
    font-weight: 700;
}}

/* [30% SECONDARY] - Form Inputs and Widgets */
QLineEdit, QTextEdit, QComboBox {{
    background-color: #2d2d2d;
    border: 1px solid #454545;
    border-radius: 4px;
    padding: 4px;
    color: #e0e0e0;
    font-size: 11px;
}}

/* [DYNAMIC] - Table View Data Scaling */
QTableView, QTableView::item {{
    background-color: #2d2d2d;
    alternate-background-color: #353535;
    border: 1px solid #454545;
    border-radius: 4px;
    padding: 4px;
    color: #e0e0e0;
    font-size: {font_size}px;
}}

/* [10% ACCENT] - Interactive Elements & Branding Blue */
QPushButton {{
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 10px;
}}

QPushButton#zoomButton {{
    min-width: 24px;
    max-width: 24px;
    padding: 2px;
}}

QPushButton:hover {{
    background-color: #0086f0;
}}

QPushButton:pressed {{
    background-color: #005a9e;
}}

/* [10% ACCENT] - Selection and Focus Indicators */
QTableView::item:selected {{
    background-color: #0078d4;
    color: white;
}}

QHeaderView::section {{
    background-color: #353535;
    color: #ffffff;
    border: 1px solid #3d3d3d;
    padding: 6px;
    font-weight: bold;
    font-size: {font_size}px;
}}

QScrollBar::handle {{
    background-color: #444444;
    border-radius: 4px;
}}
"""

# Modern Corporate Light Theme Template
LIGHT_STYLESHEET_TEMPLATE = """
/* [60% BASE] - Main Application Window Background */
QMainWindow, QWidget#centralWidget {{
    background-color: #f3f3f3;
    color: #201f1e;
    font-size: 11px;
}}

QLabel {{
    color: #201f1e;
}}

QMessageBox, QDialog {{
    background-color: #f3f3f3;
    color: #201f1e;
}}

QMessageBox QLabel {{
    color: #201f1e;
}}

/* [30% SECONDARY] - Side Panels, Docks, and Toolbars */
QDockWidget, QMenuBar, QStatusBar, QTabWidget::pane {{
    background-color: #ffffff;
    color: #201f1e;
    border: 1px solid #d2d0ce;
    font-size: 11px;
}}

/* [REFINED] Dock Widget Title and Buttons */
QDockWidget::title {{
    background-color: #edebe9;
    padding: 8px;
    font-weight: bold;
    border-bottom: 1px solid #d2d0ce;
}}

QDockWidget::close-button, QDockWidget::float-button {{
    background: #e1e1e1;
    border-radius: 3px;
    padding: 2px;
}}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
    background: #0078d4;
}}

/* [REFINED] Modern Streamlined Tabs */
QTabBar::tab {{
    background-color: transparent;
    color: #605e5c;
    padding: 6px 20px;
    border-bottom: 2px solid transparent;
    margin-right: 2px;
    font-weight: 500;
}}

QTabBar::tab:hover {{
    background-color: #f3f2f1;
    color: #201f1e;
}}

QTabBar::tab:selected {{
    background-color: #ffffff;
    color: #0078d4;
    border-bottom: 2px solid #0078d4;
    font-weight: 700;
}}

/* [30% SECONDARY] - Form Inputs and Widgets */
QLineEdit, QTextEdit, QComboBox {{
    background-color: #ffffff;
    border: 1px solid #8a8886;
    border-radius: 4px;
    padding: 4px;
    color: #201f1e;
    font-size: 11px;
}}

/* [DYNAMIC] - Table View Data Scaling (Clean Grid) */
QTableView, QTableView::item {{
    background-color: #ffffff;
    alternate-background-color: #f9f9f9;
    border: 1px solid #e1e1e1;
    padding: 2px;
    color: #201f1e;
    font-size: {font_size}px;
}}

/* [REFINED] Compact Cell Editor */
QTableView QLineEdit {{
    background-color: #ffffff;
    border: 1px solid #0078d4;
    border-radius: 0px;
    padding: 0px 4px;
    margin: 0px;
}}

/* [10% ACCENT] - Interactive Elements & Branding Blue */
QPushButton {{
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 10px;
}}

QPushButton#zoomButton {{
    min-width: 24px;
    max-width: 24px;
    padding: 2px;
}}

QPushButton:hover {{
    background-color: #106ebe;
}}

QPushButton:pressed {{
    background-color: #005a9e;
}}

/* [10% ACCENT] - Selection and Focus Indicators */
QTableView::item:selected {{
    background-color: #c7e0f4;
    color: #00101b;
}}

QHeaderView::section {{
    background-color: #edebe9;
    color: #201f1e;
    border: 1px solid #d2d0ce;
    padding: 6px;
    font-weight: bold;
    font-size: {font_size}px;
}}

QScrollBar::handle {{
    background-color: #c8c6c4;
    border-radius: 4px;
}}
"""

def get_dark_stylesheet(font_size=10):
    """Returns the corporate dark theme stylesheet with specified font size"""
    return DARK_STYLESHEET_TEMPLATE.format(font_size=font_size)

def get_light_stylesheet(font_size=10):
    """Returns the corporate light theme stylesheet with specified font size"""
    return LIGHT_STYLESHEET_TEMPLATE.format(font_size=font_size)
