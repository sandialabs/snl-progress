# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowJVojMk.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QTabWidget, QVBoxLayout,
    QWidget)
import progress.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1136, 575)
        palette = QPalette()
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet(u"")
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
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        palette1 = QPalette()
        brush = QBrush(QColor(0, 0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush)
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
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.page_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setIconSize(QSize(100, 32))
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideNone)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.tab_7.setStyleSheet(u"")
        self.verticalLayout_7 = QVBoxLayout(self.tab_7)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 20)
        icon = QIcon()
        icon.addFile(u":/logos/Images/logos/progress_transparent_alt.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tabWidget.addTab(self.tab_7, icon, "")
        self.api_tab = QWidget()
        self.api_tab.setObjectName(u"api_tab")
        self.api_tab.setStyleSheet(u"")
        self.verticalLayout_11 = QVBoxLayout(self.api_tab)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.api_tab, "")
        self.solar_tab = QWidget()
        self.solar_tab.setObjectName(u"solar_tab")
        self.solar_tab.setStyleSheet(u"")
        self.gridLayout_2 = QGridLayout(self.solar_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.solar_tab, "")
        self.wind_tab = QWidget()
        self.wind_tab.setObjectName(u"wind_tab")
        self.wind_tab.setStyleSheet(u"")
        self.gridLayout_14 = QGridLayout(self.wind_tab)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.gridLayout_14.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.wind_tab, "")
        self.sim_tab = QWidget()
        self.sim_tab.setObjectName(u"sim_tab")
        self.sim_tab.setStyleSheet(u"")
        self.verticalLayout_10 = QVBoxLayout(self.sim_tab)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.sim_tab, "")
        self.results_tab = QWidget()
        self.results_tab.setObjectName(u"results_tab")
        self.results_tab.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.results_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.results_tab, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_4 = QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.light_button = QPushButton(self.tab)
        self.light_button.setObjectName(u"light_button")
        self.light_button.setCheckable(True)
        self.light_button.setChecked(True)
        self.light_button.setAutoExclusive(True)

        self.verticalLayout_4.addWidget(self.light_button)

        self.dark_button = QPushButton(self.tab)
        self.dark_button.setObjectName(u"dark_button")
        self.dark_button.setCheckable(True)
        self.dark_button.setAutoExclusive(True)

        self.verticalLayout_4.addWidget(self.dark_button)

        self.tabWidget.addTab(self.tab, "")
        self.about_tab = QWidget()
        self.about_tab.setObjectName(u"about_tab")
        self.about_tab.setStyleSheet(u"")
        self.verticalLayout_63 = QVBoxLayout(self.about_tab)
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.verticalLayout_63.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.about_tab, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"")
        self.gridLayout_13 = QGridLayout(self.widget)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, -1, 7, -1)
        self.stackedWidget.addWidget(self.widget)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)


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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.api_tab), QCoreApplication.translate("MainWindow", u"API Key", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.solar_tab), QCoreApplication.translate("MainWindow", u"Solar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.wind_tab), QCoreApplication.translate("MainWindow", u"Wind", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sim_tab), QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.results_tab), QCoreApplication.translate("MainWindow", u"Results", None))
        self.light_button.setText(QCoreApplication.translate("MainWindow", u"Light Theme", None))
        self.dark_button.setText(QCoreApplication.translate("MainWindow", u"Dark Theme", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Themes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.about_tab), QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

