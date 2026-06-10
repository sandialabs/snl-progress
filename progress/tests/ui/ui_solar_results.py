# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solar_results.ui'
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
    QPlainTextEdit, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_SolarResults(object):
    def setupUi(self, SolarResults):
        if not SolarResults.objectName():
            SolarResults.setObjectName(u"SolarResults")
        SolarResults.resize(1211, 908)
        self.horizontalLayout = QHBoxLayout(SolarResults)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_plot = QFrame(SolarResults)
        self.frame_plot.setObjectName(u"frame_plot")
        self.frame_plot.setMaximumSize(QSize(2000, 16777215))
        self.frame_plot.setFrameShape(QFrame.WinPanel)
        self.frame_plot.setFrameShadow(QFrame.Sunken)
        self.verticalLayout = QVBoxLayout(self.frame_plot)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scroll_area_results = QScrollArea(self.frame_plot)
        self.scroll_area_results.setObjectName(u"scroll_area_results")
        self.scroll_area_results.setFrameShape(QFrame.NoFrame)
        self.scroll_area_results.setFrameShadow(QFrame.Sunken)
        self.scroll_area_results.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setObjectName(u"scroll_area_widget")
        self.scroll_area_widget.setGeometry(QRect(0, 0, 743, 856))
        self.verticalLayout_2 = QVBoxLayout(self.scroll_area_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_solar_plot = QLabel(self.scroll_area_widget)
        self.label_solar_plot.setObjectName(u"label_solar_plot")

        self.verticalLayout_2.addWidget(self.label_solar_plot)

        self.scroll_area_results.setWidget(self.scroll_area_widget)

        self.verticalLayout.addWidget(self.scroll_area_results)


        self.horizontalLayout.addWidget(self.frame_plot)

        self.frame_result = QFrame(SolarResults)
        self.frame_result.setObjectName(u"frame_result")
        self.frame_result.setMaximumSize(QSize(400, 16777215))
        self.frame_result.setFrameShape(QFrame.WinPanel)
        self.frame_result.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_3 = QVBoxLayout(self.frame_result)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.text_solar_results = QPlainTextEdit(self.frame_result)
        self.text_solar_results.setObjectName(u"text_solar_results")
        self.text_solar_results.setFrameShape(QFrame.NoFrame)
        self.text_solar_results.setFrameShadow(QFrame.Sunken)
        self.text_solar_results.setLineWidth(0)

        self.verticalLayout_3.addWidget(self.text_solar_results)


        self.horizontalLayout.addWidget(self.frame_result)


        self.retranslateUi(SolarResults)

        QMetaObject.connectSlotsByName(SolarResults)
    # setupUi

    def retranslateUi(self, SolarResults):
        SolarResults.setWindowTitle(QCoreApplication.translate("SolarResults", u"Form", None))
        self.label_solar_plot.setText("")
    # retranslateUi

