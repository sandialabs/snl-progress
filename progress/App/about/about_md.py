import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser
import markdown

class MarkdownWidget(QWidget):
    def __init__(self, markdown_file):
        super().__init__()

        layout = QVBoxLayout(self)

        self.text_browser = QTextBrowser(self)
        layout.addWidget(self.text_browser)

        self.load_markdown(markdown_file)

    def load_markdown(self, markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as file:
            markdown_text = file.read()

        html = markdown.markdown(markdown_text, extensions=['tables'])
        self.text_browser.setHtml(html)
        self.text_browser.setOpenExternalLinks(True)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    markdown_file_path = 'example.md'  

    main_window = QWidget()
    main_window.setWindowTitle("Markdown Viewer")
    main_layout = QVBoxLayout(main_window)

    markdown_widget = MarkdownWidget(markdown_file_path)
    main_layout.addWidget(markdown_widget)

    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
