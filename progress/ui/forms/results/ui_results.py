# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'results.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QTableWidget, QTableWidgetItem, QTreeView, QVBoxLayout,
    QWidget)

class Ui_FilePreviewPage(object):
    def setupUi(self, FilePreviewPage):
        if not FilePreviewPage.objectName():
            FilePreviewPage.setObjectName(u"FilePreviewPage")
        FilePreviewPage.resize(1163, 908)
        self.verticalLayout_main = QVBoxLayout(FilePreviewPage)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.main_frame = QFrame(FilePreviewPage)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFrameShape(QFrame.NoFrame)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_main = QHBoxLayout(self.main_frame)
        self.horizontalLayout_main.setObjectName(u"horizontalLayout_main")
        self.frame_file_browser = QFrame(self.main_frame)
        self.frame_file_browser.setObjectName(u"frame_file_browser")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_file_browser.sizePolicy().hasHeightForWidth())
        self.frame_file_browser.setSizePolicy(sizePolicy)
        self.frame_file_browser.setMinimumSize(QSize(300, 0))
        self.frame_file_browser.setMaximumSize(QSize(380, 16777215))
        self.frame_file_browser.setFrameShape(QFrame.StyledPanel)
        self.frame_file_browser.setFrameShadow(QFrame.Raised)
        self.verticalLayout_file_browser = QVBoxLayout(self.frame_file_browser)
        self.verticalLayout_file_browser.setObjectName(u"verticalLayout_file_browser")
        self.label_browser_title = QLabel(self.frame_file_browser)
        self.label_browser_title.setObjectName(u"label_browser_title")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_browser_title.setFont(font)

        self.verticalLayout_file_browser.addWidget(self.label_browser_title)

        self.line_separator_browser = QFrame(self.frame_file_browser)
        self.line_separator_browser.setObjectName(u"line_separator_browser")
        self.line_separator_browser.setFrameShape(QFrame.HLine)
        self.line_separator_browser.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_file_browser.addWidget(self.line_separator_browser)

        self.frame_file_path_search = QFrame(self.frame_file_browser)
        self.frame_file_path_search.setObjectName(u"frame_file_path_search")
        self.frame_file_path_search.setFrameShape(QFrame.NoFrame)
        self.frame_file_path_search.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_file_path_search)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_path = QLineEdit(self.frame_file_path_search)
        self.lineEdit_path.setObjectName(u"lineEdit_path")

        self.horizontalLayout.addWidget(self.lineEdit_path)

        self.btn_clear_search = QPushButton(self.frame_file_path_search)
        self.btn_clear_search.setObjectName(u"btn_clear_search")

        self.horizontalLayout.addWidget(self.btn_clear_search)


        self.verticalLayout_file_browser.addWidget(self.frame_file_path_search)

        self.frame_dir_options = QFrame(self.frame_file_browser)
        self.frame_dir_options.setObjectName(u"frame_dir_options")
        self.frame_dir_options.setFrameShape(QFrame.NoFrame)
        self.frame_dir_options.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_dir_options)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_home_dir = QPushButton(self.frame_dir_options)
        self.btn_home_dir.setObjectName(u"btn_home_dir")

        self.horizontalLayout_2.addWidget(self.btn_home_dir)

        self.btn_results_dir = QPushButton(self.frame_dir_options)
        self.btn_results_dir.setObjectName(u"btn_results_dir")

        self.horizontalLayout_2.addWidget(self.btn_results_dir)


        self.verticalLayout_file_browser.addWidget(self.frame_dir_options)

        self.treeView_files = QTreeView(self.frame_file_browser)
        self.treeView_files.setObjectName(u"treeView_files")

        self.verticalLayout_file_browser.addWidget(self.treeView_files)


        self.horizontalLayout_main.addWidget(self.frame_file_browser)

        self.groupBox_preview = QGroupBox(self.main_frame)
        self.groupBox_preview.setObjectName(u"groupBox_preview")
        font1 = QFont()
        font1.setPointSize(14)
        self.groupBox_preview.setFont(font1)
        self.verticalLayout_preview = QVBoxLayout(self.groupBox_preview)
        self.verticalLayout_preview.setObjectName(u"verticalLayout_preview")
        self.stackedWidget_preview = QStackedWidget(self.groupBox_preview)
        self.stackedWidget_preview.setObjectName(u"stackedWidget_preview")
        self.page_empty = QWidget()
        self.page_empty.setObjectName(u"page_empty")
        self.verticalLayout_empty = QVBoxLayout(self.page_empty)
        self.verticalLayout_empty.setObjectName(u"verticalLayout_empty")
        self.verticalSpacer_empty_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_empty.addItem(self.verticalSpacer_empty_top)

        self.label_empty = QLabel(self.page_empty)
        self.label_empty.setObjectName(u"label_empty")
        font2 = QFont()
        font2.setPointSize(16)
        self.label_empty.setFont(font2)
        self.label_empty.setAlignment(Qt.AlignCenter)

        self.verticalLayout_empty.addWidget(self.label_empty)

        self.verticalSpacer_empty_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_empty.addItem(self.verticalSpacer_empty_bottom)

        self.stackedWidget_preview.addWidget(self.page_empty)
        self.page_pdf = QWidget()
        self.page_pdf.setObjectName(u"page_pdf")
        self.verticalLayout_pdf = QVBoxLayout(self.page_pdf)
        self.verticalLayout_pdf.setObjectName(u"verticalLayout_pdf")
        self.label_pdf_title = QLabel(self.page_pdf)
        self.label_pdf_title.setObjectName(u"label_pdf_title")
        self.label_pdf_title.setMaximumSize(QSize(16777215, 30))
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.label_pdf_title.setFont(font3)

        self.verticalLayout_pdf.addWidget(self.label_pdf_title)

        self.stackedWidget_preview.addWidget(self.page_pdf)
        self.page_image = QWidget()
        self.page_image.setObjectName(u"page_image")
        self.verticalLayout_image = QVBoxLayout(self.page_image)
        self.verticalLayout_image.setObjectName(u"verticalLayout_image")
        self.label_image_title = QLabel(self.page_image)
        self.label_image_title.setObjectName(u"label_image_title")
        self.label_image_title.setFont(font3)

        self.verticalLayout_image.addWidget(self.label_image_title)

        self.scrollArea_image = QScrollArea(self.page_image)
        self.scrollArea_image.setObjectName(u"scrollArea_image")
        self.scrollArea_image.setWidgetResizable(True)
        self.scrollAreaWidgetContents_image = QWidget()
        self.scrollAreaWidgetContents_image.setObjectName(u"scrollAreaWidgetContents_image")
        self.scrollAreaWidgetContents_image.setGeometry(QRect(0, 0, 663, 771))
        self.verticalLayout_scroll_image = QVBoxLayout(self.scrollAreaWidgetContents_image)
        self.verticalLayout_scroll_image.setObjectName(u"verticalLayout_scroll_image")
        self.label_image_preview = QLabel(self.scrollAreaWidgetContents_image)
        self.label_image_preview.setObjectName(u"label_image_preview")
        self.label_image_preview.setMinimumSize(QSize(400, 300))
        self.label_image_preview.setFrameShape(QFrame.StyledPanel)
        self.label_image_preview.setAlignment(Qt.AlignCenter)

        self.verticalLayout_scroll_image.addWidget(self.label_image_preview)

        self.scrollArea_image.setWidget(self.scrollAreaWidgetContents_image)

        self.verticalLayout_image.addWidget(self.scrollArea_image)

        self.stackedWidget_preview.addWidget(self.page_image)
        self.page_csv = QWidget()
        self.page_csv.setObjectName(u"page_csv")
        self.verticalLayout_csv = QVBoxLayout(self.page_csv)
        self.verticalLayout_csv.setObjectName(u"verticalLayout_csv")
        self.label_csv_title = QLabel(self.page_csv)
        self.label_csv_title.setObjectName(u"label_csv_title")
        self.label_csv_title.setFont(font3)

        self.verticalLayout_csv.addWidget(self.label_csv_title)

        self.tableWidget_csv = QTableWidget(self.page_csv)
        if (self.tableWidget_csv.columnCount() < 4):
            self.tableWidget_csv.setColumnCount(4)
        if (self.tableWidget_csv.rowCount() < 5):
            self.tableWidget_csv.setRowCount(5)
        self.tableWidget_csv.setObjectName(u"tableWidget_csv")
        self.tableWidget_csv.setShowGrid(True)
        self.tableWidget_csv.setRowCount(5)
        self.tableWidget_csv.setColumnCount(4)

        self.verticalLayout_csv.addWidget(self.tableWidget_csv)

        self.stackedWidget_preview.addWidget(self.page_csv)
        self.page_xlsx = QWidget()
        self.page_xlsx.setObjectName(u"page_xlsx")
        self.verticalLayout = QVBoxLayout(self.page_xlsx)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_xlsx_title = QLabel(self.page_xlsx)
        self.label_xlsx_title.setObjectName(u"label_xlsx_title")
        font4 = QFont()
        font4.setBold(True)
        self.label_xlsx_title.setFont(font4)

        self.verticalLayout.addWidget(self.label_xlsx_title)

        self.tableWidget_xslx = QTableWidget(self.page_xlsx)
        self.tableWidget_xslx.setObjectName(u"tableWidget_xslx")

        self.verticalLayout.addWidget(self.tableWidget_xslx)

        self.stackedWidget_preview.addWidget(self.page_xlsx)
        self.page_html = QWidget()
        self.page_html.setObjectName(u"page_html")
        self.verticalLayout_2 = QVBoxLayout(self.page_html)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_html_title = QLabel(self.page_html)
        self.label_html_title.setObjectName(u"label_html_title")

        self.verticalLayout_2.addWidget(self.label_html_title)

        self.stackedWidget_preview.addWidget(self.page_html)

        self.verticalLayout_preview.addWidget(self.stackedWidget_preview)


        self.horizontalLayout_main.addWidget(self.groupBox_preview)


        self.verticalLayout_main.addWidget(self.main_frame)


        self.retranslateUi(FilePreviewPage)

        self.stackedWidget_preview.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(FilePreviewPage)
    # setupUi

    def retranslateUi(self, FilePreviewPage):
        FilePreviewPage.setWindowTitle(QCoreApplication.translate("FilePreviewPage", u"File Preview", None))
        self.label_browser_title.setText(QCoreApplication.translate("FilePreviewPage", u"File Browser", None))
        self.lineEdit_path.setPlaceholderText(QCoreApplication.translate("FilePreviewPage", u"Optional path or filter...", None))
        self.btn_clear_search.setText(QCoreApplication.translate("FilePreviewPage", u"Clear", None))
        self.btn_home_dir.setText(QCoreApplication.translate("FilePreviewPage", u"Set to Home Directory", None))
        self.btn_results_dir.setText(QCoreApplication.translate("FilePreviewPage", u"Set to Results Directory", None))
        self.groupBox_preview.setTitle(QCoreApplication.translate("FilePreviewPage", u"Preview", None))
        self.label_empty.setText(QCoreApplication.translate("FilePreviewPage", u"No file selected for preview.", None))
        self.label_pdf_title.setText(QCoreApplication.translate("FilePreviewPage", u"PDF Preview", None))
        self.label_image_title.setText(QCoreApplication.translate("FilePreviewPage", u"PNG Preview", None))
        self.label_image_preview.setText(QCoreApplication.translate("FilePreviewPage", u"Image preview goes here", None))
        self.label_csv_title.setText(QCoreApplication.translate("FilePreviewPage", u"CSV Preview", None))
        self.label_xlsx_title.setText(QCoreApplication.translate("FilePreviewPage", u"XLSX Preview", None))
        self.label_html_title.setText(QCoreApplication.translate("FilePreviewPage", u"HTML Preview", None))
    # retranslateUi

