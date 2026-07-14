"""Startup splash shown while the main window is loading."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QSplashScreen

from utils.app_info import APP_NAME, APP_VERSION


def create_splash_screen() -> QSplashScreen:
    pixmap = QPixmap(420, 220)
    pixmap.fill(QColor("#1e1e1e"))

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    painter.setPen(QColor("#e0e0e0"))
    title_font = QFont()
    title_font.setPointSize(18)
    title_font.setBold(True)
    painter.setFont(title_font)
    painter.drawText(pixmap.rect().adjusted(0, 40, 0, 0), Qt.AlignmentFlag.AlignHCenter, APP_NAME)

    painter.setPen(QColor("#9e9e9e"))
    sub_font = QFont()
    sub_font.setPointSize(10)
    painter.setFont(sub_font)
    painter.drawText(
        pixmap.rect().adjusted(0, 80, 0, 0),
        Qt.AlignmentFlag.AlignHCenter,
        f"Version {APP_VERSION}",
    )

    painter.setPen(QColor("#4fc3f7"))
    painter.drawText(
        pixmap.rect().adjusted(0, 130, 0, 0),
        Qt.AlignmentFlag.AlignHCenter,
        "Starting… please wait",
    )
    painter.end()

    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    return splash


def update_splash(splash: QSplashScreen | None, message: str, app) -> None:
    if splash is None:
        return
    splash.showMessage(
        message,
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        QColor("#b0b0b0"),
    )
    app.processEvents()
