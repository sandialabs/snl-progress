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
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1183, 928)
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
        self.frame_ribbon = QFrame(self.centralwidget)
        self.frame_ribbon.setObjectName(u"frame_ribbon")
        self.frame_ribbon.setMinimumSize(QSize(150, 0))
        self.sidebarLayout = QVBoxLayout(self.frame_ribbon)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.branding_card = QFrame(self.frame_ribbon)
        self.branding_card.setObjectName(u"branding_card")
        self.branding_card.setAutoFillBackground(False)
        self.branding_card.setStyleSheet(u"frame.setStyleSheet(\"background-color: transparent;\")")
        self.horizontalLayout = QHBoxLayout(self.branding_card)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_logo = QLabel(self.branding_card)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setMaximumSize(QSize(70, 120))
        self.label_logo.setPixmap(QPixmap(u":/icons/Images/icons/progress_icon_up.png"))
        self.label_logo.setScaledContents(True)
        self.label_logo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_logo)


        self.sidebarLayout.addWidget(self.branding_card)

        self.btn_home = QPushButton(self.frame_ribbon)
        self.btn_home.setObjectName(u"btn_home")

        self.sidebarLayout.addWidget(self.btn_home)

        self.btn_solar = QPushButton(self.frame_ribbon)
        self.btn_solar.setObjectName(u"btn_solar")

        self.sidebarLayout.addWidget(self.btn_solar)

        self.btn_wind = QPushButton(self.frame_ribbon)
        self.btn_wind.setObjectName(u"btn_wind")

        self.sidebarLayout.addWidget(self.btn_wind)

        self.btn_simulation = QPushButton(self.frame_ribbon)
        self.btn_simulation.setObjectName(u"btn_simulation")

        self.sidebarLayout.addWidget(self.btn_simulation)

        self.btn_results = QPushButton(self.frame_ribbon)
        self.btn_results.setObjectName(u"btn_results")

        self.sidebarLayout.addWidget(self.btn_results)

        self.navSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.sidebarLayout.addItem(self.navSpacer)

        self.btn_settings = QPushButton(self.frame_ribbon)
        self.btn_settings.setObjectName(u"btn_settings")

        self.sidebarLayout.addWidget(self.btn_settings)

        self.btn_about = QPushButton(self.frame_ribbon)
        self.btn_about.setObjectName(u"btn_about")

        self.sidebarLayout.addWidget(self.btn_about)


        self.rootLayout.addWidget(self.frame_ribbon)

        self.frame_content = QFrame(self.centralwidget)
        self.frame_content.setObjectName(u"frame_content")
        self.frame_content.setMaximumSize(QSize(16777215, 1000))
        self.contentLayout = QVBoxLayout(self.frame_content)
        self.contentLayout.setObjectName(u"contentLayout")
        self.frame_info = QFrame(self.frame_content)
        self.frame_info.setObjectName(u"frame_info")
        self.headerLayout = QHBoxLayout(self.frame_info)
        self.headerLayout.setObjectName(u"headerLayout")
        self.label_page_title = QLabel(self.frame_info)
        self.label_page_title.setObjectName(u"label_page_title")

        self.headerLayout.addWidget(self.label_page_title)

        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.label_version = QLabel(self.frame_info)
        self.label_version.setObjectName(u"label_version")

        self.headerLayout.addWidget(self.label_version)


        self.contentLayout.addWidget(self.frame_info)

        self.stackedWidget = QStackedWidget(self.frame_content)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 0))
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

        self.frame_nav_btns = QFrame(self.frame_content)
        self.frame_nav_btns.setObjectName(u"frame_nav_btns")
        self.frame_nav_btns.setMaximumSize(QSize(16777215, 60))
        self.frame_nav_btns.setFrameShape(QFrame.NoFrame)
        self.frame_nav_btns.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_nav_btns)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_prev = QPushButton(self.frame_nav_btns)
        self.btn_prev.setObjectName(u"btn_prev")

        self.horizontalLayout_2.addWidget(self.btn_prev)

        self.btn_next = QPushButton(self.frame_nav_btns)
        self.btn_next.setObjectName(u"btn_next")

        self.horizontalLayout_2.addWidget(self.btn_next)


        self.contentLayout.addWidget(self.frame_nav_btns)

        self.contentLayout.setStretch(1, 1)

        self.rootLayout.addWidget(self.frame_content)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QuESt ProGRESS", None))
        self.label_logo.setText("")
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_solar.setText(QCoreApplication.translate("MainWindow", u"Solar Data", None))
        self.btn_wind.setText(QCoreApplication.translate("MainWindow", u"Wind Data", None))
        self.btn_simulation.setText(QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.btn_results.setText(QCoreApplication.translate("MainWindow", u"Results", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.btn_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label_page_title.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
        self.btn_prev.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.btn_next.setText(QCoreApplication.translate("MainWindow", u"Next", None))
    # retranslateUi

