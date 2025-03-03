# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)
import progress.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1286, 847)
        palette = QPalette()
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet(u"QLineEdit {\n"
"    background: white; /* Set a solid background color */\n"
"    border: 1px solid rgb(59, 103, 59); /* Set a border color */\n"
"    border-radius: 4px; /* Optional: rounded corners */\n"
"    color: rgb(0, 0, 0); /* Text color */\n"
"    padding: 5px; /* Optional: padding inside the line edit */\n"
"}")
        self.actionInfo = QAction(MainWindow)
        self.actionInfo.setObjectName(u"actionInfo")
        self.actionOptions = QAction(MainWindow)
        self.actionOptions.setObjectName(u"actionOptions")
        self.actionMore_Info = QAction(MainWindow)
        self.actionMore_Info.setObjectName(u"actionMore_Info")
        self.actionContact = QAction(MainWindow)
        self.actionContact.setObjectName(u"actionContact")
        self.actionFAQ = QAction(MainWindow)
        self.actionFAQ.setObjectName(u"actionFAQ")
        self.actionAnything = QAction(MainWindow)
        self.actionAnything.setObjectName(u"actionAnything")
        self.actionHome_Page = QAction(MainWindow)
        self.actionHome_Page.setObjectName(u"actionHome_Page")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    color: rgb(59, 103, 59);\n"
"    background: transparent;\n"
"    border: 1px solid transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    color: rgb(59, 103, 59);\n"
"    background: rgba(69, 160, 73, 0.1);\n"
"}\n"
"")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        palette1 = QPalette()
        self.stackedWidget.setPalette(palette1)
        self.stackedWidget.setStyleSheet(u"")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setStyleSheet(u"")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"")
        self.gridLayout_3 = QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget = QTabWidget(self.page_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget::pane {\n"
"    border: 0px;\n"
"}\n"
"QTabBar::tab {\n"
"    background: transparent;\n"
"    padding: 5px 15px; /* Reduced padding for thinner tabs */\n"
"    border: 1px solid transparent;\n"
"    color: rgb(59, 103, 59);\n"
"    border-bottom: 2px solid transparent;\n"
"}\n"
"QTabBar::tab:selected {\n"
"    color: rgb(59, 103, 59);\n"
"    border-bottom: 2px solid rgb(59, 103, 59);\n"
"}\n"
"QTabBar::tab:hover {\n"
"    background: rgba(69, 160, 73, 0.1); \n"
"    color: rgb(59, 103, 59);\n"
"}\n"
"QFrame{\n"
"	background-color:transparent;\n"
"	border: none;\n"
"}\n"
"QTextBrowser {\n"
"    border: 1px solid rgb(59, 103, 59);\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"	background-color: rgb(233, 233, 233);\n"
"}\n"
"")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setIconSize(QSize(100, 32))
        self.tabWidget.setMovable(False)
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.verticalLayout_7 = QVBoxLayout(self.tab_7)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frame_5 = QFrame(self.tab_7)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"background-color:transparent;\n"
"border: none;")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"background-color:transparent;\n"
"border: none;")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_3)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet(u"background-color:transparent;\n"
"border: none;")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_59 = QFrame(self.frame_2)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_59.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_59)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_59)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamilies([u"Helvetica Neue"])
        font.setPointSize(64)
        font.setBold(False)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"font: 64pt \"Helvetica Neue\";")
        self.label_2.setTextFormat(Qt.TextFormat.AutoText)
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(True)

        self.horizontalLayout_30.addWidget(self.label_2)


        self.verticalLayout_4.addWidget(self.frame_59)

        self.frame_58 = QFrame(self.frame_2)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_58.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_58)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.frame_58)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy1)
        self.textBrowser.setMinimumSize(QSize(0, 80))
        font1 = QFont()
        font1.setFamilies([u"Helvetica Neue"])
        font1.setPointSize(14)
        font1.setBold(False)
        font1.setItalic(False)
        self.textBrowser.setFont(font1)
        self.textBrowser.setStyleSheet(u"QTextBrowser {\n"
"	font: 14pt \"Helvetica Neue\";\n"
"        border: none;  \n"
"        background: transparent;  \n"
"        color: rgb(59, 103, 59);\n"
"}")
        self.textBrowser.setFrameShape(QFrame.Shape.NoFrame)

        self.horizontalLayout_24.addWidget(self.textBrowser)


        self.verticalLayout_4.addWidget(self.frame_58)

        self.frame_7 = QFrame(self.frame_2)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy2)
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)

        self.pushButton_getStarted = QPushButton(self.frame_7)
        self.pushButton_getStarted.setObjectName(u"pushButton_getStarted")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_getStarted.sizePolicy().hasHeightForWidth())
        self.pushButton_getStarted.setSizePolicy(sizePolicy3)
        self.pushButton_getStarted.setMinimumSize(QSize(45, 31))
        font2 = QFont()
        font2.setFamilies([u"Helvetica Neue"])
        font2.setPointSize(20)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_getStarted.setFont(font2)
        self.pushButton_getStarted.setStyleSheet(u"QPushButton {\n"
"   font: 20pt \"Helvetica Neue\";\n"
"    border-radius: 8px;\n"
"    color: rgb(59, 103, 59);\n"
"    background: transparent;\n"
"    border: 1px solid rgb(59, 103, 59);\n"
"}\n"
"QPushButton:hover {\n"
"    color: rgb(59, 103, 59);\n"
"    background: rgba(69, 160, 73, 0.1);\n"
"}\n"
"")
        self.pushButton_getStarted.setFlat(True)

        self.horizontalLayout_11.addWidget(self.pushButton_getStarted)


        self.verticalLayout_4.addWidget(self.frame_7)

        self.verticalLayout_4.setStretch(0, 10)
        self.verticalLayout_4.setStretch(1, 1)

        self.horizontalLayout_10.addWidget(self.frame_2)

        self.horizontalLayout_10.setStretch(0, 2)

        self.verticalLayout_6.addWidget(self.frame_3)


        self.verticalLayout_7.addWidget(self.frame_5)

        self.frame = QFrame(self.tab_7)
        self.frame.setObjectName(u"frame")
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setStyleSheet(u"background-color:transparent;\n"
"border: none;")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_15 = QLabel(self.frame)
        self.label_15.setObjectName(u"label_15")
        sizePolicy3.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy3)
        self.label_15.setMaximumSize(QSize(180, 85))
        self.label_15.setPixmap(QPixmap(u":/logos/Images/logos/Quest_Logo_RGB.png"))
        self.label_15.setScaledContents(True)

        self.horizontalLayout_6.addWidget(self.label_15)

        self.horizontalSpacer_7 = QSpacerItem(385, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)

        self.label_16 = QLabel(self.frame)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMaximumSize(QSize(300, 90))
        self.label_16.setPixmap(QPixmap(u":/logos/Images/logos/Sandia_National_Laboratories_logo.svg"))
        self.label_16.setScaledContents(True)

        self.horizontalLayout_6.addWidget(self.label_16)

        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(110, 110))
        self.label_7.setPixmap(QPixmap(u":/logos/Images/logos/DOE_transparent.png"))
        self.label_7.setScaledContents(True)

        self.horizontalLayout_6.addWidget(self.label_7)

        self.textBrowser_7 = QTextBrowser(self.frame)
        self.textBrowser_7.setObjectName(u"textBrowser_7")
        sizePolicy1.setHeightForWidth(self.textBrowser_7.sizePolicy().hasHeightForWidth())
        self.textBrowser_7.setSizePolicy(sizePolicy1)
        self.textBrowser_7.setMinimumSize(QSize(0, 0))
        self.textBrowser_7.setMaximumSize(QSize(16777215, 120))
        self.textBrowser_7.setStyleSheet(u"QTextBrowser {\n"
"	font: 14pt \"Helvetica Neue\";\n"
"        border: none;  \n"
"        background: transparent;  \n"
"        color: rgb(59, 103, 59);\n"
"}\n"
"\n"
"font: 13pt \"Helvetica Neue\";")

        self.horizontalLayout_6.addWidget(self.textBrowser_7)


        self.verticalLayout_7.addWidget(self.frame)

        icon = QIcon()
        icon.addFile(u":/logos/Images/logos/progress_transparent_alt.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab_7, icon, "")
        self.api_tab = QWidget()
        self.api_tab.setObjectName(u"api_tab")
        self.verticalLayout_11 = QVBoxLayout(self.api_tab)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.widget_13 = QWidget(self.api_tab)
        self.widget_13.setObjectName(u"widget_13")
        self.verticalLayout_16 = QVBoxLayout(self.widget_13)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.widget_13)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_17 = QVBoxLayout(self.widget_3)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_16 = QFrame(self.widget_3)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frame_15 = QFrame(self.frame_16)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_15)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.frame_15)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"background-color:transparent;\n"
