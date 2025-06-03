# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'landingdOCGlR.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import progress.resources_rc


class Ui_land(object):
    def setupUi(self, land):
        if not land.objectName():
            land.setObjectName(u"land")
        land.resize(1172, 700)
        self.verticalLayout = QVBoxLayout(land)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label = QLabel(land)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_2 = QLabel(land)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.get_started_button = QPushButton(land)
        self.get_started_button.setObjectName(u"get_started_button")
        self.get_started_button.setStyleSheet(u"")
        self.get_started_button.setFlat(True)

        self.verticalLayout.addWidget(self.get_started_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(land)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background:transparent;\n"
"border: 0px;")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(100, 50))
        self.label_4.setPixmap(QPixmap(u":/logos/Images/logos/Quest_Logo_RGB.png"))
        self.label_4.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_4)


        self.horizontalLayout.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignRight)

        self.label_5 = QLabel(land)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(120, 50))
        self.label_5.setPixmap(QPixmap(u":/logos/Images/logos/Sandia_National_Laboratories_logo.svg"))
        self.label_5.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_5)

        self.label_3 = QLabel(land)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(60, 60))
        self.label_3.setPixmap(QPixmap(u":/logos/Images/logos/DOE_transparent.png"))
        self.label_3.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.frame_2 = QFrame(land)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background: transparent;")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(9, -1, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet(u"")
        self.label_6.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.frame_2)


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
        self.label_6.setText(QCoreApplication.translate("land", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">Acknowledgement: </span>This material is based upon work supported by the U.S. Department of Energy, Office of Electricity (OE), Energy Storage Division.</p></body></html>", None))
    # retranslateUi

