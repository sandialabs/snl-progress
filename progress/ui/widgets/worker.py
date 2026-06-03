import sys
from PySide6.QtCore import Signal, QThread


class WorkerThread(QThread):
    finished = Signal()
    output_updated = Signal(str)

    def __init__(self, method, *args):
        super().__init__()
        self.method = method
        self.args = args

    def run(self):
        stdout_buffer = StdoutBuffer(self)
        sys.stdout = stdout_buffer

        self.method(*self.args)

        sys.stdout = sys.__stdout__

        self.finished.emit()


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
