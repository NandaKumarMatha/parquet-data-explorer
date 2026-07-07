from PyQt6.QtCore import QThread, pyqtSignal

from data.parquet_handler import load_parquet, load_parquet_full, LoadCancelled


class PageLoadWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, file_path, offset, limit):
        super().__init__()
        self.file_path = file_path
        self.offset = offset
        self.limit = limit

    def run(self):
        try:
            df = load_parquet(self.file_path, offset=self.offset, limit=self.limit)
            self.finished.emit(df)
        except MemoryError:
            self.error.emit("Not enough memory to load this page. Try a smaller page size.")
        except Exception as e:
            self.error.emit(str(e))


class FullDataLoadWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int)

    def __init__(self, file_path, edited_cells=None):
        super().__init__()
        self.file_path = file_path
        self.edited_cells = edited_cells or {}
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            df = load_parquet_full(
                self.file_path,
                edited_cells=self.edited_cells,
                cancel_check=lambda: self._cancelled,
                on_progress=lambda done, total: self.progress.emit(done, total),
            )
            if self._cancelled:
                return
            self.finished.emit(df)
        except LoadCancelled:
            self.error.emit("Load cancelled")
        except MemoryError:
            self.error.emit(
                "Not enough memory to load the full file. "
                "Try filtering, exporting one page, or using a machine with more RAM."
            )
        except Exception as e:
            self.error.emit(str(e))
