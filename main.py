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
from utils.terminal_banner import print_launch_banner
from utils.single_instance import InstanceListener, try_notify_existing_instance
from ui.splash import create_splash_screen, update_splash


def main():
    print_launch_banner()
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path("fav.ico")))
    app.setApplicationName("Parquet Explorer")
    app.setOrganizationName("ParquetExplorer")

    # A second desktop click should focus the running app, not start another slow load.
    if try_notify_existing_instance():
        print("Parquet Explorer is already running — bringing it to the front.")
        return 0

    splash = create_splash_screen()
    splash.show()
    update_splash(splash, "Loading application…", app)

    listener = InstanceListener(app)
    if not listener.start():
        # Another instance won the race; exit quietly.
        splash.close()
        return 0

    update_splash(splash, "Loading main window…", app)
    from ui.main_window import MainWindow

    file_path = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    update_splash(splash, "Preparing interface…", app)
    window = MainWindow(file_path)

    def raise_existing_window():
        window.show()
        window.raise_()
        window.activateWindow()

    listener.activate_requested.connect(raise_existing_window)

    window.show()
    splash.finish(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
