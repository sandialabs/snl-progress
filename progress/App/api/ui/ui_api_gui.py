# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'api_guiWWpqPU.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_api_widget(object):
    def setupUi(self, api_widget):
        if not api_widget.objectName():
            api_widget.setObjectName(u"api_widget")
        api_widget.resize(1232, 794)
        self.verticalLayout = QVBoxLayout(api_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_13 = QWidget(api_widget)
        self.widget_13.setObjectName(u"widget_13")
        self.widget_13.setStyleSheet(u"")
        self.verticalLayout_16 = QVBoxLayout(self.widget_13)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.widget_13)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setStyleSheet(u"")
        self.verticalLayout_17 = QVBoxLayout(self.widget_3)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_16 = QFrame(self.widget_3)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setStyleSheet(u"")
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(327, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.frame_15 = QFrame(self.frame_16)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setStyleSheet(u"")
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_15)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.frame_15)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_10)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_8)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_17 = QFrame(self.frame_8)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setStyleSheet(u"")
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
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.pushButton_help_API = QPushButton(self.frame_21)
        self.pushButton_help_API.setObjectName(u"pushButton_help_API")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_help_API.sizePolicy().hasHeightForWidth())
        self.pushButton_help_API.setSizePolicy(sizePolicy)
        self.pushButton_help_API.setMinimumSize(QSize(23, 23))
        font = QFont()
        font.setPointSize(12)
        self.pushButton_help_API.setFont(font)
        self.pushButton_help_API.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_help_API.setStyleSheet(u"")
        self.pushButton_help_API.setFlat(True)

        self.gridLayout_6.addWidget(self.pushButton_help_API, 0, 2, 1, 1)

        self.lineEdit_api = QLineEdit(self.frame_21)
        self.lineEdit_api.setObjectName(u"lineEdit_api")
        self.lineEdit_api.setMinimumSize(QSize(0, 30))
        self.lineEdit_api.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.lineEdit_api, 1, 0, 1, 2)

        self.horizontalSpacer_2 = QSpacerItem(373, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 1, 1, 1)

        self.label_21 = QLabel(self.frame_21)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_6.addWidget(self.label_21, 0, 0, 1, 1)


        self.verticalLayout_15.addWidget(self.frame_21)

        self.frame_18 = QFrame(self.frame_17)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setStyleSheet(u"")
        self.frame_18.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_18)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_22 = QLabel(self.frame_18)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.label_22, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(388, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)

        self.pushButton_help_API_2 = QPushButton(self.frame_18)
        self.pushButton_help_API_2.setObjectName(u"pushButton_help_API_2")
        sizePolicy.setHeightForWidth(self.pushButton_help_API_2.sizePolicy().hasHeightForWidth())
        self.pushButton_help_API_2.setSizePolicy(sizePolicy)
        self.pushButton_help_API_2.setMinimumSize(QSize(23, 23))
        self.pushButton_help_API_2.setFont(font)
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
        self.frame_19.setStyleSheet(u"")
        self.frame_19.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_41 = QVBoxLayout(self.frame_19)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.verticalLayout_41.setContentsMargins(0, 0, 0, 0)
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
        self.verticalLayout_42.setContentsMargins(0, 0, 0, 0)
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
        self.frame_22.setStyleSheet(u"")
        self.frame_22.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pushButton_save_solarinput = QPushButton(self.frame_22)
        self.pushButton_save_solarinput.setObjectName(u"pushButton_save_solarinput")
        self.pushButton_save_solarinput.setMinimumSize(QSize(87, 23))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(18)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_save_solarinput.setFont(font1)
        self.pushButton_save_solarinput.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.pushButton_save_solarinput)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.pushButton_skip_API = QPushButton(self.frame_22)
        self.pushButton_skip_API.setObjectName(u"pushButton_skip_API")
        self.pushButton_skip_API.setMinimumSize(QSize(40, 23))
        self.pushButton_skip_API.setFont(font1)
        self.pushButton_skip_API.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.pushButton_skip_API)

        self.pushButton_help_API_3 = QPushButton(self.frame_22)
        self.pushButton_help_API_3.setObjectName(u"pushButton_help_API_3")
        self.pushButton_help_API_3.setMinimumSize(QSize(23, 23))
        self.pushButton_help_API_3.setFont(font)
        self.pushButton_help_API_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_help_API_3.setStyleSheet(u"")
        self.pushButton_help_API_3.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_help_API_3)


        self.verticalLayout_14.addWidget(self.frame_22)

        self.verticalLayout_14.setStretch(0, 1)

        self.horizontalLayout_3.addWidget(self.frame_15)

        self.horizontalSpacer_3 = QSpacerItem(720, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(2, 1)

        self.verticalLayout_17.addWidget(self.frame_16)

        self.widget_16 = QWidget(self.widget_3)
        self.widget_16.setObjectName(u"widget_16")
        self.widget_16.setStyleSheet(u"")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_16)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.pushButton_DI_previous_4 = QPushButton(self.widget_16)
        self.pushButton_DI_previous_4.setObjectName(u"pushButton_DI_previous_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_DI_previous_4.sizePolicy().hasHeightForWidth())
        self.pushButton_DI_previous_4.setSizePolicy(sizePolicy1)
        self.pushButton_DI_previous_4.setMinimumSize(QSize(69, 25))
        self.pushButton_DI_previous_4.setFont(font1)
        self.pushButton_DI_previous_4.setStyleSheet(u"")
        self.pushButton_DI_previous_4.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pushButton_DI_previous_4)

        self.horizontalSpacer_14 = QSpacerItem(1023, 45, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_14)

        self.pushButton_DI_next_4 = QPushButton(self.widget_16)
        self.pushButton_DI_next_4.setObjectName(u"pushButton_DI_next_4")
        self.pushButton_DI_next_4.setMinimumSize(QSize(52, 25))
        self.pushButton_DI_next_4.setFont(font1)
        self.pushButton_DI_next_4.setStyleSheet(u"")
        self.pushButton_DI_next_4.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pushButton_DI_next_4)


        self.verticalLayout_17.addWidget(self.widget_16)


        self.verticalLayout_16.addWidget(self.widget_3)


        self.verticalLayout.addWidget(self.widget_13)


        self.retranslateUi(api_widget)

        QMetaObject.connectSlotsByName(api_widget)
    # setupUi

    def retranslateUi(self, api_widget):
        api_widget.setWindowTitle(QCoreApplication.translate("api_widget", u"Form", None))
        self.pushButton_help_API.setText(QCoreApplication.translate("api_widget", u"?", None))
        self.lineEdit_api.setText("")
        self.label_21.setText(QCoreApplication.translate("api_widget", u"API Key:", None))
        self.label_22.setText(QCoreApplication.translate("api_widget", u"Name:", None))
        self.pushButton_help_API_2.setText(QCoreApplication.translate("api_widget", u"?", None))
        self.lineEdit_name.setText("")
        self.label_23.setText(QCoreApplication.translate("api_widget", u"Email ID:", None))
        self.lineEdit_email.setText("")
        self.label_24.setText(QCoreApplication.translate("api_widget", u"Affiliation:", None))
        self.lineEdit_aff.setText("")
        self.pushButton_save_solarinput.setText(QCoreApplication.translate("api_widget", u"Save Input", None))
        self.pushButton_skip_API.setText(QCoreApplication.translate("api_widget", u"Skip", None))
        self.pushButton_help_API_3.setText(QCoreApplication.translate("api_widget", u"?", None))
        self.pushButton_DI_previous_4.setText(QCoreApplication.translate("api_widget", u"Previous", None))
        self.pushButton_DI_next_4.setText(QCoreApplication.translate("api_widget", u"Next", None))
    # retranslateUi

