# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solar.ui'
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
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_SolarPage(object):
    def setupUi(self, SolarPage):
        if not SolarPage.objectName():
            SolarPage.setObjectName(u"SolarPage")
        SolarPage.resize(1163, 908)
        self.verticalLayout = QVBoxLayout(SolarPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.solarStackedWidget = QStackedWidget(SolarPage)
        self.solarStackedWidget.setObjectName(u"solarStackedWidget")
        self.solarStackedWidget.setContextMenuPolicy(Qt.DefaultContextMenu)
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
        self.main_frame.setFrameShape(QFrame.NoFrame)
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
        self.data_frame.setFrameShape(QFrame.NoFrame)
        self.data_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.data_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.groupBox_input = QGroupBox(self.data_frame)
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

        self.frame_start_date = QFrame(self.groupBox_input)
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


        self.verticalLayout_5.addWidget(self.frame_start_date)

        self.frame_end_date = QFrame(self.groupBox_input)
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

        self.pushButton_2 = QPushButton(self.frame_end_date)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QSize(40, 40))
        self.pushButton_2.setFlat(True)

        self.horizontalLayout_end.addWidget(self.pushButton_2)


        self.verticalLayout_5.addWidget(self.frame_end_date)

        self.line_separator_2 = QFrame(self.groupBox_input)
        self.line_separator_2.setObjectName(u"line_separator_2")
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_separator_2)

        self.frame_btns_data = QFrame(self.groupBox_input)
        self.frame_btns_data.setObjectName(u"frame_btns_data")
        self.frame_btns_data.setEnabled(True)
        self.frame_btns_data.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_buttons = QHBoxLayout(self.frame_btns_data)
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.btn_download_solar = QPushButton(self.frame_btns_data)
        self.btn_download_solar.setObjectName(u"btn_download_solar")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_download_solar.sizePolicy().hasHeightForWidth())
        self.btn_download_solar.setSizePolicy(sizePolicy3)

        self.horizontalLayout_buttons.addWidget(self.btn_download_solar)


        self.verticalLayout_5.addWidget(self.frame_btns_data)


        self.verticalLayout_4.addWidget(self.groupBox_input)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout_3.addWidget(self.data_frame)


        self.verticalLayout_2.addWidget(self.main_frame)

        self.solarStackedWidget.addWidget(self.page_data)
        self.page_cluster = QWidget()
        self.page_cluster.setObjectName(u"page_cluster")
        self.verticalLayout_6 = QVBoxLayout(self.page_cluster)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.second_frame = QFrame(self.page_cluster)
        self.second_frame.setObjectName(u"second_frame")
        self.second_frame.setFrameShape(QFrame.NoFrame)
        self.second_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.second_frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.cluster_frame = QFrame(self.second_frame)
        self.cluster_frame.setObjectName(u"cluster_frame")
        self.cluster_frame.setFrameShape(QFrame.NoFrame)
        self.cluster_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.cluster_frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)

        self.groupBox_cluster = QGroupBox(self.cluster_frame)
        self.groupBox_cluster.setObjectName(u"groupBox_cluster")
        self.groupBox_cluster.setFont(font)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_cluster)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_algo_hint = QLabel(self.groupBox_cluster)
        self.label_algo_hint.setObjectName(u"label_algo_hint")
        sizePolicy2.setHeightForWidth(self.label_algo_hint.sizePolicy().hasHeightForWidth())
        self.label_algo_hint.setSizePolicy(sizePolicy2)
        self.label_algo_hint.setFont(font)

        self.verticalLayout_9.addWidget(self.label_algo_hint)

        self.radio_btn_k_means = QRadioButton(self.groupBox_cluster)
        self.radio_btn_k_means.setObjectName(u"radio_btn_k_means")
        self.radio_btn_k_means.setFont(font)
        self.radio_btn_k_means.setCheckable(True)
        self.radio_btn_k_means.setChecked(True)

        self.verticalLayout_9.addWidget(self.radio_btn_k_means)

        self.line_seperator_3 = QFrame(self.groupBox_cluster)
        self.line_seperator_3.setObjectName(u"line_seperator_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.line_seperator_3.sizePolicy().hasHeightForWidth())
        self.line_seperator_3.setSizePolicy(sizePolicy4)
        self.line_seperator_3.setFrameShape(QFrame.HLine)
        self.line_seperator_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_seperator_3)

        self.frame_num_cluster = QFrame(self.groupBox_cluster)
        self.frame_num_cluster.setObjectName(u"frame_num_cluster")
        self.frame_num_cluster.setFrameShape(QFrame.NoFrame)
        self.frame_num_cluster.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_num_cluster)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_num_cluster = QLabel(self.frame_num_cluster)
        self.label_num_cluster.setObjectName(u"label_num_cluster")
        self.label_num_cluster.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_num_cluster)

        self.spin_box_num_cluster = QSpinBox(self.frame_num_cluster)
        self.spin_box_num_cluster.setObjectName(u"spin_box_num_cluster")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.spin_box_num_cluster.sizePolicy().hasHeightForWidth())
        self.spin_box_num_cluster.setSizePolicy(sizePolicy5)
        self.spin_box_num_cluster.setMaximumSize(QSize(300, 16777215))
        self.spin_box_num_cluster.setMinimum(0)
        self.spin_box_num_cluster.setMaximum(20)

        self.horizontalLayout_2.addWidget(self.spin_box_num_cluster)

        self.horizontalSpacer = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_eval_cluster = QPushButton(self.frame_num_cluster)
        self.btn_eval_cluster.setObjectName(u"btn_eval_cluster")
        self.btn_eval_cluster.setFont(font)

        self.horizontalLayout_2.addWidget(self.btn_eval_cluster)

        self.btn_open_results = QPushButton(self.frame_num_cluster)
        self.btn_open_results.setObjectName(u"btn_open_results")
        self.btn_open_results.setFont(font)

        self.horizontalLayout_2.addWidget(self.btn_open_results)

        self.btn_info_num_cluster = QPushButton(self.frame_num_cluster)
        self.btn_info_num_cluster.setObjectName(u"btn_info_num_cluster")
        self.btn_info_num_cluster.setIcon(icon)
        self.btn_info_num_cluster.setIconSize(QSize(40, 40))
        self.btn_info_num_cluster.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btn_info_num_cluster)


        self.verticalLayout_9.addWidget(self.frame_num_cluster)

        self.line_seperator_4 = QFrame(self.groupBox_cluster)
        self.line_seperator_4.setObjectName(u"line_seperator_4")
        sizePolicy4.setHeightForWidth(self.line_seperator_4.sizePolicy().hasHeightForWidth())
        self.line_seperator_4.setSizePolicy(sizePolicy4)
        self.line_seperator_4.setFrameShape(QFrame.HLine)
        self.line_seperator_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_seperator_4)

        self.frame_final_cluster = QFrame(self.groupBox_cluster)
        self.frame_final_cluster.setObjectName(u"frame_final_cluster")
        self.frame_final_cluster.setFrameShape(QFrame.NoFrame)
        self.frame_final_cluster.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_final_cluster)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_final_num_cluster = QLabel(self.frame_final_cluster)
        self.label_final_num_cluster.setObjectName(u"label_final_num_cluster")
        self.label_final_num_cluster.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_final_num_cluster)

        self.spin_box_final_num_cluster = QSpinBox(self.frame_final_cluster)
        self.spin_box_final_num_cluster.setObjectName(u"spin_box_final_num_cluster")
        sizePolicy5.setHeightForWidth(self.spin_box_final_num_cluster.sizePolicy().hasHeightForWidth())
        self.spin_box_final_num_cluster.setSizePolicy(sizePolicy5)
        self.spin_box_final_num_cluster.setMaximumSize(QSize(300, 16777215))
        self.spin_box_final_num_cluster.setMaximum(20)

        self.horizontalLayout_3.addWidget(self.spin_box_final_num_cluster)

        self.horizontalSpacer_2 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.btn_gen_cluster = QPushButton(self.frame_final_cluster)
        self.btn_gen_cluster.setObjectName(u"btn_gen_cluster")
        self.btn_gen_cluster.setFont(font)

        self.horizontalLayout_3.addWidget(self.btn_gen_cluster)

        self.btn_info_final_num_cluster = QPushButton(self.frame_final_cluster)
        self.btn_info_final_num_cluster.setObjectName(u"btn_info_final_num_cluster")
        self.btn_info_final_num_cluster.setIcon(icon)
        self.btn_info_final_num_cluster.setIconSize(QSize(40, 40))
        self.btn_info_final_num_cluster.setFlat(True)

        self.horizontalLayout_3.addWidget(self.btn_info_final_num_cluster)


        self.verticalLayout_9.addWidget(self.frame_final_cluster)

        self.line_seperator_5 = QFrame(self.groupBox_cluster)
        self.line_seperator_5.setObjectName(u"line_seperator_5")
        self.line_seperator_5.setFrameShape(QFrame.HLine)
        self.line_seperator_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_seperator_5)

        self.frame_btns_cluster = QFrame(self.groupBox_cluster)
        self.frame_btns_cluster.setObjectName(u"frame_btns_cluster")
        self.frame_btns_cluster.setFrameShape(QFrame.Panel)
        self.frame_btns_cluster.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_btns_cluster)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.btn_skip = QPushButton(self.frame_btns_cluster)
        self.btn_skip.setObjectName(u"btn_skip")
        self.btn_skip.setFont(font)

        self.horizontalLayout_4.addWidget(self.btn_skip)

        self.btn_info_skip = QPushButton(self.frame_btns_cluster)
        self.btn_info_skip.setObjectName(u"btn_info_skip")
        self.btn_info_skip.setIcon(icon)
        self.btn_info_skip.setIconSize(QSize(40, 40))
        self.btn_info_skip.setFlat(True)

        self.horizontalLayout_4.addWidget(self.btn_info_skip)


        self.verticalLayout_9.addWidget(self.frame_btns_cluster)


        self.verticalLayout_8.addWidget(self.groupBox_cluster)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_4)


        self.verticalLayout_7.addWidget(self.cluster_frame)

        self.nav_bottom_cluster = QWidget(self.second_frame)
        self.nav_bottom_cluster.setObjectName(u"nav_bottom_cluster")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.nav_bottom_cluster.sizePolicy().hasHeightForWidth())
        self.nav_bottom_cluster.setSizePolicy(sizePolicy6)
        self.nav_bottom_cluster.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.nav_bottom_cluster)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bottom_spacer_cluster = QSpacerItem(987, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.bottom_spacer_cluster)

        self.btn_prev_page_cluster = QPushButton(self.nav_bottom_cluster)
        self.btn_prev_page_cluster.setObjectName(u"btn_prev_page_cluster")

        self.horizontalLayout.addWidget(self.btn_prev_page_cluster)

        self.btn_next_page_cluster = QPushButton(self.nav_bottom_cluster)
        self.btn_next_page_cluster.setObjectName(u"btn_next_page_cluster")

        self.horizontalLayout.addWidget(self.btn_next_page_cluster)


        self.verticalLayout_7.addWidget(self.nav_bottom_cluster)


        self.verticalLayout_6.addWidget(self.second_frame)

        self.solarStackedWidget.addWidget(self.page_cluster)

        self.verticalLayout.addWidget(self.solarStackedWidget)


        self.retranslateUi(SolarPage)

        self.solarStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SolarPage)
    # setupUi

    def retranslateUi(self, SolarPage):
        SolarPage.setWindowTitle(QCoreApplication.translate("SolarPage", u"Form", None))
        self.groupBox_input.setTitle(QCoreApplication.translate("SolarPage", u"Solar Data Input", None))
        self.label_source_hint.setText(QCoreApplication.translate("SolarPage", u"Select a data source.", None))
        self.combo_data_source.setItemText(0, QCoreApplication.translate("SolarPage", u"-- Select Option --", None))
        self.combo_data_source.setItemText(1, QCoreApplication.translate("SolarPage", u"Use Your Own Data", None))
        self.combo_data_source.setItemText(2, QCoreApplication.translate("SolarPage", u"Download Solar Data from ERA5", None))
        self.combo_data_source.setItemText(3, QCoreApplication.translate("SolarPage", u"No Solar Data", None))

        self.label_start_year.setText(QCoreApplication.translate("SolarPage", u"Start Year", None))
        self.line_edit_start.setPlaceholderText(QCoreApplication.translate("SolarPage", u"e.g. 2018", None))
        self.btn_start_info.setText("")
        self.label_end_year.setText(QCoreApplication.translate("SolarPage", u"End Year", None))
        self.line_edit_end.setPlaceholderText(QCoreApplication.translate("SolarPage", u"e.g. 2023", None))
        self.pushButton_2.setText("")
        self.btn_download_solar.setText(QCoreApplication.translate("SolarPage", u"Download Solar Data", None))
        self.groupBox_cluster.setTitle(QCoreApplication.translate("SolarPage", u"Clustering Method", None))
        self.label_algo_hint.setText(QCoreApplication.translate("SolarPage", u"Select ML Algorithm:", None))
        self.radio_btn_k_means.setText(QCoreApplication.translate("SolarPage", u"K-Means", None))
        self.label_num_cluster.setText(QCoreApplication.translate("SolarPage", u"No. of Clusters:", None))
        self.btn_eval_cluster.setText(QCoreApplication.translate("SolarPage", u"Evaluate", None))
        self.btn_open_results.setText(QCoreApplication.translate("SolarPage", u"Open Results", None))
        self.btn_info_num_cluster.setText("")
        self.label_final_num_cluster.setText(QCoreApplication.translate("SolarPage", u"Final No. of Clusters:", None))
        self.btn_gen_cluster.setText(QCoreApplication.translate("SolarPage", u"Generate", None))
        self.btn_info_final_num_cluster.setText("")
        self.btn_skip.setText(QCoreApplication.translate("SolarPage", u"Skip", None))
        self.btn_info_skip.setText("")
        self.btn_prev_page_cluster.setText(QCoreApplication.translate("SolarPage", u"Prev", None))
        self.btn_next_page_cluster.setText(QCoreApplication.translate("SolarPage", u"Next", None))
    # retranslateUi

