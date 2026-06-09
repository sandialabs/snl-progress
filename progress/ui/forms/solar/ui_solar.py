# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solar_new.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_SolarPage(object):
    def setupUi(self, SolarPage):
        if not SolarPage.objectName():
            SolarPage.setObjectName(u"SolarPage")
        SolarPage.resize(1231, 928)
        self.verticalLayout = QVBoxLayout(SolarPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.solarStackedWidget = QStackedWidget(SolarPage)
        self.solarStackedWidget.setObjectName(u"solarStackedWidget")
        self.page_data = QWidget()
        self.page_data.setObjectName(u"page_data")
        self.verticalLayout_2 = QVBoxLayout(self.page_data)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_frame = QFrame(self.page_data)
        self.main_frame.setObjectName(u"main_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_frame.sizePolicy().hasHeightForWidth())
        self.main_frame.setSizePolicy(sizePolicy)
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.main_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.data_frame = QFrame(self.main_frame)
        self.data_frame.setObjectName(u"data_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.data_frame.sizePolicy().hasHeightForWidth())
        self.data_frame.setSizePolicy(sizePolicy1)
        self.data_frame.setFrameShape(QFrame.StyledPanel)
        self.data_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.data_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget_input = QWidget(self.data_frame)
        self.widget_input.setObjectName(u"widget_input")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_input.sizePolicy().hasHeightForWidth())
        self.widget_input.setSizePolicy(sizePolicy2)
        self.verticalLayout_5 = QVBoxLayout(self.widget_input)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_solar_input = QFrame(self.widget_input)
        self.frame_solar_input.setObjectName(u"frame_solar_input")
        self.frame_solar_input.setFrameShape(QFrame.StyledPanel)
        self.frame_solar_input.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_solar_input)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_data_input = QLabel(self.frame_solar_input)
        self.label_data_input.setObjectName(u"label_data_input")
        sizePolicy.setHeightForWidth(self.label_data_input.sizePolicy().hasHeightForWidth())
        self.label_data_input.setSizePolicy(sizePolicy)
        self.label_data_input.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout_6.addWidget(self.label_data_input)

        self.combo_data_source = QComboBox(self.frame_solar_input)
        self.combo_data_source.setObjectName(u"combo_data_source")

        self.verticalLayout_6.addWidget(self.combo_data_source)

        self.btn_upload_data = QPushButton(self.frame_solar_input)
        self.btn_upload_data.setObjectName(u"btn_upload_data")

        self.verticalLayout_6.addWidget(self.btn_upload_data)


        self.verticalLayout_5.addWidget(self.frame_solar_input)

        self.frame_start_date = QFrame(self.widget_input)
        self.frame_start_date.setObjectName(u"frame_start_date")
        self.frame_start_date.setFrameShape(QFrame.StyledPanel)
        self.frame_start_date.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_start_date)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_start_year = QLabel(self.frame_start_date)
        self.label_start_year.setObjectName(u"label_start_year")

        self.horizontalLayout_2.addWidget(self.label_start_year)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.line_edit_start = QLineEdit(self.frame_start_date)
        self.line_edit_start.setObjectName(u"line_edit_start")

        self.horizontalLayout_2.addWidget(self.line_edit_start)


        self.verticalLayout_5.addWidget(self.frame_start_date)

        self.frame_end_date = QFrame(self.widget_input)
        self.frame_end_date.setObjectName(u"frame_end_date")
        self.frame_end_date.setFrameShape(QFrame.StyledPanel)
        self.frame_end_date.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_end_date)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_end_year = QLabel(self.frame_end_date)
        self.label_end_year.setObjectName(u"label_end_year")

        self.horizontalLayout_3.addWidget(self.label_end_year)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.line_edit_end = QLineEdit(self.frame_end_date)
        self.line_edit_end.setObjectName(u"line_edit_end")

        self.horizontalLayout_3.addWidget(self.line_edit_end)


        self.verticalLayout_5.addWidget(self.frame_end_date)


        self.gridLayout.addWidget(self.widget_input, 0, 0, 1, 1)

        self.btn_download_solar = QPushButton(self.data_frame)
        self.btn_download_solar.setObjectName(u"btn_download_solar")

        self.gridLayout.addWidget(self.btn_download_solar, 1, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.data_frame)

        self.nav_bottom = QWidget(self.main_frame)
        self.nav_bottom.setObjectName(u"nav_bottom")
        self.nav_bottom.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout = QHBoxLayout(self.nav_bottom)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bottom_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.bottom_spacer)

        self.btn_prev_page = QPushButton(self.nav_bottom)
        self.btn_prev_page.setObjectName(u"btn_prev_page")

        self.horizontalLayout.addWidget(self.btn_prev_page)

        self.btn_next_page = QPushButton(self.nav_bottom)
        self.btn_next_page.setObjectName(u"btn_next_page")

        self.horizontalLayout.addWidget(self.btn_next_page)


        self.verticalLayout_3.addWidget(self.nav_bottom)


        self.verticalLayout_2.addWidget(self.main_frame)

        self.solarStackedWidget.addWidget(self.page_data)
        self.page_cluster = QWidget()
        self.page_cluster.setObjectName(u"page_cluster")
        self.gridLayout_2 = QGridLayout(self.page_cluster)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame = QFrame(self.page_cluster)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_7 = QVBoxLayout(self.widget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_7.addWidget(self.textBrowser)


        self.gridLayout_3.addWidget(self.widget, 0, 2, 1, 1)

        self.widget_2 = QWidget(self.frame)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_8 = QVBoxLayout(self.widget_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.textBrowser_2 = QTextBrowser(self.widget_2)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.verticalLayout_8.addWidget(self.textBrowser_2)


        self.gridLayout_3.addWidget(self.widget_2, 0, 1, 1, 1)

        self.widget_3 = QWidget(self.frame)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_9 = QVBoxLayout(self.widget_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_2 = QFrame(self.widget_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.radioButton = QRadioButton(self.frame_2)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_10.addWidget(self.radioButton)


        self.verticalLayout_9.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.widget_3)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.radioButton_2 = QRadioButton(self.frame_3)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_11.addWidget(self.radioButton_2)


        self.verticalLayout_9.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.widget_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_4)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_12.addWidget(self.pushButton)


        self.verticalLayout_9.addWidget(self.frame_4)


        self.gridLayout_3.addWidget(self.widget_3, 0, 0, 1, 1)

        self.nav_bottom_2 = QWidget(self.frame)
        self.nav_bottom_2.setObjectName(u"nav_bottom_2")
        self.nav_bottom_2.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_4 = QHBoxLayout(self.nav_bottom_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.bottom_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.bottom_spacer_2)

        self.btn_prev_page_2 = QPushButton(self.nav_bottom_2)
        self.btn_prev_page_2.setObjectName(u"btn_prev_page_2")

        self.horizontalLayout_4.addWidget(self.btn_prev_page_2)

        self.btn_next_page_2 = QPushButton(self.nav_bottom_2)
        self.btn_next_page_2.setObjectName(u"btn_next_page_2")

        self.horizontalLayout_4.addWidget(self.btn_next_page_2)


        self.gridLayout_3.addWidget(self.nav_bottom_2, 1, 0, 1, 3)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.solarStackedWidget.addWidget(self.page_cluster)

        self.verticalLayout.addWidget(self.solarStackedWidget)


        self.retranslateUi(SolarPage)

        self.solarStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SolarPage)
    # setupUi

    def retranslateUi(self, SolarPage):
        SolarPage.setWindowTitle(QCoreApplication.translate("SolarPage", u"Form", None))
        self.label_data_input.setText(QCoreApplication.translate("SolarPage", u"Data Input:", None))
        self.btn_upload_data.setText(QCoreApplication.translate("SolarPage", u"PushButton", None))
        self.label_start_year.setText(QCoreApplication.translate("SolarPage", u"Start Year:", None))
        self.label_end_year.setText(QCoreApplication.translate("SolarPage", u"End Year:", None))
        self.btn_download_solar.setText(QCoreApplication.translate("SolarPage", u"Download Solar Data", None))
        self.btn_prev_page.setText(QCoreApplication.translate("SolarPage", u"Prev", None))
        self.btn_next_page.setText(QCoreApplication.translate("SolarPage", u"Next", None))
        self.radioButton.setText(QCoreApplication.translate("SolarPage", u"RadioButton", None))
        self.radioButton_2.setText(QCoreApplication.translate("SolarPage", u"RadioButton", None))
        self.pushButton.setText(QCoreApplication.translate("SolarPage", u"PushButton", None))
        self.btn_prev_page_2.setText(QCoreApplication.translate("SolarPage", u"Prev", None))
        self.btn_next_page_2.setText(QCoreApplication.translate("SolarPage", u"Next", None))
    # retranslateUi

