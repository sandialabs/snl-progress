# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solar_guidpzHON.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTextBrowser,
    QVBoxLayout, QWidget)
import progress.resources_rc

class Ui_solar_widget(object):
    def setupUi(self, solar_widget):
        if not solar_widget.objectName():
            solar_widget.setObjectName(u"solar_widget")
        solar_widget.resize(1248, 681)
        self.verticalLayout_2 = QVBoxLayout(solar_widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.stackedWidget_2 = QStackedWidget(solar_widget)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget_2.sizePolicy().hasHeightForWidth())
        self.stackedWidget_2.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        self.stackedWidget_2.setFont(font)
        self.stackedWidget_2.setStyleSheet(u"")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        sizePolicy.setHeightForWidth(self.page_4.sizePolicy().hasHeightForWidth())
        self.page_4.setSizePolicy(sizePolicy)
        self.page_4.setStyleSheet(u"")
        self.gridLayout_5 = QGridLayout(self.page_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.page_4)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setStyleSheet(u"")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(6)
        self.gridLayout_4.setContentsMargins(0, 9, 0, 0)
        self.widget_6 = QWidget(self.frame_4)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.widget_6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_4 = QTextBrowser(self.widget_6)
        self.textBrowser_4.setObjectName(u"textBrowser_4")
        self.textBrowser_4.setStyleSheet(u"")
        self.textBrowser_4.setFrameShape(QFrame.Shape.NoFrame)

        self.gridLayout.addWidget(self.textBrowser_4, 0, 1, 2, 1)

        self.pushButton_solar_dl = QPushButton(self.widget_6)
        self.pushButton_solar_dl.setObjectName(u"pushButton_solar_dl")
        self.pushButton_solar_dl.setEnabled(True)
        self.pushButton_solar_dl.setMinimumSize(QSize(143, 0))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(18)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_solar_dl.setFont(font1)
        self.pushButton_solar_dl.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_solar_dl.setStyleSheet(u"")

        self.gridLayout.addWidget(self.pushButton_solar_dl, 2, 0, 1, 1)

        self.widget_4 = QWidget(self.widget_6)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy1)
        self.widget_4.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.widget_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.solar_frame = QFrame(self.widget_4)
        self.solar_frame.setObjectName(u"solar_frame")
        self.solar_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.solar_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.solar_frame)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.solar_frame)
        self.label_20.setObjectName(u"label_20")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy2)
        self.label_20.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.label_20)

        self.comboBox_2 = QComboBox(self.solar_frame)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy3)
        self.comboBox_2.setMinimumSize(QSize(0, 30))
        font2 = QFont()
        font2.setPointSize(11)
        self.comboBox_2.setFont(font2)
        self.comboBox_2.setStyleSheet(u"")
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setMaxVisibleItems(10)

        self.verticalLayout_3.addWidget(self.comboBox_2)

        self.pushButton_solar_upload = QPushButton(self.solar_frame)
        self.pushButton_solar_upload.setObjectName(u"pushButton_solar_upload")
        self.pushButton_solar_upload.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.pushButton_solar_upload)


        self.verticalLayout.addWidget(self.solar_frame)


        self.gridLayout.addWidget(self.widget_4, 0, 0, 1, 1)

        self.widget_5 = QWidget(self.widget_6)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setEnabled(True)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setStyleSheet(u"")
        self.verticalLayout_9 = QVBoxLayout(self.widget_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.solar_frame_2 = QFrame(self.widget_5)
        self.solar_frame_2.setObjectName(u"solar_frame_2")
        self.solar_frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.solar_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.solar_frame_2)
        self.verticalLayout_4.setSpacing(15)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.solar_frame_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)

        self.lineEdit_starty = QLineEdit(self.solar_frame_2)
        self.lineEdit_starty.setObjectName(u"lineEdit_starty")
        self.lineEdit_starty.setEnabled(True)
        self.lineEdit_starty.setMinimumSize(QSize(0, 30))

        self.verticalLayout_4.addWidget(self.lineEdit_starty)


        self.verticalLayout_9.addWidget(self.solar_frame_2)

        self.solar_frame_3 = QFrame(self.widget_5)
        self.solar_frame_3.setObjectName(u"solar_frame_3")
        self.solar_frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.solar_frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.solar_frame_3)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.solar_frame_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setEnabled(True)

        self.verticalLayout_5.addWidget(self.label_26)

        self.lineEdit_endy = QLineEdit(self.solar_frame_3)
        self.lineEdit_endy.setObjectName(u"lineEdit_endy")
        self.lineEdit_endy.setMinimumSize(QSize(0, 30))

        self.verticalLayout_5.addWidget(self.lineEdit_endy)


        self.verticalLayout_9.addWidget(self.solar_frame_3)


        self.gridLayout.addWidget(self.widget_5, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.widget_6, 0, 0, 1, 1)

        self.widget_10 = QWidget(self.frame_4)
        self.widget_10.setObjectName(u"widget_10")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy4)
        self.widget_10.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.widget_10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_DI_previous_2 = QPushButton(self.widget_10)
        self.pushButton_DI_previous_2.setObjectName(u"pushButton_DI_previous_2")
        self.pushButton_DI_previous_2.setMinimumSize(QSize(55, 25))
        self.pushButton_DI_previous_2.setSizeIncrement(QSize(0, 0))
        self.pushButton_DI_previous_2.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_DI_previous_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButton_DI_next_2 = QPushButton(self.widget_10)
        self.pushButton_DI_next_2.setObjectName(u"pushButton_DI_next_2")
        self.pushButton_DI_next_2.setEnabled(True)
        self.pushButton_DI_next_2.setMinimumSize(QSize(45, 25))
        self.pushButton_DI_next_2.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_DI_next_2)


        self.gridLayout_4.addWidget(self.widget_10, 1, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 0, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5.setStyleSheet(u"")
        self.verticalLayout_23 = QVBoxLayout(self.page_5)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.frame_32 = QFrame(self.page_5)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setStyleSheet(u"")
        self.frame_32.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_27.setSpacing(6)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.frame_33 = QFrame(self.frame_32)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setStyleSheet(u"")
        self.frame_33.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_22 = QVBoxLayout(self.frame_33)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.frame_33)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"")
        self.verticalLayout_24 = QVBoxLayout(self.widget)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.frame_28 = QFrame(self.widget)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setStyleSheet(u"")
        self.frame_28.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_20 = QVBoxLayout(self.frame_28)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.frame_14 = QFrame(self.frame_28)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setStyleSheet(u"")
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_7 = QVBoxLayout(self.frame_14)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.solar2_frame = QFrame(self.frame_14)
        self.solar2_frame.setObjectName(u"solar2_frame")
        self.solar2_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.solar2_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.solar2_frame)
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.solar2_frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_help_solar = QPushButton(self.solar2_frame)
        self.pushButton_help_solar.setObjectName(u"pushButton_help_solar")
        self.pushButton_help_solar.setMinimumSize(QSize(25, 23))
        font3 = QFont()
        font3.setPointSize(12)
        self.pushButton_help_solar.setFont(font3)
        self.pushButton_help_solar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_help_solar.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/Images/icons/ainfo_24dp_5F6368_FILL0_wght200_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_help_solar.setIcon(icon)
        self.pushButton_help_solar.setIconSize(QSize(32, 32))
        self.pushButton_help_solar.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_help_solar)


        self.verticalLayout_7.addWidget(self.solar2_frame)

        self.solar2_frame_2 = QFrame(self.frame_14)
        self.solar2_frame_2.setObjectName(u"solar2_frame_2")
        self.solar2_frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.solar2_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.solar2_frame_2)
        self.verticalLayout_6.setSpacing(15)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.solar2_frame_2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_6.addWidget(self.label_5)

        self.lineEdit = QLineEdit(self.solar2_frame_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setStyleSheet(u"")

        self.verticalLayout_6.addWidget(self.lineEdit)


        self.verticalLayout_7.addWidget(self.solar2_frame_2)


        self.verticalLayout_20.addWidget(self.frame_14)

        self.solar2_frame_27 = QFrame(self.frame_28)
        self.solar2_frame_27.setObjectName(u"solar2_frame_27")
        self.solar2_frame_27.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_22 = QHBoxLayout(self.solar2_frame_27)
        self.horizontalLayout_22.setSpacing(15)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.solar2_frame_27)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(135, 0))
        self.pushButton_2.setSizeIncrement(QSize(0, 0))
        self.pushButton_2.setFont(font1)
        self.pushButton_2.setStyleSheet(u"")

        self.horizontalLayout_22.addWidget(self.pushButton_2)

        self.pushButton_api_8 = QPushButton(self.solar2_frame_27)
        self.pushButton_api_8.setObjectName(u"pushButton_api_8")
        self.pushButton_api_8.setMinimumSize(QSize(25, 23))
        self.pushButton_api_8.setFont(font3)
        self.pushButton_api_8.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_api_8.setStyleSheet(u"")
        self.pushButton_api_8.setIcon(icon)
        self.pushButton_api_8.setIconSize(QSize(32, 32))
        self.pushButton_api_8.setFlat(True)

        self.horizontalLayout_22.addWidget(self.pushButton_api_8)


        self.verticalLayout_20.addWidget(self.solar2_frame_27)


        self.verticalLayout_24.addWidget(self.frame_28)


        self.verticalLayout_22.addWidget(self.widget)

        self.widget_2 = QWidget(self.frame_33)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"")
        self.verticalLayout_21 = QVBoxLayout(self.widget_2)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.frame_30 = QFrame(self.widget_2)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setStyleSheet(u"")
        self.frame_30.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_43 = QVBoxLayout(self.frame_30)
        self.verticalLayout_43.setSpacing(0)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.solar2_frame_54 = QFrame(self.frame_30)
        self.solar2_frame_54.setObjectName(u"solar2_frame_54")
        self.solar2_frame_54.setStyleSheet(u"")
        self.solar2_frame_54.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_38 = QVBoxLayout(self.solar2_frame_54)
        self.verticalLayout_38.setSpacing(15)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.solar2_frame_54)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_38.addWidget(self.label_6)

        self.lineEdit_2 = QLineEdit(self.solar2_frame_54)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(0, 30))
        self.lineEdit_2.setStyleSheet(u"")

        self.verticalLayout_38.addWidget(self.lineEdit_2)


        self.verticalLayout_43.addWidget(self.solar2_frame_54)


        self.verticalLayout_21.addWidget(self.frame_30)

        self.frame_31 = QFrame(self.widget_2)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setStyleSheet(u"")
        self.frame_31.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 25)
        self.pushButton_3 = QPushButton(self.frame_31)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(135, 0))
        self.pushButton_3.setFont(font1)
        self.pushButton_3.setStyleSheet(u"")

        self.horizontalLayout_25.addWidget(self.pushButton_3)


        self.verticalLayout_21.addWidget(self.frame_31)


        self.verticalLayout_22.addWidget(self.widget_2)


        self.horizontalLayout_27.addWidget(self.frame_33)

        self.frame_29 = QFrame(self.frame_32)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setStyleSheet(u"")
        self.frame_29.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_23.setSpacing(6)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_6 = QTextBrowser(self.frame_29)
        self.textBrowser_6.setObjectName(u"textBrowser_6")
        self.textBrowser_6.setStyleSheet(u"")

        self.horizontalLayout_23.addWidget(self.textBrowser_6)

        self.textBrowser_5 = QTextBrowser(self.frame_29)
        self.textBrowser_5.setObjectName(u"textBrowser_5")
        self.textBrowser_5.setStyleSheet(u"")
        self.textBrowser_5.setFrameShape(QFrame.Shape.NoFrame)

        self.horizontalLayout_23.addWidget(self.textBrowser_5)

        self.horizontalLayout_23.setStretch(0, 2)
        self.horizontalLayout_23.setStretch(1, 1)

        self.horizontalLayout_27.addWidget(self.frame_29)

        self.horizontalLayout_27.setStretch(1, 1)

        self.verticalLayout_23.addWidget(self.frame_32)

        self.widget_17 = QWidget(self.page_5)
        self.widget_17.setObjectName(u"widget_17")
        self.widget_17.setStyleSheet(u"")
        self.horizontalLayout_26 = QHBoxLayout(self.widget_17)
        self.horizontalLayout_26.setSpacing(0)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.pushButton_DI_previous_5 = QPushButton(self.widget_17)
        self.pushButton_DI_previous_5.setObjectName(u"pushButton_DI_previous_5")
        sizePolicy3.setHeightForWidth(self.pushButton_DI_previous_5.sizePolicy().hasHeightForWidth())
        self.pushButton_DI_previous_5.setSizePolicy(sizePolicy3)
        self.pushButton_DI_previous_5.setMinimumSize(QSize(55, 25))
        self.pushButton_DI_previous_5.setFont(font1)
        self.pushButton_DI_previous_5.setStyleSheet(u"")

        self.horizontalLayout_26.addWidget(self.pushButton_DI_previous_5)

        self.horizontalSpacer_15 = QSpacerItem(1023, 45, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_15)

        self.pushButton_DI_next_5 = QPushButton(self.widget_17)
        self.pushButton_DI_next_5.setObjectName(u"pushButton_DI_next_5")
        self.pushButton_DI_next_5.setMinimumSize(QSize(45, 25))
        self.pushButton_DI_next_5.setFont(font1)
        self.pushButton_DI_next_5.setStyleSheet(u"")

        self.horizontalLayout_26.addWidget(self.pushButton_DI_next_5)


        self.verticalLayout_23.addWidget(self.widget_17)

        self.verticalLayout_23.setStretch(0, 1)
        self.stackedWidget_2.addWidget(self.page_5)

        self.verticalLayout_2.addWidget(self.stackedWidget_2)


        self.retranslateUi(solar_widget)

        self.stackedWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(solar_widget)
    # setupUi

    def retranslateUi(self, solar_widget):
        solar_widget.setWindowTitle(QCoreApplication.translate("solar_widget", u"Form", None))
        self.pushButton_solar_dl.setText(QCoreApplication.translate("solar_widget", u"Download Solar Data", None))
        self.label_20.setText(QCoreApplication.translate("solar_widget", u"Data input:", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("solar_widget", u"--Select Option--", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("solar_widget", u"Download Solar Data from NSRDB", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("solar_widget", u"Use Own Data", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("solar_widget", u"No Solar", None))

        self.pushButton_solar_upload.setText(QCoreApplication.translate("solar_widget", u"Upload Data", None))
        self.label_3.setText(QCoreApplication.translate("solar_widget", u"Start Year:", None))
        self.lineEdit_starty.setText("")
        self.label_26.setText(QCoreApplication.translate("solar_widget", u"End Year:", None))
        self.lineEdit_endy.setText("")
        self.pushButton_DI_previous_2.setText(QCoreApplication.translate("solar_widget", u"Previous", None))
        self.pushButton_DI_next_2.setText(QCoreApplication.translate("solar_widget", u"Next", None))
        self.pushButton.setText(QCoreApplication.translate("solar_widget", u"Skip", None))
        self.pushButton_help_solar.setText("")
        self.label_5.setText(QCoreApplication.translate("solar_widget", u"No. of Clusters to Evaluate:", None))
        self.pushButton_2.setText(QCoreApplication.translate("solar_widget", u"Evaluate Clusters", None))
        self.pushButton_api_8.setText("")
        self.label_6.setText(QCoreApplication.translate("solar_widget", u"Final No. of clusters:", None))
        self.pushButton_3.setText(QCoreApplication.translate("solar_widget", u"Generate Clusters", None))
        self.pushButton_DI_previous_5.setText(QCoreApplication.translate("solar_widget", u"Previous", None))
        self.pushButton_DI_next_5.setText(QCoreApplication.translate("solar_widget", u"Next", None))
    # retranslateUi

