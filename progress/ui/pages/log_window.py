import sys
import logging
from typing import Optional

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget, QPlainTextEdit

from progress.ui.forms.log_window.ui_log_window import Ui_LogPage

""" LOGGING LAYERS:
logger.debug("Detailed developer/debug message")
logger.info("Normal application event")
logger.warning("Something unusual happened")
logger.error("Something failed")
logger.exception("Something failed with traceback")
"""


class _LogEmitter(QObject):
    """
    Sends log text safely to the Qt widget.
    """
    text_written = Signal(str)


class _QtLogHandler(QObject, logging.Handler):
    """
    Logging handler that writes Python logging messages to the app log window.
    """

    def __init__(self, log_widget: QPlainTextEdit):
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.log_widget = log_widget

        # Signal used to update the GUI safely.
        self.emitter = _LogEmitter()
        self.emitter.text_written.connect(self._append_text)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record)
            self._append_text(message + "\n")
        except Exception:
            self.handleError(record)

    def _append_text(self, text: str) -> None:
        cursor = self.log_widget.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_widget.setTextCursor(cursor)
        self.log_widget.insertPlainText(text)
        self.log_widget.ensureCursorVisible()


class _QtPrintStream(QObject):
    """
    Redirects print output into the app log window.
    """
    text_written = Signal(str)

    def write(self, text: str) -> None:
        if text:
            self.text_written.emit(str(text))

    def flush(self) -> None:
        pass


class LogWindowController(QObject):
    """
    Connects logging, print output, and errors to the log window widget.
    """

    def __init__(
        self,
        log_widget: QPlainTextEdit,
        level: int = logging.INFO,
        capture_print: bool = True,
        remove_existing_handlers: bool = True,
        defer_capture: bool = False,
    ):
        super().__init__()

        self.log_widget = log_widget
        self.log_widget.setReadOnly(True)

        # Keep original streams so they can be restored if needed.
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        # Handler for normal Python logging.
        self.log_handler = _QtLogHandler(self.log_widget)
        self.log_handler.setLevel(level)
        self.log_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                datefmt="%H:%M:%S",
            )
        )

        # Configure root logger so logs from all modules go here.
        root_logger = logging.getLogger()

        if not defer_capture and remove_existing_handlers:
            for handler in list(root_logger.handlers):
                root_logger.removeHandler(handler)

        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(level)

        self.print_stream = None
        self.error_stream = None
        self._capture_enabled = False

        if capture_print:
            self.print_stream = _QtPrintStream()
            self.error_stream = _QtPrintStream()

            self.print_stream.text_written.connect(self._append_plain_text)
            self.error_stream.text_written.connect(self._append_plain_text)

            if not defer_capture:
                sys.stdout = self.print_stream
                sys.stderr = self.error_stream
                self._capture_enabled = True

    def enable_capture(self) -> None:
        """Redirect stdout/stderr to the log window and optionally clean up terminal handlers."""
        if self._capture_enabled:
            return

        if self.print_stream and self.error_stream:
            sys.stdout = self.print_stream
            sys.stderr = self.error_stream

        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            if handler is not self.log_handler:
                root_logger.removeHandler(handler)

        self._capture_enabled = True

    @Slot(str)
    def _append_plain_text(self, text: str) -> None:
        """
        Adds plain print/error text to the log window.
        """
        cursor = self.log_widget.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_widget.setTextCursor(cursor)

        self.log_widget.insertPlainText(text)
        self.log_widget.ensureCursorVisible()

    def clear(self) -> None:
        """
        Clears the log window.
        """
        self.log_widget.clear()

    def restore(self) -> None:
        """
        Restores original terminal output.
        """
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

        root_logger = logging.getLogger()
        root_logger.removeHandler(self.log_handler)


_log_controller: Optional[LogWindowController] = None


def install_log_window(
    log_widget: QPlainTextEdit,
    level: int = logging.INFO,
    capture_print: bool = True,
    remove_existing_handlers: bool = True,
    defer_capture: bool = False,
) -> LogWindowController:
    """
    Installs the logger once and returns the controller.
    """
    global _log_controller

    if _log_controller is None:
        _log_controller = LogWindowController(
            log_widget=log_widget,
            level=level,
            capture_print=capture_print,
            remove_existing_handlers=remove_existing_handlers,
            defer_capture=defer_capture,
        )

    return _log_controller


def get_log_window() -> Optional[LogWindowController]:
    """
    Returns the active log controller.
    """
    return _log_controller


class LogWindow(QWidget):
    """
    Separate log window.
    """

    def __init__(self):
        super().__init__()

        # Load the generated UI.
        self.ui = Ui_LogPage()
        self.ui.setupUi(self)

        self.setWindowTitle("Progress Logs")

        # Install logging onto the QPlainTextEdit named log_window.
        # Defer capture so startup output goes to the terminal; enable_capture()
        # is called later in AppController.show_all() just before windows appear.
        self.log_controller = install_log_window(self.ui.log_window, defer_capture=True)

    def clear_logs(self) -> None:
        self.log_controller.clear()
