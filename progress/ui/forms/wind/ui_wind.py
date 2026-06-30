# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'wind.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_WindPage(object):
    def setupUi(self, WindPage):
        if not WindPage.objectName():
            WindPage.setObjectName(u"WindPage")
        WindPage.resize(1163, 908)
        self.verticalLayout = QVBoxLayout(WindPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.windStackedWidget = QStackedWidget(WindPage)
        self.windStackedWidget.setObjectName(u"windStackedWidget")
        self.windStackedWidget.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.page_data = QWidget()
        self.page_data.setObjectName(u"page_data")
        self.verticalLayout_2 = QVBoxLayout(self.page_data)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_main = QFrame(self.page_data)
        self.frame_main.setObjectName(u"frame_main")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_main.sizePolicy().hasHeightForWidth())
        self.frame_main.setSizePolicy(sizePolicy)
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_main)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_data = QFrame(self.frame_main)
        self.frame_data.setObjectName(u"frame_data")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_data.sizePolicy().hasHeightForWidth())
        self.frame_data.setSizePolicy(sizePolicy1)
        self.frame_data.setFrameShape(QFrame.NoFrame)
        self.frame_data.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_data)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.groupBox_input = QGroupBox(self.frame_data)
        self.groupBox_input.setObjectName(u"groupBox_input")
        font = QFont()
        font.setPointSize(16)
        self.groupBox_input.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_input)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_source_hint = QLabel(self.groupBox_input)
        self.label_source_hint.setObjectName(u"label_source_hint")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_source_hint.sizePolicy().hasHeightForWidth())
        self.label_source_hint.setSizePolicy(sizePolicy2)

        self.verticalLayout_5.addWidget(self.label_source_hint)

        self.combo_data_source = QComboBox(self.groupBox_input)
        self.combo_data_source.addItem("")
        self.combo_data_source.addItem("")
        self.combo_data_source.addItem("")
        self.combo_data_source.addItem("")
        self.combo_data_source.setObjectName(u"combo_data_source")

        self.verticalLayout_5.addWidget(self.combo_data_source)

        self.line_separator_1 = QFrame(self.groupBox_input)
        self.line_separator_1.setObjectName(u"line_separator_1")
        self.line_separator_1.setFrameShape(QFrame.HLine)
        self.line_separator_1.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_separator_1)

        self.frame_date_range = QFrame(self.groupBox_input)
        self.frame_date_range.setObjectName(u"frame_date_range")
        self.frame_date_range.setFrameShape(QFrame.NoFrame)
        self.frame_date_range.setFrameShadow(QFrame.Plain)
        self.verticalLayout_7 = QVBoxLayout(self.frame_date_range)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frame_start_date = QFrame(self.frame_date_range)
        self.frame_start_date.setObjectName(u"frame_start_date")
        self.frame_start_date.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_start = QHBoxLayout(self.frame_start_date)
        self.horizontalLayout_start.setObjectName(u"horizontalLayout_start")
        self.label_start_year = QLabel(self.frame_start_date)
        self.label_start_year.setObjectName(u"label_start_year")
        self.label_start_year.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_start.addWidget(self.label_start_year)

        self.horizontalSpacer_start = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_start.addItem(self.horizontalSpacer_start)

        self.line_edit_start = QLineEdit(self.frame_start_date)
        self.line_edit_start.setObjectName(u"line_edit_start")

        self.horizontalLayout_start.addWidget(self.line_edit_start)

        self.btn_start_info = QPushButton(self.frame_start_date)
        self.btn_start_info.setObjectName(u"btn_start_info")
        icon = QIcon()
        icon.addFile(u":/icons/Images/icons/about.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_start_info.setIcon(icon)
        self.btn_start_info.setIconSize(QSize(40, 40))
        self.btn_start_info.setFlat(True)

        self.horizontalLayout_start.addWidget(self.btn_start_info)


        self.verticalLayout_7.addWidget(self.frame_start_date)

        self.frame_end_date = QFrame(self.frame_date_range)
        self.frame_end_date.setObjectName(u"frame_end_date")
        self.frame_end_date.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_end = QHBoxLayout(self.frame_end_date)
        self.horizontalLayout_end.setObjectName(u"horizontalLayout_end")
        self.label_end_year = QLabel(self.frame_end_date)
        self.label_end_year.setObjectName(u"label_end_year")
        self.label_end_year.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_end.addWidget(self.label_end_year)

        self.horizontalSpacer_end = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_end.addItem(self.horizontalSpacer_end)

        self.line_edit_end = QLineEdit(self.frame_end_date)
        self.line_edit_end.setObjectName(u"line_edit_end")

        self.horizontalLayout_end.addWidget(self.line_edit_end)

        self.btn_end_info = QPushButton(self.frame_end_date)
        self.btn_end_info.setObjectName(u"btn_end_info")
        self.btn_end_info.setIcon(icon)
        self.btn_end_info.setIconSize(QSize(40, 40))
        self.btn_end_info.setFlat(True)

        self.horizontalLayout_end.addWidget(self.btn_end_info)


        self.verticalLayout_7.addWidget(self.frame_end_date)


        self.verticalLayout_5.addWidget(self.frame_date_range)

        self.line_separator_2 = QFrame(self.groupBox_input)
        self.line_separator_2.setObjectName(u"line_separator_2")
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_separator_2)

        self.frame_btns_data = QFrame(self.groupBox_input)
        self.frame_btns_data.setObjectName(u"frame_btns_data")
        self.frame_btns_data.setEnabled(True)
        self.frame_btns_data.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_6 = QVBoxLayout(self.frame_btns_data)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.btn_download_wind = QPushButton(self.frame_btns_data)
        self.btn_download_wind.setObjectName(u"btn_download_wind")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_download_wind.sizePolicy().hasHeightForWidth())
        self.btn_download_wind.setSizePolicy(sizePolicy3)

        self.verticalLayout_6.addWidget(self.btn_download_wind)

        self.btn_validate_own_data = QPushButton(self.frame_btns_data)
        self.btn_validate_own_data.setObjectName(u"btn_validate_own_data")

        self.verticalLayout_6.addWidget(self.btn_validate_own_data)

        self.frame_process_wind = QFrame(self.frame_btns_data)
        self.frame_process_wind.setObjectName(u"frame_process_wind")
        self.frame_process_wind.setFrameShape(QFrame.NoFrame)
        self.frame_process_wind.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_process_wind)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_process_wind = QPushButton(self.frame_process_wind)
        self.btn_process_wind.setObjectName(u"btn_process_wind")

        self.horizontalLayout.addWidget(self.btn_process_wind)

        self.btn_process_info = QPushButton(self.frame_process_wind)
        self.btn_process_info.setObjectName(u"btn_process_info")
        self.btn_process_info.setIcon(icon)
        self.btn_process_info.setIconSize(QSize(40, 40))
        self.btn_process_info.setFlat(True)

        self.horizontalLayout.addWidget(self.btn_process_info)


        self.verticalLayout_6.addWidget(self.frame_process_wind)


        self.verticalLayout_5.addWidget(self.frame_btns_data)

        self.label_hint_selection = QLabel(self.groupBox_input)
        self.label_hint_selection.setObjectName(u"label_hint_selection")

        self.verticalLayout_5.addWidget(self.label_hint_selection)


        self.verticalLayout_4.addWidget(self.groupBox_input)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout_3.addWidget(self.frame_data)


        self.verticalLayout_2.addWidget(self.frame_main)

        self.windStackedWidget.addWidget(self.page_data)

        self.verticalLayout.addWidget(self.windStackedWidget)


        self.retranslateUi(WindPage)

        self.windStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(WindPage)
    # setupUi

    def retranslateUi(self, WindPage):
        WindPage.setWindowTitle(QCoreApplication.translate("WindPage", u"Form", None))
        self.groupBox_input.setTitle(QCoreApplication.translate("WindPage", u"Wind Data Input", None))
        self.label_source_hint.setText(QCoreApplication.translate("WindPage", u"Select a data source.", None))
        self.combo_data_source.setItemText(0, QCoreApplication.translate("WindPage", u"-- Select Option --", None))
        self.combo_data_source.setItemText(1, QCoreApplication.translate("WindPage", u"Use Your Own Data", None))
        self.combo_data_source.setItemText(2, QCoreApplication.translate("WindPage", u"Download Wind Data from ERA5", None))
        self.combo_data_source.setItemText(3, QCoreApplication.translate("WindPage", u"No Wind Data", None))

        self.label_start_year.setText(QCoreApplication.translate("WindPage", u"Start Year", None))
        self.line_edit_start.setPlaceholderText(QCoreApplication.translate("WindPage", u"e.g. 2018", None))
        self.btn_start_info.setText("")
        self.label_end_year.setText(QCoreApplication.translate("WindPage", u"End Year", None))
        self.line_edit_end.setPlaceholderText(QCoreApplication.translate("WindPage", u"e.g. 2023", None))
        self.btn_end_info.setText("")
        self.btn_download_wind.setText(QCoreApplication.translate("WindPage", u"Download Wind Data", None))
        self.btn_validate_own_data.setText(QCoreApplication.translate("WindPage", u"Validate Uploaded Data", None))
        self.btn_process_wind.setText(QCoreApplication.translate("WindPage", u"Process Wind Data", None))
        self.btn_process_info.setText("")
        self.label_hint_selection.setText(QCoreApplication.translate("WindPage", u"Please select an option.", None))
    # retranslateUi