"border: none;")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_10)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"background-color:transparent;\n"
"border: none;")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_8)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_17 = QFrame(self.frame_8)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setStyleSheet(u"QLineEdit {\n"
"    background: white; /* Set a solid background color */\n"
"    border: 1px solid rgb(59, 103, 59); /* Set a border color */\n"
"    border-radius: 4px; /* Optional: rounded corners */\n"
"    color: rgb(0, 0, 0); /* Text color */\n"
"    padding: 5px; /* Optional: padding inside the line edit */\n"
"}")
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_17)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_21 = QFrame(self.frame_17)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setStyleSheet(u"")
        self.frame_21.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_21)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_21 = QLabel(self.frame_21)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_6.addWidget(self.label_21, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(373, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 1, 1, 1)

        self.pushButton_help_API = QPushButton(self.frame_21)
        self.pushButton_help_API.setObjectName(u"pushButton_help_API")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_help_API.sizePolicy().hasHeightForWidth())
        self.pushButton_help_API.setSizePolicy(sizePolicy4)
        self.pushButton_help_API.setMinimumSize(QSize(23, 23))
        font3 = QFont()
        font3.setPointSize(12)
        self.pushButton_help_API.setFont(font3)
        self.pushButton_help_API.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_help_API.setStyleSheet(u"")
        self.pushButton_help_API.setFlat(True)

        self.gridLayout_6.addWidget(self.pushButton_help_API, 0, 2, 1, 1)

        self.lineEdit_api = QLineEdit(self.frame_21)
        self.lineEdit_api.setObjectName(u"lineEdit_api")
        self.lineEdit_api.setMinimumSize(QSize(0, 30))

        self.gridLayout_6.addWidget(self.lineEdit_api, 1, 0, 1, 2)


        self.verticalLayout_15.addWidget(self.frame_21)

        self.frame_18 = QFrame(self.frame_17)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_18)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_22 = QLabel(self.frame_18)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_7.addWidget(self.label_22, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(388, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)

        self.pushButton_help_API_2 = QPushButton(self.frame_18)
        self.pushButton_help_API_2.setObjectName(u"pushButton_help_API_2")
        sizePolicy4.setHeightForWidth(self.pushButton_help_API_2.sizePolicy().hasHeightForWidth())
        self.pushButton_help_API_2.setSizePolicy(sizePolicy4)
        self.pushButton_help_API_2.setMinimumSize(QSize(23, 23))
        self.pushButton_help_API_2.setFont(font3)
        self.pushButton_help_API_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_help_API_2.setStyleSheet(u"")
        self.pushButton_help_API_2.setFlat(True)

        self.gridLayout_7.addWidget(self.pushButton_help_API_2, 0, 2, 1, 1)

        self.lineEdit_name = QLineEdit(self.frame_18)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        self.lineEdit_name.setMinimumSize(QSize(0, 30))

        self.gridLayout_7.addWidget(self.lineEdit_name, 1, 0, 1, 2)


        self.verticalLayout_15.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.frame_17)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_41 = QVBoxLayout(self.frame_19)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.label_23 = QLabel(self.frame_19)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_41.addWidget(self.label_23)

        self.lineEdit_email = QLineEdit(self.frame_19)
        self.lineEdit_email.setObjectName(u"lineEdit_email")
        self.lineEdit_email.setMinimumSize(QSize(0, 30))

        self.verticalLayout_41.addWidget(self.lineEdit_email)


        self.verticalLayout_15.addWidget(self.frame_19)

        self.frame_20 = QFrame(self.frame_17)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_42 = QVBoxLayout(self.frame_20)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.label_24 = QLabel(self.frame_20)
        self.label_24.setObjectName(u"label_24")

        self.verticalLayout_42.addWidget(self.label_24)

        self.lineEdit_aff = QLineEdit(self.frame_20)
        self.lineEdit_aff.setObjectName(u"lineEdit_aff")
        self.lineEdit_aff.setMinimumSize(QSize(0, 30))

        self.verticalLayout_42.addWidget(self.lineEdit_aff)


        self.verticalLayout_15.addWidget(self.frame_20)


        self.verticalLayout_8.addWidget(self.frame_17)


        self.horizontalLayout_17.addWidget(self.frame_8)


        self.verticalLayout_14.addWidget(self.frame_10)

        self.frame_22 = QFrame(self.frame_15)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_save_solarinput = QPushButton(self.frame_22)
        self.pushButton_save_solarinput.setObjectName(u"pushButton_save_solarinput")
        self.pushButton_save_solarinput.setMinimumSize(QSize(87, 23))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(18)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_save_solarinput.setFont(font4)
        self.pushButton_save_solarinput.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_5.addWidget(self.pushButton_save_solarinput)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.pushButton_skip_API = QPushButton(self.frame_22)
        self.pushButton_skip_API.setObjectName(u"pushButton_skip_API")
        self.pushButton_skip_API.setMinimumSize(QSize(40, 23))
        self.pushButton_skip_API.setFont(font4)
        self.pushButton_skip_API.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_5.addWidget(self.pushButton_skip_API)

        self.pushButton_help_API_3 = QPushButton(self.frame_22)
        self.pushButton_help_API_3.setObjectName(u"pushButton_help_API_3")
        self.pushButton_help_API_3.setMinimumSize(QSize(23, 23))
        self.pushButton_help_API_3.setFont(font3)
        self.pushButton_help_API_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_help_API_3.setStyleSheet(u"")
        self.pushButton_help_API_3.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_help_API_3)


        self.verticalLayout_14.addWidget(self.frame_22)

        self.verticalLayout_14.setStretch(0, 1)

        self.horizontalLayout_18.addWidget(self.frame_15)

        self.horizontalSpacer_3 = QSpacerItem(720, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_3)


        self.verticalLayout_17.addWidget(self.frame_16)

        self.widget_16 = QWidget(self.widget_3)
        self.widget_16.setObjectName(u"widget_16")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_16)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.pushButton_DI_previous_4 = QPushButton(self.widget_16)
        self.pushButton_DI_previous_4.setObjectName(u"pushButton_DI_previous_4")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.pushButton_DI_previous_4.sizePolicy().hasHeightForWidth())
        self.pushButton_DI_previous_4.setSizePolicy(sizePolicy5)
        self.pushButton_DI_previous_4.setMinimumSize(QSize(69, 25))
        self.pushButton_DI_previous_4.setFont(font4)
        self.pushButton_DI_previous_4.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_13.addWidget(self.pushButton_DI_previous_4)

        self.horizontalSpacer_14 = QSpacerItem(1023, 45, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_14)

        self.pushButton_DI_next_4 = QPushButton(self.widget_16)
        self.pushButton_DI_next_4.setObjectName(u"pushButton_DI_next_4")
        self.pushButton_DI_next_4.setMinimumSize(QSize(52, 25))
        self.pushButton_DI_next_4.setFont(font4)
        self.pushButton_DI_next_4.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_13.addWidget(self.pushButton_DI_next_4)


        self.verticalLayout_17.addWidget(self.widget_16)

        self.verticalLayout_17.setStretch(0, 1)

        self.verticalLayout_16.addWidget(self.widget_3)


        self.verticalLayout_11.addWidget(self.widget_13)

        self.tabWidget.addTab(self.api_tab, "")
        self.solar_tab = QWidget()
        self.solar_tab.setObjectName(u"solar_tab")
        self.gridLayout_2 = QGridLayout(self.solar_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.stackedWidget_2 = QStackedWidget(self.solar_tab)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.stackedWidget_2.sizePolicy().hasHeightForWidth())
        self.stackedWidget_2.setSizePolicy(sizePolicy6)
        font5 = QFont()
        font5.setPointSize(9)
        self.stackedWidget_2.setFont(font5)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        sizePolicy6.setHeightForWidth(self.page_4.sizePolicy().hasHeightForWidth())
        self.page_4.setSizePolicy(sizePolicy6)
        self.gridLayout_5 = QGridLayout(self.page_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.frame_4 = QFrame(self.page_4)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy6.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy6)
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.widget_6 = QWidget(self.frame_4)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy6.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy6)
        self.gridLayout = QGridLayout(self.widget_6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_solar_upload = QPushButton(self.widget_6)
        self.pushButton_solar_upload.setObjectName(u"pushButton_solar_upload")
        self.pushButton_solar_upload.setStyleSheet(u"font: 18pt \"Arial\";")

        self.gridLayout.addWidget(self.pushButton_solar_upload, 1, 0, 1, 1)

        self.pushButton_solar_dl = QPushButton(self.widget_6)
        self.pushButton_solar_dl.setObjectName(u"pushButton_solar_dl")
        self.pushButton_solar_dl.setEnabled(True)
        self.pushButton_solar_dl.setMinimumSize(QSize(143, 0))
        self.pushButton_solar_dl.setFont(font4)
        self.pushButton_solar_dl.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_solar_dl.setStyleSheet(u"\n"
"font: 18pt \"Arial\";")

        self.gridLayout.addWidget(self.pushButton_solar_dl, 3, 0, 1, 1)

        self.textBrowser_4 = QTextBrowser(self.widget_6)
        self.textBrowser_4.setObjectName(u"textBrowser_4")
        self.textBrowser_4.setStyleSheet(u"")
        self.textBrowser_4.setFrameShape(QFrame.Shape.NoFrame)

        self.gridLayout.addWidget(self.textBrowser_4, 0, 1, 3, 1)

        self.widget_5 = QWidget(self.widget_6)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setEnabled(True)
        sizePolicy6.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy6)
        self.verticalLayout_9 = QVBoxLayout(self.widget_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_9.addWidget(self.label_3)

        self.lineEdit_starty = QLineEdit(self.widget_5)
        self.lineEdit_starty.setObjectName(u"lineEdit_starty")
        self.lineEdit_starty.setEnabled(True)
        self.lineEdit_starty.setMinimumSize(QSize(0, 30))

        self.verticalLayout_9.addWidget(self.lineEdit_starty)

        self.label_26 = QLabel(self.widget_5)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setEnabled(True)

        self.verticalLayout_9.addWidget(self.label_26)

        self.lineEdit_endy = QLineEdit(self.widget_5)
        self.lineEdit_endy.setObjectName(u"lineEdit_endy")
        self.lineEdit_endy.setMinimumSize(QSize(0, 30))

        self.verticalLayout_9.addWidget(self.lineEdit_endy)


        self.gridLayout.addWidget(self.widget_5, 2, 0, 1, 1)

        self.widget_4 = QWidget(self.widget_6)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy7)
        self.verticalLayout = QVBoxLayout(self.widget_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_20 = QLabel(self.widget_4)
        self.label_20.setObjectName(u"label_20")
        sizePolicy7.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy7)

        self.verticalLayout.addWidget(self.label_20)

        self.comboBox_2 = QComboBox(self.widget_4)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy5.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy5)
        self.comboBox_2.setMinimumSize(QSize(0, 30))
        self.comboBox_2.setStyleSheet(u"QComboBox {\n"
"    background: white;\n"
"    border: 1px solid rgb(59, 103, 59);\n"
"    border-radius: 4px;\n"
"    color: rgb(0, 0, 0);\n"
"    padding: 5px;\n"
"}\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: white;\n"
"    border: 1px solid rgb(59, 103, 59);\n"
"    selection-background-color: rgb(59, 103, 59);\n"
"    selection-color: white;\n"
"}")
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setMaxVisibleItems(10)

        self.verticalLayout.addWidget(self.comboBox_2)


        self.gridLayout.addWidget(self.widget_4, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.widget_6, 0, 0, 1, 1)

        self.widget_10 = QWidget(self.frame_4)
        self.widget_10.setObjectName(u"widget_10")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy8)
        self.horizontalLayout = QHBoxLayout(self.widget_10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_DI_previous_2 = QPushButton(self.widget_10)
        self.pushButton_DI_previous_2.setObjectName(u"pushButton_DI_previous_2")
        self.pushButton_DI_previous_2.setMinimumSize(QSize(55, 25))
        self.pushButton_DI_previous_2.setSizeIncrement(QSize(0, 0))
        self.pushButton_DI_previous_2.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout.addWidget(self.pushButton_DI_previous_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_DI_next_2 = QPushButton(self.widget_10)
        self.pushButton_DI_next_2.setObjectName(u"pushButton_DI_next_2")
        self.pushButton_DI_next_2.setEnabled(True)
        self.pushButton_DI_next_2.setMinimumSize(QSize(45, 25))
        self.pushButton_DI_next_2.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout.addWidget(self.pushButton_DI_next_2)


        self.gridLayout_4.addWidget(self.widget_10, 1, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 0, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_23 = QVBoxLayout(self.page_5)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.frame_32 = QFrame(self.page_5)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_27.setSpacing(6)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.frame_33 = QFrame(self.frame_32)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_33.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_33)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.frame_33)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_24 = QVBoxLayout(self.widget)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.frame_28 = QFrame(self.widget)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_28)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.frame_14 = QFrame(self.frame_28)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setStyleSheet(u"QLineEdit {\n"
"    background: white; /* Set a solid background color */\n"
"    border: 1px solid rgb(59, 103, 59); /* Set a border color */\n"
"    border-radius: 4px; /* Optional: rounded corners */\n"
"    color: rgb(0, 0, 0); /* Text color */\n"
"    padding: 5px; /* Optional: padding inside the line edit */\n"
"}\n"
"QFrame {\n"
"	background-color:transparent;\n"
"	border:none;\n"
"}")
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_14)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.pushButton = QPushButton(self.frame_14)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"font: 18pt \"Arial\";")

        self.gridLayout_8.addWidget(self.pushButton, 0, 0, 1, 1)

        self.pushButton_help_solar = QPushButton(self.frame_14)
        self.pushButton_help_solar.setObjectName(u"pushButton_help_solar")
        self.pushButton_help_solar.setMinimumSize(QSize(25, 23))
        self.pushButton_help_solar.setFont(font3)
        self.pushButton_help_solar.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_help_solar.setStyleSheet(u"")
        self.pushButton_help_solar.setFlat(True)

        self.gridLayout_8.addWidget(self.pushButton_help_solar, 0, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(158, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_9, 0, 2, 1, 1)

        self.label_5 = QLabel(self.frame_14)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_8.addWidget(self.label_5, 1, 0, 1, 3)

        self.lineEdit = QLineEdit(self.frame_14)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))

        self.gridLayout_8.addWidget(self.lineEdit, 2, 0, 1, 3)


        self.verticalLayout_20.addWidget(self.frame_14)

        self.frame_27 = QFrame(self.frame_28)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_16)

        self.pushButton_2 = QPushButton(self.frame_27)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(135, 0))
        self.pushButton_2.setSizeIncrement(QSize(0, 0))
        self.pushButton_2.setFont(font4)
        self.pushButton_2.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_22.addWidget(self.pushButton_2)

        self.pushButton_api_8 = QPushButton(self.frame_27)
        self.pushButton_api_8.setObjectName(u"pushButton_api_8")
        self.pushButton_api_8.setMinimumSize(QSize(25, 23))
        self.pushButton_api_8.setFont(font3)
        self.pushButton_api_8.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_api_8.setStyleSheet(u"")
        self.pushButton_api_8.setFlat(True)

        self.horizontalLayout_22.addWidget(self.pushButton_api_8)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_8)


        self.verticalLayout_20.addWidget(self.frame_27)


        self.verticalLayout_24.addWidget(self.frame_28)


        self.verticalLayout_22.addWidget(self.widget)

        self.widget_2 = QWidget(self.frame_33)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_21 = QVBoxLayout(self.widget_2)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.frame_30 = QFrame(self.widget_2)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_43 = QVBoxLayout(self.frame_30)
        self.verticalLayout_43.setSpacing(0)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.frame_54 = QFrame(self.frame_30)
        self.frame_54.setObjectName(u"frame_54")
        self.frame_54.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_54.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_54)
        self.verticalLayout_38.setSpacing(0)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.frame_54)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_38.addWidget(self.label_6)

        self.lineEdit_2 = QLineEdit(self.frame_54)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(0, 30))

        self.verticalLayout_38.addWidget(self.lineEdit_2)


        self.verticalLayout_43.addWidget(self.frame_54)


        self.verticalLayout_21.addWidget(self.frame_30)

        self.frame_31 = QFrame(self.widget_2)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_17)

        self.pushButton_3 = QPushButton(self.frame_31)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(135, 0))
        self.pushButton_3.setFont(font4)
        self.pushButton_3.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_25.addWidget(self.pushButton_3)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_18)


        self.verticalLayout_21.addWidget(self.frame_31)


        self.verticalLayout_22.addWidget(self.widget_2)


        self.horizontalLayout_27.addWidget(self.frame_33)

        self.frame_29 = QFrame(self.frame_32)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_29.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_23.setSpacing(6)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_6 = QTextBrowser(self.frame_29)
        self.textBrowser_6.setObjectName(u"textBrowser_6")
        self.textBrowser_6.setStyleSheet(u"")

        self.horizontalLayout_23.addWidget(self.textBrowser_6)

        self.textBrowser_5 = QTextBrowser(self.frame_29)
        self.textBrowser_5.setObjectName(u"textBrowser_5")
        self.textBrowser_5.setStyleSheet(u"")
        self.textBrowser_5.setFrameShape(QFrame.Shape.Box)

        self.horizontalLayout_23.addWidget(self.textBrowser_5)

        self.horizontalLayout_23.setStretch(0, 2)
        self.horizontalLayout_23.setStretch(1, 1)

        self.horizontalLayout_27.addWidget(self.frame_29)

        self.horizontalLayout_27.setStretch(1, 1)

        self.verticalLayout_23.addWidget(self.frame_32)

        self.widget_17 = QWidget(self.page_5)
        self.widget_17.setObjectName(u"widget_17")
        self.horizontalLayout_26 = QHBoxLayout(self.widget_17)
        self.horizontalLayout_26.setSpacing(0)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.pushButton_DI_previous_5 = QPushButton(self.widget_17)
        self.pushButton_DI_previous_5.setObjectName(u"pushButton_DI_previous_5")
        sizePolicy5.setHeightForWidth(self.pushButton_DI_previous_5.sizePolicy().hasHeightForWidth())
        self.pushButton_DI_previous_5.setSizePolicy(sizePolicy5)
        self.pushButton_DI_previous_5.setMinimumSize(QSize(55, 25))
        self.pushButton_DI_previous_5.setFont(font4)
        self.pushButton_DI_previous_5.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_26.addWidget(self.pushButton_DI_previous_5)

        self.horizontalSpacer_15 = QSpacerItem(1023, 45, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_15)

        self.pushButton_DI_next_5 = QPushButton(self.widget_17)
        self.pushButton_DI_next_5.setObjectName(u"pushButton_DI_next_5")
        self.pushButton_DI_next_5.setMinimumSize(QSize(45, 25))
        self.pushButton_DI_next_5.setFont(font4)
        self.pushButton_DI_next_5.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_26.addWidget(self.pushButton_DI_next_5)


        self.verticalLayout_23.addWidget(self.widget_17)

        self.verticalLayout_23.setStretch(0, 1)
        self.stackedWidget_2.addWidget(self.page_5)

        self.gridLayout_2.addWidget(self.stackedWidget_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.solar_tab, "")
        self.wind_tab = QWidget()
        self.wind_tab.setObjectName(u"wind_tab")
        self.wind_tab.setStyleSheet(u"")
        self.gridLayout_14 = QGridLayout(self.wind_tab)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.frame_55 = QFrame(self.wind_tab)
        self.frame_55.setObjectName(u"frame_55")
        self.frame_55.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_55.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_55)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.textBrowser_3 = QTextBrowser(self.frame_55)
        self.textBrowser_3.setObjectName(u"textBrowser_3")
        self.textBrowser_3.setStyleSheet(u"")

        self.gridLayout_12.addWidget(self.textBrowser_3, 0, 1, 4, 1)

        self.widget_12 = QWidget(self.frame_55)
        self.widget_12.setObjectName(u"widget_12")
        self.gridLayout_11 = QGridLayout(self.widget_12)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.pushButton_4 = QPushButton(self.widget_12)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setFont(font4)
        self.pushButton_4.setStyleSheet(u"font: 18pt \"Arial\";")
        self.pushButton_4.setFlat(True)

        self.gridLayout_11.addWidget(self.pushButton_4, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_7 = QPushButton(self.widget_12)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy9)
        self.pushButton_7.setFont(font4)
        self.pushButton_7.setStyleSheet(u"font: 18pt \"Arial\";")
        self.pushButton_7.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_7)

        self.pushButton_help_wind = QPushButton(self.widget_12)
        self.pushButton_help_wind.setObjectName(u"pushButton_help_wind")
        sizePolicy3.setHeightForWidth(self.pushButton_help_wind.sizePolicy().hasHeightForWidth())
        self.pushButton_help_wind.setSizePolicy(sizePolicy3)
        self.pushButton_help_wind.setMinimumSize(QSize(0, 0))
        self.pushButton_help_wind.setFont(font3)
        self.pushButton_help_wind.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_help_wind.setStyleSheet(u"")
        self.pushButton_help_wind.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_help_wind)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_13)


        self.gridLayout_11.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.gridLayout_12.addWidget(self.widget_12, 3, 0, 1, 1)

        self.widget_9 = QWidget(self.frame_55)
        self.widget_9.setObjectName(u"widget_9")
        self.gridLayout_10 = QGridLayout(self.widget_9)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_31 = QLabel(self.widget_9)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_10.addWidget(self.label_31, 0, 0, 1, 1)

        self.lineEdit_22 = QLineEdit(self.widget_9)
        self.lineEdit_22.setObjectName(u"lineEdit_22")
        self.lineEdit_22.setMinimumSize(QSize(0, 30))

        self.gridLayout_10.addWidget(self.lineEdit_22, 1, 0, 1, 1)

        self.label_32 = QLabel(self.widget_9)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_10.addWidget(self.label_32, 2, 0, 1, 1)

        self.lineEdit_23 = QLineEdit(self.widget_9)
        self.lineEdit_23.setObjectName(u"lineEdit_23")
        self.lineEdit_23.setMinimumSize(QSize(0, 30))

        self.gridLayout_10.addWidget(self.lineEdit_23, 3, 0, 1, 1)


        self.gridLayout_12.addWidget(self.widget_9, 2, 0, 1, 1)

        self.widget_8 = QWidget(self.frame_55)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy6.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy6)
        self.verticalLayout_2 = QVBoxLayout(self.widget_8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_27 = QLabel(self.widget_8)
        self.label_27.setObjectName(u"label_27")
        sizePolicy2.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy2)
        self.label_27.setMaximumSize(QSize(100, 100))

        self.verticalLayout_2.addWidget(self.label_27)

        self.comboBox_3 = QComboBox(self.widget_8)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setMinimumSize(QSize(0, 30))
        self.comboBox_3.setStyleSheet(u"QComboBox {\n"
"    background: white;\n"
"    border: 1px solid rgb(59, 103, 59);\n"
"    border-radius: 4px;\n"
"    color: rgb(0, 0, 0);\n"
"    padding: 5px;\n"
"}\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: white;\n"
"    border: 1px solid rgb(59, 103, 59);\n"
"    selection-background-color: rgb(59, 103, 59);\n"
"    selection-color: white;\n"
"}")
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setMaxVisibleItems(10)

        self.verticalLayout_2.addWidget(self.comboBox_3)

        self.pushButton_wind_upload = QPushButton(self.widget_8)
        self.pushButton_wind_upload.setObjectName(u"pushButton_wind_upload")
        self.pushButton_wind_upload.setStyleSheet(u"font: 18pt \"Arial\";")

        self.verticalLayout_2.addWidget(self.pushButton_wind_upload)


        self.gridLayout_12.addWidget(self.widget_8, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_55, 0, 0, 1, 1)

        self.widget_11 = QWidget(self.wind_tab)
        self.widget_11.setObjectName(u"widget_11")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_DI_previous_3 = QPushButton(self.widget_11)
        self.pushButton_DI_previous_3.setObjectName(u"pushButton_DI_previous_3")
        self.pushButton_DI_previous_3.setFont(font4)
        self.pushButton_DI_previous_3.setStyleSheet(u"font: 18pt \"Arial\";")
        self.pushButton_DI_previous_3.setFlat(True)

        self.horizontalLayout_7.addWidget(self.pushButton_DI_previous_3)

        self.horizontalSpacer_11 = QSpacerItem(1023, 45, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)

        self.pushButton_DI_next_3 = QPushButton(self.widget_11)
        self.pushButton_DI_next_3.setObjectName(u"pushButton_DI_next_3")
        self.pushButton_DI_next_3.setFont(font4)
        self.pushButton_DI_next_3.setStyleSheet(u"font: 18pt \"Arial\";")
        self.pushButton_DI_next_3.setFlat(True)

        self.horizontalLayout_7.addWidget(self.pushButton_DI_next_3)


        self.gridLayout_14.addWidget(self.widget_11, 1, 0, 1, 1)

        self.tabWidget.addTab(self.wind_tab, "")
        self.sim_tab = QWidget()
        self.sim_tab.setObjectName(u"sim_tab")
        self.verticalLayout_10 = QVBoxLayout(self.sim_tab)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.widget_7 = QWidget(self.sim_tab)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_27 = QVBoxLayout(self.widget_7)
        self.verticalLayout_27.setSpacing(0)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.frame_44 = QFrame(self.widget_7)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_44.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_44)
        self.horizontalLayout_36.setSpacing(0)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.frame_43 = QFrame(self.frame_44)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_43.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.frame_43)
        self.verticalLayout_26.setSpacing(0)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.frame_37 = QFrame(self.frame_43)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setMinimumSize(QSize(0, 30))
        self.frame_37.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_37.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_37)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.frame_37)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_13.addWidget(self.label_12)

        self.lineEdit_4 = QLineEdit(self.frame_37)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.verticalLayout_13.addWidget(self.lineEdit_4)


        self.verticalLayout_26.addWidget(self.frame_37)

        self.frame_38 = QFrame(self.frame_43)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_38.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_38)
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.label_17 = QLabel(self.frame_38)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_28.addWidget(self.label_17)

        self.lineEdit_5 = QLineEdit(self.frame_38)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(0, 30))

        self.verticalLayout_28.addWidget(self.lineEdit_5)


        self.verticalLayout_26.addWidget(self.frame_38)

        self.frame_39 = QFrame(self.frame_43)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_39.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.frame_39)
        self.verticalLayout_29.setSpacing(0)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.frame_39)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_29.addWidget(self.label_19)

        self.lineEdit_6 = QLineEdit(self.frame_39)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMinimumSize(QSize(0, 30))

        self.verticalLayout_29.addWidget(self.lineEdit_6)


        self.verticalLayout_26.addWidget(self.frame_39)

        self.frame_40 = QFrame(self.frame_43)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_40.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.frame_40)
        self.verticalLayout_30.setSpacing(0)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.label_18 = QLabel(self.frame_40)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_30.addWidget(self.label_18)

        self.comboBox = QComboBox(self.frame_40)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(0, 30))
        self.comboBox.setStyleSheet(u"QComboBox {\n"
"    background: white;\n"
"    border: 1px solid rgb(59, 103, 59);\n"
"    border-radius: 4px;\n"
"    color: rgb(0, 0, 0);\n"
"    padding: 5px;\n"
"}\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: white;\n"
"    border: 1px solid rgb(59, 103, 59);\n"
"    selection-background-color: rgb(59, 103, 59);\n"
"    selection-color: white;\n"
"}")
        self.comboBox.setEditable(False)
        self.comboBox.setMaxVisibleItems(10)

        self.verticalLayout_30.addWidget(self.comboBox)


        self.verticalLayout_26.addWidget(self.frame_40)

        self.frame_41 = QFrame(self.frame_43)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_41.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_35.setSpacing(0)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_19)

        self.pushButton_5 = QPushButton(self.frame_41)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setFont(font4)
        self.pushButton_5.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_35.addWidget(self.pushButton_5)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_12)


        self.verticalLayout_26.addWidget(self.frame_41, 0, Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_36.addWidget(self.frame_43)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_36.addItem(self.horizontalSpacer_24)

        self.textBrowser_2 = QTextBrowser(self.frame_44)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setStyleSheet(u"")

        self.horizontalLayout_36.addWidget(self.textBrowser_2)

        self.horizontalLayout_36.setStretch(0, 1)
        self.horizontalLayout_36.setStretch(2, 3)

        self.verticalLayout_27.addWidget(self.frame_44)

        self.frame_42 = QFrame(self.widget_7)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_42.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_42)
        self.horizontalLayout_37.setSpacing(0)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.pushButton_sim_previous = QPushButton(self.frame_42)
        self.pushButton_sim_previous.setObjectName(u"pushButton_sim_previous")
        self.pushButton_sim_previous.setFont(font4)
        self.pushButton_sim_previous.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_37.addWidget(self.pushButton_sim_previous)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_10)

        self.pushButton_6 = QPushButton(self.frame_42)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setFont(font4)
        self.pushButton_6.setStyleSheet(u"font: 18pt \"Arial\";")

        self.horizontalLayout_37.addWidget(self.pushButton_6)


        self.verticalLayout_27.addWidget(self.frame_42)

        self.verticalLayout_27.setStretch(0, 1)

        self.verticalLayout_10.addWidget(self.widget_7)

        self.tabWidget.addTab(self.sim_tab, "")
        self.results_tab = QWidget()
        self.results_tab.setObjectName(u"results_tab")
        self.verticalLayout_45 = QVBoxLayout(self.results_tab)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.tabWidget_2 = QTabWidget(self.results_tab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setTabPosition(QTabWidget.TabPosition.South)
        self.tabWidget_2.setElideMode(Qt.TextElideMode.ElideNone)
        self.tabWidget_2.setUsesScrollButtons(True)
        self.tabWidget_2.setDocumentMode(False)
        self.tabWidget_2.setTabsClosable(False)
        self.tabWidget_2.setMovable(False)
        self.tabWidget_2.setTabBarAutoHide(False)
        self.COV_tab = QWidget()
        self.COV_tab.setObjectName(u"COV_tab")
        self.horizontalLayout_16 = QHBoxLayout(self.COV_tab)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.verticalLayout_46 = QVBoxLayout()
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")

        self.horizontalLayout_16.addLayout(self.verticalLayout_46)

        self.tabWidget_2.addTab(self.COV_tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_50 = QVBoxLayout(self.tab_3)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.verticalLayout_49 = QVBoxLayout()
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")

        self.verticalLayout_50.addLayout(self.verticalLayout_49)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_52 = QVBoxLayout(self.tab_4)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.verticalLayout_51 = QVBoxLayout()
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")

        self.verticalLayout_52.addLayout(self.verticalLayout_51)

        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_54 = QVBoxLayout(self.tab_5)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.verticalLayout_53 = QVBoxLayout()
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")

        self.verticalLayout_54.addLayout(self.verticalLayout_53)

        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_56 = QVBoxLayout(self.tab_6)
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.verticalLayout_55 = QVBoxLayout()
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")

        self.verticalLayout_56.addLayout(self.verticalLayout_55)

        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.verticalLayout_60 = QVBoxLayout(self.tab_8)
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.verticalLayout_59 = QVBoxLayout()
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")

        self.verticalLayout_60.addLayout(self.verticalLayout_59)

        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_48 = QVBoxLayout(self.tab_2)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.verticalLayout_47 = QVBoxLayout()
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")

        self.verticalLayout_48.addLayout(self.verticalLayout_47)

        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.verticalLayout_62 = QVBoxLayout(self.tab_9)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.verticalLayout_61 = QVBoxLayout()
        self.verticalLayout_61.setObjectName(u"verticalLayout_61")

        self.verticalLayout_62.addLayout(self.verticalLayout_61)

        self.tabWidget_2.addTab(self.tab_9, "")

        self.verticalLayout_45.addWidget(self.tabWidget_2)

        self.tabWidget.addTab(self.results_tab, "")
        self.about_tab = QWidget()
        self.about_tab.setObjectName(u"about_tab")
        self.verticalLayout_63 = QVBoxLayout(self.about_tab)
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.label = QLabel(self.about_tab)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setPointSize(20)
        self.label.setFont(font6)

        self.verticalLayout_63.addWidget(self.label)

        self.tabWidget.addTab(self.about_tab, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_13 = QGridLayout(self.page_3)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.stackedWidget.addWidget(self.page_3)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QuESt ProGRESS", None))
        self.actionInfo.setText(QCoreApplication.translate("MainWindow", u"Documentation  ", None))
        self.actionOptions.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.actionMore_Info.setText(QCoreApplication.translate("MainWindow", u"More Info", None))
        self.actionContact.setText(QCoreApplication.translate("MainWindow", u"Contact", None))
        self.actionFAQ.setText(QCoreApplication.translate("MainWindow", u"FAQ", None))
        self.actionAnything.setText(QCoreApplication.translate("MainWindow", u"Anything", None))
        self.actionHome_Page.setText(QCoreApplication.translate("MainWindow", u"Home Page", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:64pt; color:#00670f;\">Probabilistic Grid Reliability Analysis with Energy Storage Systems</span></p></body></html>", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Helvetica Neue'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Aptos','sans-serif'; font-size:24pt;\">A Python-based open-source tool for assessing the resource adequacy of the evolving electric power grid integrated with energy storage systems.</span></p></body></html>", None))
        self.pushButton_getStarted.setText(QCoreApplication.translate("MainWindow", u"  Get Started  ", None))
        self.label_15.setText("")
        self.label_16.setText("")
        self.label_7.setText("")
        self.textBrowser_7.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Helvetica Neue'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:18pt; font-weight:700;\">Acknowledgement</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:18pt;\">This material is based upon worked supported by the U.S. Deparment of Energy, Office of Electricity (OE), Energy S"
                        "torage Division.</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), "")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"API Key:", None))
        self.pushButton_help_API.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.lineEdit_api.setText("")
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.pushButton_help_API_2.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.lineEdit_name.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Email ID:", None))
        self.lineEdit_email.setText("")
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Affiliation:", None))
        self.lineEdit_aff.setText("")
        self.pushButton_save_solarinput.setText(QCoreApplication.translate("MainWindow", u"Save Input", None))
        self.pushButton_skip_API.setText(QCoreApplication.translate("MainWindow", u"Skip", None))
        self.pushButton_help_API_3.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.pushButton_DI_previous_4.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.pushButton_DI_next_4.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.api_tab), QCoreApplication.translate("MainWindow", u"API Key", None))
        self.pushButton_solar_upload.setText(QCoreApplication.translate("MainWindow", u"Upload Data", None))
        self.pushButton_solar_dl.setText(QCoreApplication.translate("MainWindow", u"Download Solar Data", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Start Year:", None))
        self.lineEdit_starty.setText("")
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"End Year:", None))
        self.lineEdit_endy.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Datal input:", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"--Select Option--", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Download Solar Data from NSRDB", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Use Own Data", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"No Solar", None))

        self.pushButton_DI_previous_2.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.pushButton_DI_next_2.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Skip", None))
        self.pushButton_help_solar.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"No. of Clusters to Evaluate:", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Evaluate Clusters", None))
        self.pushButton_api_8.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Final No. of clusters:", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Generate Clusters", None))
        self.pushButton_DI_previous_5.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.pushButton_DI_next_5.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.solar_tab), QCoreApplication.translate("MainWindow", u"Solar", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Download Wind Speed Data", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Process Wind Speed Data", None))
        self.pushButton_help_wind.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Start Year:", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"End Year:", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Datal input:", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("MainWindow", u"--Select Option--", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("MainWindow", u"Download Wind Data from WIND Toolkit", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("MainWindow", u"Use Own Data", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("MainWindow", u"No Wind", None))

        self.pushButton_wind_upload.setText(QCoreApplication.translate("MainWindow", u"Upload Data", None))
        self.pushButton_DI_previous_3.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.pushButton_DI_next_3.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.wind_tab), QCoreApplication.translate("MainWindow", u"Wind", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Samples:", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Simulation hours:", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"8760", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Load Factor", None))
        self.lineEdit_6.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Model type:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Zonal Model", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Copper Sheet Model", None))

        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Run Simulation", None))
        self.pushButton_sim_previous.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sim_tab), QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.COV_tab), QCoreApplication.translate("MainWindow", u"COV", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Loadcurt", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"LOLP", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"SOC", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Solar", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Wind", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Heatmap", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"Indices", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.results_tab), QCoreApplication.translate("MainWindow", u"Results", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"This page is under construction.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.about_tab), QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

