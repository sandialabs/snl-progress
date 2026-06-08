# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1262, 928)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QHBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_frame = QFrame(self.centralwidget)
        self.sidebar_frame.setObjectName(u"sidebar_frame")
        self.sidebar_frame.setMinimumSize(QSize(150, 0))
        self.sidebarLayout = QVBoxLayout(self.sidebar_frame)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.branding_card = QFrame(self.sidebar_frame)
        self.branding_card.setObjectName(u"branding_card")
        self.branding_card.setAutoFillBackground(False)
        self.branding_card.setStyleSheet(u"frame.setStyleSheet(\"background-color: transparent;\")")
        self.brandingLayout = QVBoxLayout(self.branding_card)
        self.brandingLayout.setObjectName(u"brandingLayout")
        self.logo_label = QLabel(self.branding_card)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setMaximumSize(QSize(120, 50))
        self.logo_label.setPixmap(QPixmap(u":/logos/Images/logos/progress_transparent_alt.png"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.brandingLayout.addWidget(self.logo_label)


        self.sidebarLayout.addWidget(self.branding_card)

        self.btn_home = QPushButton(self.sidebar_frame)
        self.btn_home.setObjectName(u"btn_home")

        self.sidebarLayout.addWidget(self.btn_home)

        self.btn_solar = QPushButton(self.sidebar_frame)
        self.btn_solar.setObjectName(u"btn_solar")

        self.sidebarLayout.addWidget(self.btn_solar)

        self.btn_wind = QPushButton(self.sidebar_frame)
        self.btn_wind.setObjectName(u"btn_wind")

        self.sidebarLayout.addWidget(self.btn_wind)

        self.btn_simulation = QPushButton(self.sidebar_frame)
        self.btn_simulation.setObjectName(u"btn_simulation")

        self.sidebarLayout.addWidget(self.btn_simulation)

        self.btn_results = QPushButton(self.sidebar_frame)
        self.btn_results.setObjectName(u"btn_results")

        self.sidebarLayout.addWidget(self.btn_results)

        self.navSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.sidebarLayout.addItem(self.navSpacer)

        self.btn_settings = QPushButton(self.sidebar_frame)
        self.btn_settings.setObjectName(u"btn_settings")

        self.sidebarLayout.addWidget(self.btn_settings)

        self.btn_about = QPushButton(self.sidebar_frame)
        self.btn_about.setObjectName(u"btn_about")

        self.sidebarLayout.addWidget(self.btn_about)


        self.rootLayout.addWidget(self.sidebar_frame)

        self.content_frame = QFrame(self.centralwidget)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setMaximumSize(QSize(16777215, 1000))
        self.contentLayout = QVBoxLayout(self.content_frame)
        self.contentLayout.setObjectName(u"contentLayout")
        self.header_frame = QFrame(self.content_frame)
        self.header_frame.setObjectName(u"header_frame")
        self.headerLayout = QHBoxLayout(self.header_frame)
        self.headerLayout.setObjectName(u"headerLayout")
        self.page_title = QLabel(self.header_frame)
        self.page_title.setObjectName(u"page_title")

        self.headerLayout.addWidget(self.page_title)

        self.breadcrumb_label = QLabel(self.header_frame)
        self.breadcrumb_label.setObjectName(u"breadcrumb_label")

        self.headerLayout.addWidget(self.breadcrumb_label)

        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.version_label = QLabel(self.header_frame)
        self.version_label.setObjectName(u"version_label")

        self.headerLayout.addWidget(self.version_label)


        self.contentLayout.addWidget(self.header_frame)

        self.stackedWidget = QStackedWidget(self.content_frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background-color: transparent;")
        self.page_landing = QWidget()
        self.page_landing.setObjectName(u"page_landing")
        self.stackedWidget.addWidget(self.page_landing)
        self.page_solar = QWidget()
        self.page_solar.setObjectName(u"page_solar")
        self.stackedWidget.addWidget(self.page_solar)
        self.page_wind = QWidget()
        self.page_wind.setObjectName(u"page_wind")
        self.stackedWidget.addWidget(self.page_wind)
        self.page_simulation = QWidget()
        self.page_simulation.setObjectName(u"page_simulation")
        self.stackedWidget.addWidget(self.page_simulation)
        self.page_results = QWidget()
        self.page_results.setObjectName(u"page_results")
        self.stackedWidget.addWidget(self.page_results)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.stackedWidget.addWidget(self.page_settings)
        self.page_about = QWidget()
        self.page_about.setObjectName(u"page_about")
        self.stackedWidget.addWidget(self.page_about)

        self.contentLayout.addWidget(self.stackedWidget)

        self.status_frame = QFrame(self.content_frame)
        self.status_frame.setObjectName(u"status_frame")
        self.statusLayout = QHBoxLayout(self.status_frame)
        self.statusLayout.setObjectName(u"statusLayout")
        self.status_label = QLabel(self.status_frame)
        self.status_label.setObjectName(u"status_label")

        self.statusLayout.addWidget(self.status_label)

        self.statusSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.statusLayout.addItem(self.statusSpacer)

        self.project_label = QLabel(self.status_frame)
        self.project_label.setObjectName(u"project_label")

        self.statusLayout.addWidget(self.project_label)


        self.contentLayout.addWidget(self.status_frame)

        self.contentLayout.setStretch(1, 1)

        self.rootLayout.addWidget(self.content_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QuESt ProGRESS", None))
        self.logo_label.setText("")
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_solar.setText(QCoreApplication.translate("MainWindow", u"Solar Data", None))
        self.btn_wind.setText(QCoreApplication.translate("MainWindow", u"Wind Data", None))
        self.btn_simulation.setText(QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.btn_results.setText(QCoreApplication.translate("MainWindow", u"Results", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.btn_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.page_title.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.breadcrumb_label.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.version_label.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
        self.status_label.setText(QCoreApplication.translate("MainWindow", u"Ready", None))
        self.project_label.setText(QCoreApplication.translate("MainWindow", u"No Project Loaded", None))
    # retranslateUi

