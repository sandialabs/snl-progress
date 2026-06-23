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
        LandingPage.resize(1183, 928)
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
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_progress_logo.sizePolicy().hasHeightForWidth())
        self.label_progress_logo.setSizePolicy(sizePolicy)
        self.label_progress_logo.setMaximumSize(QSize(1000, 280))
        self.label_progress_logo.setScaledContents(False)
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
        font.setPointSize(36)
        self.label_progress_desc.setFont(font)
        self.label_progress_desc.setAlignment(Qt.AlignCenter)
        self.label_progress_desc.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_progress_desc)

        self.frame_nav_btns = QFrame(self.frame_logo)
        self.frame_nav_btns.setObjectName(u"frame_nav_btns")
        self.frame_nav_btns.setFrameShape(QFrame.NoFrame)
        self.frame_nav_btns.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_nav_btns)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_getting_started = QPushButton(self.frame_nav_btns)
        self.btn_getting_started.setObjectName(u"btn_getting_started")

        self.horizontalLayout.addWidget(self.btn_getting_started)

        self.btn_documentation = QPushButton(self.frame_nav_btns)
        self.btn_documentation.setObjectName(u"btn_documentation")

        self.horizontalLayout.addWidget(self.btn_documentation)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.frame_nav_btns)


        self.verticalLayout.addWidget(self.frame_logo)

        self.frame_ackknowledgement = QFrame(LandingPage)
        self.frame_ackknowledgement.setObjectName(u"frame_ackknowledgement")
        self.frame_ackknowledgement.setFrameShape(QFrame.NoFrame)
        self.frame_ackknowledgement.setFrameShadow(QFrame.Plain)
        self.verticalLayout_3 = QVBoxLayout(self.frame_ackknowledgement)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_desc = QLabel(self.frame_ackknowledgement)
        self.label_desc.setObjectName(u"label_desc")
        font1 = QFont()
        font1.setPointSize(18)
        self.label_desc.setFont(font1)
        self.label_desc.setAlignment(Qt.AlignCenter)
        self.label_desc.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_desc)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.horizontalSpacer_7)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.horizontalSpacer_8)

        self.label_ack_doe = QLabel(self.frame_ackknowledgement)
        self.label_ack_doe.setObjectName(u"label_ack_doe")
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(True)
        self.label_ack_doe.setFont(font2)
        self.label_ack_doe.setAlignment(Qt.AlignCenter)
        self.label_ack_doe.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_ack_doe)


        self.verticalLayout.addWidget(self.frame_ackknowledgement)

        self.frame_footer = QFrame(LandingPage)
        self.frame_footer.setObjectName(u"frame_footer")
        self.frame_footer.setFrameShape(QFrame.NoFrame)
        self.frame_footer.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_footer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label_quest_logo = QLabel(self.frame_footer)
        self.label_quest_logo.setObjectName(u"label_quest_logo")
        self.label_quest_logo.setMinimumSize(QSize(80, 40))
        self.label_quest_logo.setMaximumSize(QSize(160, 70))
        self.label_quest_logo.setPixmap(QPixmap(u":/logos/Images/logos/Quest_Logo_RGB.png"))
        self.label_quest_logo.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_quest_logo)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label_doe_logo = QLabel(self.frame_footer)
        self.label_doe_logo.setObjectName(u"label_doe_logo")
        self.label_doe_logo.setMinimumSize(QSize(150, 150))
        self.label_doe_logo.setMaximumSize(QSize(150, 150))
        self.label_doe_logo.setPixmap(QPixmap(u":/logos/Images/logos/DOE_transparent.png"))
        self.label_doe_logo.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_doe_logo)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.label_snl_logo = QLabel(self.frame_footer)
        self.label_snl_logo.setObjectName(u"label_snl_logo")
        self.label_snl_logo.setMinimumSize(QSize(80, 40))
        self.label_snl_logo.setMaximumSize(QSize(180, 100))
        self.label_snl_logo.setPixmap(QPixmap(u":/logos/Images/logos/SNL_logo.png"))
        self.label_snl_logo.setScaledContents(True)
        self.label_snl_logo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_snl_logo)

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
        self.btn_getting_started.setText(QCoreApplication.translate("LandingPage", u"Get Started", None))
        self.btn_documentation.setText(QCoreApplication.translate("LandingPage", u"Documentation", None))
        self.label_desc.setText(QCoreApplication.translate("LandingPage", u"A Python-based open-source tool for assessing the resource adequacy of the evolving electric power grid integrated with energy storage systems.", None))
        self.label_ack_doe.setText(QCoreApplication.translate("LandingPage", u"Acknowledgement: This material is based upon work supported by the U.S. Department of Energy Office of Electricity, Energy Storage Division.", None))
        self.label_quest_logo.setText("")
        self.label_doe_logo.setText("")
        self.label_snl_logo.setText("")
    # retranslateUi

