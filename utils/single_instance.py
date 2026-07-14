"""Single-instance guard so desktop double-clicks don't spawn many slow startups."""

from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

SERVER_NAME = "parquet-explorer-single-instance"


class InstanceListener(QObject):
    activate_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._server = QLocalServer(self)
        self._server.newConnection.connect(self._on_new_connection)

    def start(self) -> bool:
        QLocalServer.removeServer(SERVER_NAME)
        return self._server.listen(SERVER_NAME)

    def _on_new_connection(self):
        while self._server.hasPendingConnections():
            socket = self._server.nextPendingConnection()
            socket.readyRead.connect(lambda s=socket: self._read_socket(s))
            if socket.bytesAvailable():
                self._read_socket(socket)

    def _read_socket(self, socket: QLocalSocket):
        _ = bytes(socket.readAll())
        socket.disconnectFromServer()
        self.activate_requested.emit()


def try_notify_existing_instance() -> bool:
    """Return True if another instance is already running and was notified."""
    socket = QLocalSocket()
    socket.connectToServer(SERVER_NAME)
    if not socket.waitForConnected(250):
        return False
    socket.write(b"raise")
    socket.flush()
    socket.waitForBytesWritten(250)
    socket.disconnectFromServer()
    return True
