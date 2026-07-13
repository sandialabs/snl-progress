"""Styled QMessageBox wrappers.

Every message box is created as an instance with an inline stylesheet so
it renders correctly on all platforms (especially Windows, where native
dialogs ignore the application QSS and QPalette).
"""

from PySide6.QtWidgets import QMessageBox

_MSGBOX_LIGHT = """
QMessageBox {
    background-color: #ffffff;
}
QMessageBox QLabel {
    color: #0f172a;
    font-size: 13px;
    min-width: 300px;
}
QMessageBox QPushButton {
    background-color: #387a3d;
    color: #ffffff;
    border: 1px solid #387a3d;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
    min-width: 80px;
    min-height: 20px;
}
QMessageBox QPushButton:hover {
    background-color: #2d6a30;
    border-color: #2d6a30;
}
QMessageBox QPushButton:pressed {
    background-color: #235827;
    border-color: #235827;
}
"""

_MSGBOX_DARK = """
QMessageBox {
    background-color: #1e293b;
}
QMessageBox QLabel {
    color: #f1f5f9;
    font-size: 13px;
    min-width: 300px;
}
QMessageBox QPushButton {
    background-color: #4ade80;
    color: #0f172a;
    border: 1px solid #4ade80;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
    min-width: 80px;
    min-height: 20px;
}
QMessageBox QPushButton:hover {
    background-color: #22c55e;
    border-color: #22c55e;
    color: #0f172a;
}
QMessageBox QPushButton:pressed {
    background-color: #16a34a;
    border-color: #16a34a;
    color: #0f172a;
}
"""


def _current_style() -> str:
    from PySide6.QtWidgets import QApplication
    from progress.dpi import is_windows
    if not is_windows():
        return ""
    from PySide6.QtCore import QSettings
    theme = QSettings("QuESt", "snl-progress").value("theme", "light")
    return _MSGBOX_DARK if theme == "dark" else _MSGBOX_LIGHT


def _make(parent, icon, title, text, buttons=QMessageBox.Ok):
    msg = QMessageBox(parent)
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(buttons)
    style = _current_style()
    if style:
        msg.setStyleSheet(style)
    return msg


def information(parent, title, text):
    return _make(parent, QMessageBox.Information, title, text).exec_()


def critical(parent, title, text):
    return _make(parent, QMessageBox.Critical, title, text).exec_()


def warning(parent, title, text):
    return _make(parent, QMessageBox.Warning, title, text).exec_()


def question(parent, title, text, buttons=QMessageBox.Yes | QMessageBox.No):
    return _make(parent, QMessageBox.Question, title, text, buttons).exec_()
