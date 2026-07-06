# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'simulation.ui'
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
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_SimulationPage(object):
    def setupUi(self, SimulationPage):
        if not SimulationPage.objectName():
            SimulationPage.setObjectName(u"SimulationPage")
        SimulationPage.resize(1183, 928)
        self.horizontalLayout_11 = QHBoxLayout(SimulationPage)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.frame_main = QFrame(SimulationPage)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout_container = QVBoxLayout(self.frame_main)
        self.verticalLayout_container.setObjectName(u"verticalLayout_container")
        self.verticalSpacer_top = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_container.addItem(self.verticalSpacer_top)

        self.frame_simulation = QFrame(self.frame_main)
        self.frame_simulation.setObjectName(u"frame_simulation")
        self.frame_simulation.setFrameShape(QFrame.NoFrame)
        self.frame_simulation.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_simulation)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_simulation = QGroupBox(self.frame_simulation)
        self.groupBox_simulation.setObjectName(u"groupBox_simulation")
        font = QFont()
        font.setPointSize(16)
        self.groupBox_simulation.setFont(font)
        self.verticalLayout_simulation = QVBoxLayout(self.groupBox_simulation)
        self.verticalLayout_simulation.setObjectName(u"verticalLayout_simulation")
        self.label_sim_hint = QLabel(self.groupBox_simulation)
        self.label_sim_hint.setObjectName(u"label_sim_hint")

        self.verticalLayout_simulation.addWidget(self.label_sim_hint)

        self.line_separator_1 = QFrame(self.groupBox_simulation)
        self.line_separator_1.setObjectName(u"line_separator_1")
        self.line_separator_1.setFrameShape(QFrame.HLine)
        self.line_separator_1.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_simulation.addWidget(self.line_separator_1)

        self.frame_center = QFrame(self.groupBox_simulation)
        self.frame_center.setObjectName(u"frame_center")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.frame_progress_params = QFrame(self.frame_center)
        self.frame_progress_params.setObjectName(u"frame_progress_params")
        self.frame_progress_params.setFrameShape(QFrame.NoFrame)
        self.frame_progress_params.setFrameShadow(QFrame.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.frame_progress_params)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_samples = QFrame(self.frame_progress_params)
        self.frame_samples.setObjectName(u"frame_samples")
        self.frame_samples.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_samples = QHBoxLayout(self.frame_samples)
        self.horizontalLayout_samples.setObjectName(u"horizontalLayout_samples")
        self.horizontalLayout_samples.setContentsMargins(-1, 0, -1, 0)
        self.label_samples = QLabel(self.frame_samples)
        self.label_samples.setObjectName(u"label_samples")
        self.label_samples.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_samples.addWidget(self.label_samples)

        self.lineEdit_samples = QLineEdit(self.frame_samples)
        self.lineEdit_samples.setObjectName(u"lineEdit_samples")

        self.horizontalLayout_samples.addWidget(self.lineEdit_samples)

        self.btn_info_samples = QPushButton(self.frame_samples)
        self.btn_info_samples.setObjectName(u"btn_info_samples")
        icon = QIcon()
        icon.addFile(u":/icons/Images/icons/about.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_info_samples.setIcon(icon)
        self.btn_info_samples.setIconSize(QSize(40, 40))
        self.btn_info_samples.setFlat(True)

        self.horizontalLayout_samples.addWidget(self.btn_info_samples)


        self.verticalLayout_2.addWidget(self.frame_samples)

        self.frame_hours = QFrame(self.frame_progress_params)
        self.frame_hours.setObjectName(u"frame_hours")
        self.frame_hours.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_hours = QHBoxLayout(self.frame_hours)
        self.horizontalLayout_hours.setObjectName(u"horizontalLayout_hours")
        self.horizontalLayout_hours.setContentsMargins(-1, 0, -1, 0)
        self.label_hours = QLabel(self.frame_hours)
        self.label_hours.setObjectName(u"label_hours")
        self.label_hours.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_hours.addWidget(self.label_hours)

        self.lineEdit_hours = QLineEdit(self.frame_hours)
        self.lineEdit_hours.setObjectName(u"lineEdit_hours")

        self.horizontalLayout_hours.addWidget(self.lineEdit_hours)

        self.btn_info_hours = QPushButton(self.frame_hours)
        self.btn_info_hours.setObjectName(u"btn_info_hours")
        self.btn_info_hours.setIcon(icon)
        self.btn_info_hours.setIconSize(QSize(40, 40))
        self.btn_info_hours.setFlat(True)

        self.horizontalLayout_hours.addWidget(self.btn_info_hours)


        self.verticalLayout_2.addWidget(self.frame_hours)

        self.frame_load_factor = QFrame(self.frame_progress_params)
        self.frame_load_factor.setObjectName(u"frame_load_factor")
        self.frame_load_factor.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_load_factor = QHBoxLayout(self.frame_load_factor)
        self.horizontalLayout_load_factor.setObjectName(u"horizontalLayout_load_factor")
        self.horizontalLayout_load_factor.setContentsMargins(-1, 0, -1, 0)
        self.label_load_factor = QLabel(self.frame_load_factor)
        self.label_load_factor.setObjectName(u"label_load_factor")
        self.label_load_factor.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_load_factor.addWidget(self.label_load_factor)

        self.lineEdit_load_factor = QLineEdit(self.frame_load_factor)
        self.lineEdit_load_factor.setObjectName(u"lineEdit_load_factor")

        self.horizontalLayout_load_factor.addWidget(self.lineEdit_load_factor)

        self.btn_info_load_factor = QPushButton(self.frame_load_factor)
        self.btn_info_load_factor.setObjectName(u"btn_info_load_factor")
        self.btn_info_load_factor.setIcon(icon)
        self.btn_info_load_factor.setIconSize(QSize(40, 40))
        self.btn_info_load_factor.setFlat(True)

        self.horizontalLayout_load_factor.addWidget(self.btn_info_load_factor)


        self.verticalLayout_2.addWidget(self.frame_load_factor)

        self.frame_model_type = QFrame(self.frame_progress_params)
        self.frame_model_type.setObjectName(u"frame_model_type")
        self.frame_model_type.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_model_type = QHBoxLayout(self.frame_model_type)
        self.horizontalLayout_model_type.setObjectName(u"horizontalLayout_model_type")
        self.horizontalLayout_model_type.setContentsMargins(-1, 0, -1, 0)
        self.label_model_type = QLabel(self.frame_model_type)
        self.label_model_type.setObjectName(u"label_model_type")
        self.label_model_type.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_model_type.addWidget(self.label_model_type)

        self.comboBox_model_type = QComboBox(self.frame_model_type)
        self.comboBox_model_type.addItem("")
        self.comboBox_model_type.addItem("")
        self.comboBox_model_type.addItem("")
        self.comboBox_model_type.setObjectName(u"comboBox_model_type")

        self.horizontalLayout_model_type.addWidget(self.comboBox_model_type)

        self.spacer_model = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_model_type.addItem(self.spacer_model)

        self.btn_info_model_type = QPushButton(self.frame_model_type)
        self.btn_info_model_type.setObjectName(u"btn_info_model_type")
        self.btn_info_model_type.setIcon(icon)
        self.btn_info_model_type.setIconSize(QSize(40, 40))
        self.btn_info_model_type.setFlat(True)

        self.horizontalLayout_model_type.addWidget(self.btn_info_model_type)


        self.verticalLayout_2.addWidget(self.frame_model_type)

        self.frame_opt_period = QFrame(self.frame_progress_params)
        self.frame_opt_period.setObjectName(u"frame_opt_period")
        self.frame_opt_period.setFrameShape(QFrame.NoFrame)
        self.frame_opt_period.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_opt_period)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.label_opt_period = QLabel(self.frame_opt_period)
        self.label_opt_period.setObjectName(u"label_opt_period")
        self.label_opt_period.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_2.addWidget(self.label_opt_period)

        self.lineEdit_opt_period = QLineEdit(self.frame_opt_period)
        self.lineEdit_opt_period.setObjectName(u"lineEdit_opt_period")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_opt_period.sizePolicy().hasHeightForWidth())
        self.lineEdit_opt_period.setSizePolicy(sizePolicy)
        self.lineEdit_opt_period.setMaxLength(8760)
        self.lineEdit_opt_period.setCursorPosition(0)

        self.horizontalLayout_2.addWidget(self.lineEdit_opt_period)

        self.btn_info_opt_period = QPushButton(self.frame_opt_period)
        self.btn_info_opt_period.setObjectName(u"btn_info_opt_period")
        self.btn_info_opt_period.setIcon(icon)
        self.btn_info_opt_period.setIconSize(QSize(40, 40))
        self.btn_info_opt_period.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btn_info_opt_period)


        self.verticalLayout_2.addWidget(self.frame_opt_period)


        self.horizontalLayout_8.addWidget(self.frame_progress_params)

        self.line_seperator_3 = QFrame(self.frame_center)
        self.line_seperator_3.setObjectName(u"line_seperator_3")
        self.line_seperator_3.setFrameShape(QFrame.VLine)
        self.line_seperator_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line_seperator_3)

        self.frame_pcm_params = QFrame(self.frame_center)
        self.frame_pcm_params.setObjectName(u"frame_pcm_params")
        self.frame_pcm_params.setFrameShape(QFrame.NoFrame)
        self.frame_pcm_params.setFrameShadow(QFrame.Plain)
        self.verticalLayout_3 = QVBoxLayout(self.frame_pcm_params)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_dc_load = QFrame(self.frame_pcm_params)
        self.frame_dc_load.setObjectName(u"frame_dc_load")
        self.frame_dc_load.setFrameShape(QFrame.NoFrame)
        self.frame_dc_load.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_dc_load)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.label_dc_load = QLabel(self.frame_dc_load)
        self.label_dc_load.setObjectName(u"label_dc_load")

        self.horizontalLayout_6.addWidget(self.label_dc_load)

        self.radio_dc_load_true = QRadioButton(self.frame_dc_load)
        self.radio_dc_load_true.setObjectName(u"radio_dc_load_true")

        self.horizontalLayout_6.addWidget(self.radio_dc_load_true)

        self.radio_dc_load_false = QRadioButton(self.frame_dc_load)
        self.radio_dc_load_false.setObjectName(u"radio_dc_load_false")
        self.radio_dc_load_false.setChecked(True)

        self.horizontalLayout_6.addWidget(self.radio_dc_load_false)

        self.btn_info_dc_load = QPushButton(self.frame_dc_load)
        self.btn_info_dc_load.setObjectName(u"btn_info_dc_load")
        self.btn_info_dc_load.setIcon(icon)
        self.btn_info_dc_load.setIconSize(QSize(40, 40))
        self.btn_info_dc_load.setFlat(True)

        self.horizontalLayout_6.addWidget(self.btn_info_dc_load)


        self.verticalLayout_3.addWidget(self.frame_dc_load)

        self.frame_degradation_eval = QFrame(self.frame_pcm_params)
        self.frame_degradation_eval.setObjectName(u"frame_degradation_eval")
        self.frame_degradation_eval.setMinimumSize(QSize(140, 0))
        self.frame_degradation_eval.setFrameShape(QFrame.NoFrame)
        self.frame_degradation_eval.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_degradation_eval)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.label_degradation_eval = QLabel(self.frame_degradation_eval)
        self.label_degradation_eval.setObjectName(u"label_degradation_eval")

        self.horizontalLayout_3.addWidget(self.label_degradation_eval)

        self.radio_degradation_eval_true = QRadioButton(self.frame_degradation_eval)
        self.radio_degradation_eval_true.setObjectName(u"radio_degradation_eval_true")

        self.horizontalLayout_3.addWidget(self.radio_degradation_eval_true)

        self.radio_degradation_eval_false = QRadioButton(self.frame_degradation_eval)
        self.radio_degradation_eval_false.setObjectName(u"radio_degradation_eval_false")
        self.radio_degradation_eval_false.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radio_degradation_eval_false)

        self.btn_info_degradation_eval = QPushButton(self.frame_degradation_eval)
        self.btn_info_degradation_eval.setObjectName(u"btn_info_degradation_eval")
        self.btn_info_degradation_eval.setIcon(icon)
        self.btn_info_degradation_eval.setIconSize(QSize(40, 40))
        self.btn_info_degradation_eval.setFlat(True)

        self.horizontalLayout_3.addWidget(self.btn_info_degradation_eval)


        self.verticalLayout_3.addWidget(self.frame_degradation_eval)

        self.frame_degradation_int = QFrame(self.frame_pcm_params)
        self.frame_degradation_int.setObjectName(u"frame_degradation_int")
        self.frame_degradation_int.setFrameShape(QFrame.NoFrame)
        self.frame_degradation_int.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_degradation_int)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.label_degradation_int = QLabel(self.frame_degradation_int)
        self.label_degradation_int.setObjectName(u"label_degradation_int")
        self.label_degradation_int.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_4.addWidget(self.label_degradation_int)

        self.lineEdit_degradation_int = QLineEdit(self.frame_degradation_int)
        self.lineEdit_degradation_int.setObjectName(u"lineEdit_degradation_int")

        self.horizontalLayout_4.addWidget(self.lineEdit_degradation_int)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.btn_info_degradation_int = QPushButton(self.frame_degradation_int)
        self.btn_info_degradation_int.setObjectName(u"btn_info_degradation_int")
        self.btn_info_degradation_int.setIcon(icon)
        self.btn_info_degradation_int.setIconSize(QSize(40, 40))
        self.btn_info_degradation_int.setFlat(True)

        self.horizontalLayout_4.addWidget(self.btn_info_degradation_int)


        self.verticalLayout_3.addWidget(self.frame_degradation_int)

        self.frame_thermal_model = QFrame(self.frame_pcm_params)
        self.frame_thermal_model.setObjectName(u"frame_thermal_model")
        self.frame_thermal_model.setFrameShape(QFrame.NoFrame)
        self.frame_thermal_model.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_thermal_model)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.label_detailed_model = QLabel(self.frame_thermal_model)
        self.label_detailed_model.setObjectName(u"label_detailed_model")
        self.label_detailed_model.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_5.addWidget(self.label_detailed_model)

        self.radio_detailed_model_true = QRadioButton(self.frame_thermal_model)
        self.radio_detailed_model_true.setObjectName(u"radio_detailed_model_true")

        self.horizontalLayout_5.addWidget(self.radio_detailed_model_true)

        self.radio_detailed_model_false = QRadioButton(self.frame_thermal_model)
        self.radio_detailed_model_false.setObjectName(u"radio_detailed_model_false")
        self.radio_detailed_model_false.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radio_detailed_model_false)

        self.btn_info_detailed_model = QPushButton(self.frame_thermal_model)
        self.btn_info_detailed_model.setObjectName(u"btn_info_detailed_model")
        self.btn_info_detailed_model.setIcon(icon)
        self.btn_info_detailed_model.setIconSize(QSize(40, 40))
        self.btn_info_detailed_model.setFlat(True)

        self.horizontalLayout_5.addWidget(self.btn_info_detailed_model)


        self.verticalLayout_3.addWidget(self.frame_thermal_model)

        self.frame_pcm_check = QFrame(self.frame_pcm_params)
        self.frame_pcm_check.setObjectName(u"frame_pcm_check")
        self.frame_pcm_check.setFrameShape(QFrame.NoFrame)
        self.frame_pcm_check.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_pcm_check)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.label_use_pcm = QLabel(self.frame_pcm_check)
        self.label_use_pcm.setObjectName(u"label_use_pcm")

        self.horizontalLayout_7.addWidget(self.label_use_pcm)

        self.radio_use_pcm_true = QRadioButton(self.frame_pcm_check)
        self.radio_use_pcm_true.setObjectName(u"radio_use_pcm_true")

        self.horizontalLayout_7.addWidget(self.radio_use_pcm_true)

        self.radio_use_pcm_false = QRadioButton(self.frame_pcm_check)
        self.radio_use_pcm_false.setObjectName(u"radio_use_pcm_false")
        self.radio_use_pcm_false.setChecked(True)

        self.horizontalLayout_7.addWidget(self.radio_use_pcm_false)

        self.btn_pcm_config = QPushButton(self.frame_pcm_check)
        self.btn_pcm_config.setObjectName(u"btn_pcm_config")

        self.horizontalLayout_7.addWidget(self.btn_pcm_config)

        self.btn_info_use_pcm = QPushButton(self.frame_pcm_check)
        self.btn_info_use_pcm.setObjectName(u"btn_info_use_pcm")
        self.btn_info_use_pcm.setIcon(icon)
        self.btn_info_use_pcm.setIconSize(QSize(40, 40))
        self.btn_info_use_pcm.setFlat(True)

        self.horizontalLayout_7.addWidget(self.btn_info_use_pcm)


        self.verticalLayout_3.addWidget(self.frame_pcm_check)


        self.horizontalLayout_8.addWidget(self.frame_pcm_params)


        self.verticalLayout_simulation.addWidget(self.frame_center)

        self.line_separator_2 = QFrame(self.groupBox_simulation)
        self.line_separator_2.setObjectName(u"line_separator_2")
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_simulation.addWidget(self.line_separator_2)

        self.frame_run_button = QFrame(self.groupBox_simulation)
        self.frame_run_button.setObjectName(u"frame_run_button")
        self.frame_run_button.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_run_button = QHBoxLayout(self.frame_run_button)
        self.horizontalLayout_run_button.setObjectName(u"horizontalLayout_run_button")
        self.horizontalSpacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_run_button.addItem(self.horizontalSpacer_left)

        self.btn_save_config = QPushButton(self.frame_run_button)
        self.btn_save_config.setObjectName(u"btn_save_config")

        self.horizontalLayout_run_button.addWidget(self.btn_save_config)

        self.btn_run_simulation = QPushButton(self.frame_run_button)
        self.btn_run_simulation.setObjectName(u"btn_run_simulation")

        self.horizontalLayout_run_button.addWidget(self.btn_run_simulation)

        self.btn_stop_simulation = QPushButton(self.frame_run_button)
        self.btn_stop_simulation.setObjectName(u"btn_stop_simulation")

        self.horizontalLayout_run_button.addWidget(self.btn_stop_simulation)

        self.horizontalSpacer_right = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_run_button.addItem(self.horizontalSpacer_right)


        self.verticalLayout_simulation.addWidget(self.frame_run_button)


        self.horizontalLayout.addWidget(self.groupBox_simulation)


        self.verticalLayout_container.addWidget(self.frame_simulation)

        self.verticalSpacer_bottom = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_container.addItem(self.verticalSpacer_bottom)


        self.horizontalLayout_11.addWidget(self.frame_main)


        self.retranslateUi(SimulationPage)

        QMetaObject.connectSlotsByName(SimulationPage)
    # setupUi

    def retranslateUi(self, SimulationPage):
        SimulationPage.setWindowTitle(QCoreApplication.translate("SimulationPage", u"Form", None))
        self.groupBox_simulation.setTitle(QCoreApplication.translate("SimulationPage", u" Monte Carlo Simulation Parameters", None))
        self.label_sim_hint.setText(QCoreApplication.translate("SimulationPage", u"Enter the simulation parameters below.", None))
        self.label_samples.setText(QCoreApplication.translate("SimulationPage", u"Samples", None))
        self.lineEdit_samples.setPlaceholderText(QCoreApplication.translate("SimulationPage", u"Enter number of samples", None))
        self.label_hours.setText(QCoreApplication.translate("SimulationPage", u"Simulation Hours", None))
        self.lineEdit_hours.setText("")
        self.lineEdit_hours.setPlaceholderText(QCoreApplication.translate("SimulationPage", u"e.g. 8000", None))
        self.btn_info_hours.setText("")
        self.label_load_factor.setText(QCoreApplication.translate("SimulationPage", u"Load Factor", None))
        self.lineEdit_load_factor.setText("")
        self.lineEdit_load_factor.setPlaceholderText(QCoreApplication.translate("SimulationPage", u"e.g. 1", None))
        self.btn_info_load_factor.setText("")
        self.label_model_type.setText(QCoreApplication.translate("SimulationPage", u"Model Type", None))
        self.comboBox_model_type.setItemText(0, QCoreApplication.translate("SimulationPage", u"Zonal Model", None))
        self.comboBox_model_type.setItemText(1, QCoreApplication.translate("SimulationPage", u"Copper Sheet Model", None))
        self.comboBox_model_type.setItemText(2, QCoreApplication.translate("SimulationPage", u"Nodal", None))

        self.btn_info_model_type.setText("")
        self.label_opt_period.setText(QCoreApplication.translate("SimulationPage", u"Optimization Period", None))
        self.lineEdit_opt_period.setPlaceholderText(QCoreApplication.translate("SimulationPage", u"e.g. 24", None))
        self.btn_info_opt_period.setText("")
        self.label_dc_load.setText(QCoreApplication.translate("SimulationPage", u"DC Load", None))
        self.radio_dc_load_true.setText(QCoreApplication.translate("SimulationPage", u"True", None))
        self.radio_dc_load_false.setText(QCoreApplication.translate("SimulationPage", u"False", None))
        self.btn_info_dc_load.setText("")
        self.label_degradation_eval.setText(QCoreApplication.translate("SimulationPage", u"Evaluate Degradation", None))
        self.radio_degradation_eval_true.setText(QCoreApplication.translate("SimulationPage", u"True", None))
        self.radio_degradation_eval_false.setText(QCoreApplication.translate("SimulationPage", u"False", None))
        self.btn_info_degradation_eval.setText("")
        self.label_degradation_int.setText(QCoreApplication.translate("SimulationPage", u"Degradation Interval", None))
        self.lineEdit_degradation_int.setPlaceholderText(QCoreApplication.translate("SimulationPage", u"e.g. 128", None))
        self.btn_info_degradation_int.setText("")
        self.label_detailed_model.setText(QCoreApplication.translate("SimulationPage", u"Detailed Thermal Model ", None))
        self.radio_detailed_model_true.setText(QCoreApplication.translate("SimulationPage", u"True", None))
        self.radio_detailed_model_false.setText(QCoreApplication.translate("SimulationPage", u"False", None))
        self.btn_info_detailed_model.setText("")
        self.label_use_pcm.setText(QCoreApplication.translate("SimulationPage", u"Use PCM", None))
        self.radio_use_pcm_true.setText(QCoreApplication.translate("SimulationPage", u"True", None))
        self.radio_use_pcm_false.setText(QCoreApplication.translate("SimulationPage", u"False", None))
        self.btn_pcm_config.setText(QCoreApplication.translate("SimulationPage", u"Open PCM Config", None))
        self.btn_info_use_pcm.setText("")
        self.btn_save_config.setText(QCoreApplication.translate("SimulationPage", u"Save Config", None))
        self.btn_run_simulation.setText(QCoreApplication.translate("SimulationPage", u"Run Simulation", None))
        self.btn_stop_simulation.setText(QCoreApplication.translate("SimulationPage", u"Stop Simulation", None))
    # retranslateUi

