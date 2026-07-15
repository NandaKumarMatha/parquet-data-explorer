from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from utils.app_info import APP_NAME, APP_VERSION, about_text
from utils.path_helper import get_resource_path


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About")
        self.setModal(True)
        self.setMinimumWidth(420)
        self.setMaximumWidth(520)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        header = QHBoxLayout()
        icon_label = QLabel()
        icon = QIcon(get_resource_path("fav.ico"))
        if not icon.isNull():
            icon_label.setPixmap(icon.pixmap(64, 64))
        header.addWidget(icon_label)

        title = QLabel(f"<b>{APP_NAME}</b><br>Version {APP_VERSION}")
        title.setTextFormat(Qt.TextFormat.RichText)
        title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        header.addWidget(title, 1)
        layout.addLayout(header)

        body = QLabel(about_text())
        body.setTextFormat(Qt.TextFormat.RichText)
        body.setOpenExternalLinks(True)
        body.setWordWrap(True)
        body.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(body)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
