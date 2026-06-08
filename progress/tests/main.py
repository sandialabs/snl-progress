import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QFile, QTextStream

import progress.resources_rc


def test_stylesheet_loads():
    f = QFile(":/styles/resources/theme.qss")
    assert f.open(QFile.ReadOnly | QFile.Text), "Could not open :/styles/resources/theme.qss"
    css = QTextStream(f).readAll()
    f.close()
    assert len(css) > 0, "theme.qss is empty"


def test_main_window_loads():
    from progress.ui.forms.main_window.ui_main_window import Ui_MainWindow
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    assert window is not None


def test_landing_page_loads():
    from progress.ui.forms.landing.ui_landing import Ui_LandingPage
    widget = QWidget()
    ui = Ui_LandingPage()
    ui.setupUi(widget)
    assert widget is not None


app = QApplication(sys.argv)

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

from progress.ui.forms.landing.ui_landing import Ui_LandingPage
from progress.ui.forms.main_window.ui_main_window import Ui_MainWindow

f = QFile(":/styles/resources/theme.qss")
f.open(QFile.ReadOnly | QFile.Text)
css = QTextStream(f).readAll()
f.close()

widget = QWidget()
widget.setWindowTitle("QuESt ProGRESS - Landing Page")
# widget.resize(1122, 928)
# ui = Ui_LandingPage()
# ui.setupUi(widget)
# widget.show()

window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
app.setStyleSheet(css)
window.show()
print(f"\n{sum(results)}/{len(results)} passed")

sys.exit(app.exec())
