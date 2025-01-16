# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'landingoVcNHn.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import progress.resources_rc


class Ui_land(object):
    def setupUi(self, land):
        if not land.objectName():
            land.setObjectName(u"land")
        land.resize(1178, 713)
        self.verticalLayout = QVBoxLayout(land)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label = QLabel(land)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 48pt \"Arial\";\n"
"color: white;")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_2 = QLabel(land)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: 16pt \"Arial\";\n"
"color: white;")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.get_started_button = QPushButton(land)
        self.get_started_button.setObjectName(u"get_started_button")
        self.get_started_button.setStyleSheet(u"\n"
"            QPushButton {\n"
"                color: white;\n"
"				font: 16pt \"Arial\";\n"
"                background-color: transparent;\n"
"                border: 2px solid white;\n"
"                padding: 10px 20px;\n"
"                border-radius: 5px;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 0.1);\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: rgba(255, 255, 255, 0.2);\n"
"            }")

        self.verticalLayout.addWidget(self.get_started_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_4 = QLabel(land)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(100, 60))
        self.label_4.setPixmap(QPixmap(u":/logos/Images/logos/Quest_Logo_RGB.png"))
        self.label_4.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_4, 0, Qt.AlignmentFlag.AlignRight)

        self.label_5 = QLabel(land)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(120, 60))
        self.label_5.setPixmap(QPixmap(u":/logos/Images/logos/Sandia_National_Laboratories_logo.svg"))
        self.label_5.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_5)

        self.label_3 = QLabel(land)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(60, 60))
        self.label_3.setPixmap(QPixmap(u":/logos/Images/logos/DOE_transparent.png"))
        self.label_3.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label_6 = QLabel(land)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"font: 12pt \"Arial\";\n"
"color: white;")
        self.label_6.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_6)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(land)

        QMetaObject.connectSlotsByName(land)
    # setupUi

    def retranslateUi(self, land):
        land.setWindowTitle(QCoreApplication.translate("land", u"Form", None))
        self.label.setText(QCoreApplication.translate("land", u"<html><head/><body><p align=\"center\">Probabilistic Grid Reliability Analysis with Energy Storage Systems</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("land", u"<html><head/><body><p align=\"center\">A Python-based open-source tool for assessing the resource adequacy of the evolving electric power grid integrated with energy storage systems.</p></body></html>", None))
        self.get_started_button.setText(QCoreApplication.translate("land", u"Get Started", None))
        self.label_4.setText("")
        self.label_5.setText("")
        self.label_3.setText("")
        self.label_6.setText(QCoreApplication.translate("land", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Acknowledgement</span><br/>This material is based upon work supported by the U.S. Department of Energy, Office of Electricity (OE), Energy Storage Division.</p></body></html>", None))
    # retranslateUi

