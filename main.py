import os

from utils.webengine_env import configure_webengine_env

configure_webengine_env()
os.environ["QT_API"] = "pyqt6"

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
# WebEngine must be imported before QApplication is constructed.
from PyQt6.QtWebEngineWidgets import QWebEngineView  # noqa: F401
from utils.path_helper import get_resource_path


def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

    from ui.main_window import MainWindow

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
