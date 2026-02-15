import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
from utils.path_helper import get_resource_path

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path("fav.ico")))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()