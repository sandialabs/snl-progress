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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_SimulationPage(object):
    def setupUi(self, SimulationPage):
        if not SimulationPage.objectName():
            SimulationPage.setObjectName(u"SimulationPage")
        SimulationPage.resize(1163, 908)
        self.verticalLayout_main = QVBoxLayout(SimulationPage)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
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

        self.frame_samples = QFrame(self.groupBox_simulation)
        self.frame_samples.setObjectName(u"frame_samples")
        self.frame_samples.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_samples = QHBoxLayout(self.frame_samples)
        self.horizontalLayout_samples.setObjectName(u"horizontalLayout_samples")
        self.label_samples = QLabel(self.frame_samples)
        self.label_samples.setObjectName(u"label_samples")
        self.label_samples.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_samples.addWidget(self.label_samples)

        self.lineEdit_samples = QLineEdit(self.frame_samples)
        self.lineEdit_samples.setObjectName(u"lineEdit_samples")

        self.horizontalLayout_samples.addWidget(self.lineEdit_samples)


        self.verticalLayout_simulation.addWidget(self.frame_samples)

        self.frame_hours = QFrame(self.groupBox_simulation)
        self.frame_hours.setObjectName(u"frame_hours")
        self.frame_hours.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_hours = QHBoxLayout(self.frame_hours)
        self.horizontalLayout_hours.setObjectName(u"horizontalLayout_hours")
        self.label_hours = QLabel(self.frame_hours)
        self.label_hours.setObjectName(u"label_hours")
        self.label_hours.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_hours.addWidget(self.label_hours)

        self.lineEdit_hours = QLineEdit(self.frame_hours)
        self.lineEdit_hours.setObjectName(u"lineEdit_hours")

        self.horizontalLayout_hours.addWidget(self.lineEdit_hours)


        self.verticalLayout_simulation.addWidget(self.frame_hours)

        self.frame_load_factor = QFrame(self.groupBox_simulation)
        self.frame_load_factor.setObjectName(u"frame_load_factor")
        self.frame_load_factor.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_load_factor = QHBoxLayout(self.frame_load_factor)
        self.horizontalLayout_load_factor.setObjectName(u"horizontalLayout_load_factor")
        self.label_load_factor = QLabel(self.frame_load_factor)
        self.label_load_factor.setObjectName(u"label_load_factor")
        self.label_load_factor.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_load_factor.addWidget(self.label_load_factor)

        self.lineEdit_load_factor = QLineEdit(self.frame_load_factor)
        self.lineEdit_load_factor.setObjectName(u"lineEdit_load_factor")

        self.horizontalLayout_load_factor.addWidget(self.lineEdit_load_factor)


        self.verticalLayout_simulation.addWidget(self.frame_load_factor)

        self.frame_model_type = QFrame(self.groupBox_simulation)
        self.frame_model_type.setObjectName(u"frame_model_type")
        self.frame_model_type.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_model_type = QHBoxLayout(self.frame_model_type)
        self.horizontalLayout_model_type.setObjectName(u"horizontalLayout_model_type")
        self.label_model_type = QLabel(self.frame_model_type)
        self.label_model_type.setObjectName(u"label_model_type")
        self.label_model_type.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_model_type.addWidget(self.label_model_type)

        self.comboBox_model_type = QComboBox(self.frame_model_type)
        self.comboBox_model_type.addItem("")
        self.comboBox_model_type.addItem("")
        self.comboBox_model_type.setObjectName(u"comboBox_model_type")

        self.horizontalLayout_model_type.addWidget(self.comboBox_model_type)


        self.verticalLayout_simulation.addWidget(self.frame_model_type)

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

        self.btn_run_simulation = QPushButton(self.frame_run_button)
        self.btn_run_simulation.setObjectName(u"btn_run_simulation")

        self.horizontalLayout_run_button.addWidget(self.btn_run_simulation)

        self.horizontalSpacer_right = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_run_button.addItem(self.horizontalSpacer_right)


        self.verticalLayout_simulation.addWidget(self.frame_run_button)


        self.horizontalLayout.addWidget(self.groupBox_simulation)


        self.verticalLayout_container.addWidget(self.frame_simulation)

        self.verticalSpacer_bottom = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_container.addItem(self.verticalSpacer_bottom)

        self.nav_bottom_sim = QWidget(self.frame_main)
        self.nav_bottom_sim.setObjectName(u"nav_bottom_sim")
        self.nav_bottom_sim.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_nav = QHBoxLayout(self.nav_bottom_sim)
        self.horizontalLayout_nav.setObjectName(u"horizontalLayout_nav")
        self.bottom_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_nav.addItem(self.bottom_spacer)

        self.btn_sim_previous = QPushButton(self.nav_bottom_sim)
        self.btn_sim_previous.setObjectName(u"btn_sim_previous")

        self.horizontalLayout_nav.addWidget(self.btn_sim_previous)

        self.btn_sim_next = QPushButton(self.nav_bottom_sim)
        self.btn_sim_next.setObjectName(u"btn_sim_next")

        self.horizontalLayout_nav.addWidget(self.btn_sim_next)


        self.verticalLayout_container.addWidget(self.nav_bottom_sim)


        self.verticalLayout_main.addWidget(self.frame_main)


        self.retranslateUi(SimulationPage)

        QMetaObject.connectSlotsByName(SimulationPage)
    # setupUi

    def retranslateUi(self, SimulationPage):
        SimulationPage.setWindowTitle(QCoreApplication.translate("SimulationPage", u"Form", None))
        self.groupBox_simulation.setTitle(QCoreApplication.translate("SimulationPage", u"Simulation Settings", None))
        self.label_sim_hint.setText(QCoreApplication.translate("SimulationPage", u"Enter the simulation settings below.", None))
        self.label_samples.setText(QCoreApplication.translate("SimulationPage", u"Samples", None))
        self.lineEdit_samples.setPlaceholderText(QCoreApplication.translate("SimulationPage", u"Enter number of samples", None))
        self.label_hours.setText(QCoreApplication.translate("SimulationPage", u"Simulation Hours", None))
        self.lineEdit_hours.setText("")
        self.lineEdit_hours.setPlaceholderText(QCoreApplication.translate("SimulationPage", u"e.g. 8000", None))
        self.label_load_factor.setText(QCoreApplication.translate("SimulationPage", u"Load Factor", None))
        self.lineEdit_load_factor.setText("")
        self.lineEdit_load_factor.setPlaceholderText(QCoreApplication.translate("SimulationPage", u"e.g. 1", None))
        self.label_model_type.setText(QCoreApplication.translate("SimulationPage", u"Model Type", None))
        self.comboBox_model_type.setItemText(0, QCoreApplication.translate("SimulationPage", u"Zonal Model", None))
        self.comboBox_model_type.setItemText(1, QCoreApplication.translate("SimulationPage", u"Copper Sheet Model", None))

        self.btn_run_simulation.setText(QCoreApplication.translate("SimulationPage", u"Run Simulation", None))
        self.btn_sim_previous.setText(QCoreApplication.translate("SimulationPage", u"Prev", None))
        self.btn_sim_next.setText(QCoreApplication.translate("SimulationPage", u"Next", None))
    # retranslateUi

