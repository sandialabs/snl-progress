# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'wind_guiMIxzwl.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTextBrowser, QVBoxLayout, QWidget)
import progress.resources_rc

class Ui_wind_widget(object):
    def setupUi(self, wind_widget):
        if not wind_widget.objectName():
            wind_widget.setObjectName(u"wind_widget")
        wind_widget.resize(1406, 876)
        self.verticalLayout_6 = QVBoxLayout(wind_widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(wind_widget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_55 = QFrame(self.frame_5)
        self.frame_55.setObjectName(u"frame_55")
        self.frame_55.setStyleSheet(u"")
        self.frame_55.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_55.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_55)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.widget_8 = QWidget(self.frame_55)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.widget_8.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.widget_8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.widget_8)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.wind_frame_2 = QFrame(self.frame)
        self.wind_frame_2.setObjectName(u"wind_frame_2")
        self.wind_frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.wind_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.wind_frame_2)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_27 = QLabel(self.wind_frame_2)
        self.label_27.setObjectName(u"label_27")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy1)
        self.label_27.setMinimumSize(QSize(200, 0))
        self.label_27.setMaximumSize(QSize(100, 100))
        self.label_27.setStyleSheet(u"")
        self.label_27.setWordWrap(False)

        self.verticalLayout_3.addWidget(self.label_27)

        self.comboBox_3 = QComboBox(self.wind_frame_2)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setMinimumSize(QSize(0, 30))
        font = QFont()
        font.setPointSize(11)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setStyleSheet(u"")
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setMaxVisibleItems(10)

        self.verticalLayout_3.addWidget(self.comboBox_3)

        self.pushButton_wind_upload = QPushButton(self.wind_frame_2)
        self.pushButton_wind_upload.setObjectName(u"pushButton_wind_upload")
        self.pushButton_wind_upload.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.pushButton_wind_upload)


        self.horizontalLayout.addWidget(self.wind_frame_2)


        self.verticalLayout_2.addWidget(self.frame)


        self.verticalLayout_7.addWidget(self.widget_8)

        self.wind_box = QFrame(self.frame_55)
        self.wind_box.setObjectName(u"wind_box")
        self.wind_box.setFrameShape(QFrame.Shape.NoFrame)
        self.wind_box.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.wind_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.wind_frame_3 = QFrame(self.wind_box)
        self.wind_frame_3.setObjectName(u"wind_frame_3")
        self.wind_frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.wind_frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.wind_frame_3)
        self.verticalLayout_4.setSpacing(15)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_31 = QLabel(self.wind_frame_3)
        self.label_31.setObjectName(u"label_31")

        self.verticalLayout_4.addWidget(self.label_31)

        self.lineEdit_22 = QLineEdit(self.wind_frame_3)
        self.lineEdit_22.setObjectName(u"lineEdit_22")
        self.lineEdit_22.setMinimumSize(QSize(0, 30))

        self.verticalLayout_4.addWidget(self.lineEdit_22)


        self.verticalLayout.addWidget(self.wind_frame_3)

        self.wind_frame_4 = QFrame(self.wind_box)
        self.wind_frame_4.setObjectName(u"wind_frame_4")
        self.wind_frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.wind_frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.wind_frame_4)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_32 = QLabel(self.wind_frame_4)
        self.label_32.setObjectName(u"label_32")

        self.verticalLayout_5.addWidget(self.label_32)

        self.lineEdit_23 = QLineEdit(self.wind_frame_4)
        self.lineEdit_23.setObjectName(u"lineEdit_23")
        self.lineEdit_23.setMinimumSize(QSize(0, 30))
        self.lineEdit_23.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.lineEdit_23)


        self.verticalLayout.addWidget(self.wind_frame_4)

        self.frame_3 = QFrame(self.wind_box)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.pushButton_4 = QPushButton(self.frame_3)
        self.pushButton_4.setObjectName(u"pushButton_4")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(18)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_4.setFont(font1)
        self.pushButton_4.setStyleSheet(u"")
        self.pushButton_4.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_4, 0, Qt.AlignmentFlag.AlignRight)

        self.pushButton_help_wind = QPushButton(self.frame_3)
        self.pushButton_help_wind.setObjectName(u"pushButton_help_wind")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_help_wind.sizePolicy().hasHeightForWidth())
        self.pushButton_help_wind.setSizePolicy(sizePolicy2)
        self.pushButton_help_wind.setMinimumSize(QSize(0, 0))
        font2 = QFont()
        font2.setPointSize(12)
        self.pushButton_help_wind.setFont(font2)
        self.pushButton_help_wind.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_help_wind.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/Images/icons/ainfo_24dp_5F6368_FILL0_wght200_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_help_wind.setIcon(icon)
        self.pushButton_help_wind.setIconSize(QSize(32, 32))
        self.pushButton_help_wind.setFlat(True)

        self.horizontalLayout_5.addWidget(self.pushButton_help_wind, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.frame_3)


        self.verticalLayout_7.addWidget(self.wind_box)

        self.frame_2 = QFrame(self.frame_55)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_7 = QPushButton(self.frame_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy3)
        self.pushButton_7.setFont(font1)
        self.pushButton_7.setStyleSheet(u"")
        self.pushButton_7.setFlat(True)

        self.horizontalLayout_3.addWidget(self.pushButton_7)

        self.horizontalSpacer_13 = QSpacerItem(356, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_13)


        self.verticalLayout_7.addWidget(self.frame_2)

        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 1)

        self.horizontalLayout_4.addWidget(self.frame_55)

        self.frame_4 = QFrame(self.frame_5)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_3 = QTextBrowser(self.frame_4)
        self.textBrowser_3.setObjectName(u"textBrowser_3")
        self.textBrowser_3.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.textBrowser_3)


        self.horizontalLayout_4.addWidget(self.frame_4)

        self.horizontalLayout_4.setStretch(0, 1)

        self.verticalLayout_6.addWidget(self.frame_5)

        self.widget_11 = QWidget(wind_widget)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setStyleSheet(u"")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_DI_previous_3 = QPushButton(self.widget_11)
        self.pushButton_DI_previous_3.setObjectName(u"pushButton_DI_previous_3")
        self.pushButton_DI_previous_3.setFont(font1)
        self.pushButton_DI_previous_3.setStyleSheet(u"")
        self.pushButton_DI_previous_3.setFlat(True)

        self.horizontalLayout_7.addWidget(self.pushButton_DI_previous_3)

        self.horizontalSpacer_11 = QSpacerItem(1023, 45, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)

        self.pushButton_DI_next_3 = QPushButton(self.widget_11)
        self.pushButton_DI_next_3.setObjectName(u"pushButton_DI_next_3")
        self.pushButton_DI_next_3.setFont(font1)
        self.pushButton_DI_next_3.setStyleSheet(u"")
        self.pushButton_DI_next_3.setFlat(True)

        self.horizontalLayout_7.addWidget(self.pushButton_DI_next_3)


        self.verticalLayout_6.addWidget(self.widget_11)


        self.retranslateUi(wind_widget)

        QMetaObject.connectSlotsByName(wind_widget)
    # setupUi

    def retranslateUi(self, wind_widget):
        wind_widget.setWindowTitle(QCoreApplication.translate("wind_widget", u"Form", None))
        self.label_27.setText(QCoreApplication.translate("wind_widget", u"Data input:         ", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("wind_widget", u"--Select Option--", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("wind_widget", u"Download Wind Data from WIND Toolkit", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("wind_widget", u"Use Own Data", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("wind_widget", u"No Wind", None))

        self.pushButton_wind_upload.setText(QCoreApplication.translate("wind_widget", u"Upload Data", None))
        self.label_31.setText(QCoreApplication.translate("wind_widget", u"Start Year:", None))
        self.label_32.setText(QCoreApplication.translate("wind_widget", u"End Year:", None))
        self.pushButton_4.setText(QCoreApplication.translate("wind_widget", u"Download Wind Speed Data", None))
        self.pushButton_help_wind.setText("")
        self.pushButton_7.setText(QCoreApplication.translate("wind_widget", u"Process Wind Speed Data", None))
        self.pushButton_DI_previous_3.setText(QCoreApplication.translate("wind_widget", u"Previous", None))
        self.pushButton_DI_next_3.setText(QCoreApplication.translate("wind_widget", u"Next", None))
    # retranslateUi

