import sys
import threading
import logging
from PySide6.QtCore import Signal, QThread
from progress.example_simulation import StopSimulation

logger = logging.getLogger(__name__)

class WorkerThread(QThread):
    error = Signal(str)
    success = Signal()

    def __init__(self, method, *args, parent=None):
        super().__init__(parent)
        self.method = method
        self.args = args

    def run(self):
        try:
            self.method(*self.args)
            self.success.emit()
        except Exception as e:
            logger.exception("Worker thread failed")
            self.error.emit(str(e))


class ProcessingThread:
    """Thread for heavy CPU work — no Qt involvement (avoids M-chip segfaults)."""
    def __init__(self, method, *args):
        self.stop_event = threading.Event()
        self._thread = threading.Thread(
            target=self._run, args=(method, *args), daemon=True
        )

    def _run(self, method, *args):
        try:
            method(*args, stop_event=self.stop_event)
        except StopSimulation:
            pass

    def stop(self):
        self.stop_event.set()

    def start(self):
        self._thread.start()

    def isFinished(self):
        return not self._thread.is_alive()

class StdoutBuffer:
    def __init__(self, worker_thread):
        self.worker_thread = worker_thread
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        lines = self.buffer.split("\n")
        for line in lines[:-1]:
            self.worker_thread.output_updated.emit(line)
        self.buffer = lines[-1]

    def flush(self):
        pass
