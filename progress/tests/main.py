# test_ui.py
import sys
import pytest
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QTextStream

import progress.resources_rc  # registers the .qrc bundle

app = QApplication(sys.argv)



def test_stylesheet_loads():
    f = QFile(":/styles/resources/theme.qss")
    assert f.open(QFile.ReadOnly | QFile.Text), "Could not open :/styles/resources/theme.qss"
    css = QTextStream(f).readAll()
    f.close()
    assert len(css) > 0, "theme.qss is empty"


def test_main_window_loads():
    from progress.ui.forms.main_window.ui_main_window import Ui_MainWindow
    from PySide6.QtWidgets import QMainWindow
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    assert window is not None


def test_landing_page_loads():
    from progress.ui.forms.landing.ui_landing import Ui_LandingPage
    from PySide6.QtWidgets import QWidget
    widget = QWidget()
    ui = Ui_LandingPage()
    ui.setupUi(widget)
    assert widget is not None


def test_stylesheet_applied():
    from progress.ui.forms.main_window.ui_main_window import Ui_MainWindow
    from PySide6.QtWidgets import QMainWindow
    f = QFile(":/styles/resources/theme.qss")
    f.open(QFile.ReadOnly | QFile.Text)
    css = QTextStream(f).readAll()
    f.close()

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    app.setStyleSheet(css)
    assert app.styleSheet() == css

results = []
for name, fn in [
    ("stylesheet loads", test_stylesheet_loads),
    ("main window loads", test_main_window_loads),
    ("landing page loads", test_landing_page_loads),
]:
    try:
        fn()
        print(f"  PASS  {name}")
        results.append(True)
    except Exception as e:
        print(f"  FAIL  {name}: {e}")
        results.append(False)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
