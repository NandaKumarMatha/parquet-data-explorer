import os
os.environ['QT_API'] = 'pyqt6'

# Snap/WebEngine: use software GL before Qt platform plugins initialize.
if os.environ.get('SNAP'):
    os.environ.setdefault('QT_OPENGL', 'software')
    os.environ.setdefault('QT_XCB_GL_INTEGRATION', 'none')

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
from utils.path_helper import get_resource_path

def main():
    if os.environ.get('SNAP'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path("fav.ico")))
    
    file_path = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
    window = MainWindow(file_path)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()