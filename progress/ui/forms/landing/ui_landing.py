# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'landing.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_LandingPage(object):
    def setupUi(self, LandingPage):
        if not LandingPage.objectName():
            LandingPage.setObjectName(u"LandingPage")
        LandingPage.resize(1163, 908)
        self.verticalLayout = QVBoxLayout(LandingPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_logo = QFrame(LandingPage)
        self.frame_logo.setObjectName(u"frame_logo")
        self.frame_logo.setFrameShape(QFrame.NoFrame)
        self.frame_logo.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.frame_logo)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.frame_logo)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_progress_logo = QLabel(self.frame_2)
        self.label_progress_logo.setObjectName(u"label_progress_logo")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_progress_logo.sizePolicy().hasHeightForWidth())
        self.label_progress_logo.setSizePolicy(sizePolicy)
        self.label_progress_logo.setMaximumSize(QSize(943, 239))
        self.label_progress_logo.setPixmap(QPixmap(u":/logos/Images/logos/progress_transparent_alt.png"))
        self.label_progress_logo.setScaledContents(True)
        self.label_progress_logo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_progress_logo)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.label_progress_desc = QLabel(self.frame_logo)
        self.label_progress_desc.setObjectName(u"label_progress_desc")
        palette = QPalette()
        brush = QBrush(QColor(45, 105, 46, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(127, 127, 127, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        self.label_progress_desc.setPalette(palette)
        font = QFont()
        font.setPointSize(40)
        self.label_progress_desc.setFont(font)
        self.label_progress_desc.setAlignment(Qt.AlignCenter)
        self.label_progress_desc.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_progress_desc)

        self.frame = QFrame(self.frame_logo)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.frame)


        self.verticalLayout.addWidget(self.frame_logo)

        self.frame_ackknowledgement = QFrame(LandingPage)
        self.frame_ackknowledgement.setObjectName(u"frame_ackknowledgement")
        self.frame_ackknowledgement.setFrameShape(QFrame.NoFrame)
        self.frame_ackknowledgement.setFrameShadow(QFrame.Plain)
        self.verticalLayout_3 = QVBoxLayout(self.frame_ackknowledgement)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.frame_ackknowledgement)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setPointSize(18)
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.horizontalSpacer_7)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.horizontalSpacer_8)

        self.label_4 = QLabel(self.frame_ackknowledgement)
        self.label_4.setObjectName(u"label_4")
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(True)
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_4)


        self.verticalLayout.addWidget(self.frame_ackknowledgement)

        self.frame_footer = QFrame(LandingPage)
        self.frame_footer.setObjectName(u"frame_footer")
        self.frame_footer.setFrameShape(QFrame.NoFrame)
        self.frame_footer.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_footer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label_5 = QLabel(self.frame_footer)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(80, 40))
        self.label_5.setMaximumSize(QSize(160, 70))
        self.label_5.setPixmap(QPixmap(u":/logos/Images/logos/Quest_Logo_RGB.png"))
        self.label_5.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_5)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label_6 = QLabel(self.frame_footer)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(150, 150))
        self.label_6.setMaximumSize(QSize(150, 150))
        self.label_6.setPixmap(QPixmap(u":/logos/Images/logos/DOE_transparent.png"))
        self.label_6.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.label_7 = QLabel(self.frame_footer)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(80, 40))
        self.label_7.setMaximumSize(QSize(180, 100))
        self.label_7.setPixmap(QPixmap(u":/logos/Images/logos/SNL_logo.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_7)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addWidget(self.frame_footer)


        self.retranslateUi(LandingPage)

        QMetaObject.connectSlotsByName(LandingPage)
    # setupUi

    def retranslateUi(self, LandingPage):
        LandingPage.setWindowTitle(QCoreApplication.translate("LandingPage", u"Form", None))
        self.label_progress_logo.setText("")
        self.label_progress_desc.setText(QCoreApplication.translate("LandingPage", u"Probabilistic Grid Reliability Analysis with Energy Storage Systems", None))
        self.pushButton.setText(QCoreApplication.translate("LandingPage", u"Get Started", None))
        self.pushButton_2.setText(QCoreApplication.translate("LandingPage", u"Documentation", None))
        self.label_3.setText(QCoreApplication.translate("LandingPage", u"A Python-based open-source tool for assessing the resource adequacy of the evolving electric power grid integrated with energy storage systems.", None))
        self.label_4.setText(QCoreApplication.translate("LandingPage", u"Acknowledgement: This material is based upon work supported by the U.S. Department of Energy Office of Electricity, Energy Storage Division.", None))
        self.label_5.setText("")
        self.label_6.setText("")
        self.label_7.setText("")
    # retranslateUi

