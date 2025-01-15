# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'results_viewerZygaLc.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)
import progress.resources_rc

class Ui_results_widget(object):
    def setupUi(self, results_widget):
        if not results_widget.objectName():
            results_widget.setObjectName(u"results_widget")
        results_widget.resize(1080, 734)
        self.horizontalLayout = QHBoxLayout(results_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(results_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(230, 0))
        self.frame.setMaximumSize(QSize(230, 16777215))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.frame)

        self.file_min = QPushButton(results_widget)
        self.file_min.setObjectName(u"file_min")
        icon = QIcon()
        icon.addFile(u":/icons/Images/icons/more_vert_24dp_C8C8C8_FILL0_wght200_GRAD0_opsz24.png", QSize(), QIcon.Normal, QIcon.Off)
        self.file_min.setIcon(icon)
        self.file_min.setIconSize(QSize(16, 24))
        self.file_min.setFlat(True)

        self.horizontalLayout.addWidget(self.file_min)

        self.tabWidget = QTabWidget(results_widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"\n"
"    background-color: rgb(40, 40, 40); /* Dark background color */\n"
"    color: rgb(200, 200, 200); /* Light text color */\n"
"")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.South)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_3 = QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_3, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(results_widget)

        QMetaObject.connectSlotsByName(results_widget)
    # setupUi

    def retranslateUi(self, results_widget):
        results_widget.setWindowTitle(QCoreApplication.translate("results_widget", u"Form", None))
        self.file_min.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("results_widget", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("results_widget", u"Tab 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("results_widget", u"Tab 3", None))
    # retranslateUi

