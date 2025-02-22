import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser
import markdown


class MarkdownWidget(QWidget):
    def __init__(self, markdown_file):
        super().__init__()

        # Create a layout for the widget
        layout = QVBoxLayout(self)

        # Create a QTextBrowser widget
        self.text_browser = QTextBrowser(self)
        layout.addWidget(self.text_browser)

        # Load and display the Markdown file
        self.load_markdown(markdown_file)

    def load_markdown(self, markdown_file):
        # Read the Markdown file
        with open(markdown_file, 'r', encoding='utf-8') as file:
            markdown_text = file.read()

        # Convert Markdown to HTML
        html = markdown.markdown(markdown_text)

        # Set the HTML content to the QTextBrowser
        self.text_browser.setHtml(html)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Specify the path to your Markdown file
    markdown_file_path = 'example.md'  # Change this to your Markdown file path

    # Create the main window
    main_window = QWidget()
    main_window.setWindowTitle("Markdown Viewer")
    main_layout = QVBoxLayout(main_window)

    # Create an instance of MarkdownWidget and add it to the layout
    markdown_widget = MarkdownWidget(markdown_file_path)
    main_layout.addWidget(markdown_widget)

    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
