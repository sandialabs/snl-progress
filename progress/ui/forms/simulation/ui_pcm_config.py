# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pcm_config.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QDateTimeEdit,
    QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)
import resources_rc

class Ui_PCMConfigPage(object):
    def setupUi(self, PCMConfigPage):
        if not PCMConfigPage.objectName():
            PCMConfigPage.setObjectName(u"PCMConfigPage")
        PCMConfigPage.resize(630, 600)
        PCMConfigPage.setMinimumSize(QSize(630, 600))
        PCMConfigPage.setMaximumSize(QSize(630, 636))
        self.verticalLayout = QVBoxLayout(PCMConfigPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_pcm_config = QGroupBox(PCMConfigPage)
        self.groupBox_pcm_config.setObjectName(u"groupBox_pcm_config")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_pcm_config)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_pcm_venv = QFrame(self.groupBox_pcm_config)
        self.frame_pcm_venv.setObjectName(u"frame_pcm_venv")
        self.frame_pcm_venv.setFrameShape(QFrame.NoFrame)
        self.frame_pcm_venv.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_pcm_venv)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.label_pcm_venv = QLabel(self.frame_pcm_venv)
        self.label_pcm_venv.setObjectName(u"label_pcm_venv")

        self.horizontalLayout_14.addWidget(self.label_pcm_venv)

        self.lineEdit_pcm_venv = QLineEdit(self.frame_pcm_venv)
        self.lineEdit_pcm_venv.setObjectName(u"lineEdit_pcm_venv")

        self.horizontalLayout_14.addWidget(self.lineEdit_pcm_venv)

        self.btn_info_venv = QPushButton(self.frame_pcm_venv)
        self.btn_info_venv.setObjectName(u"btn_info_venv")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_venv.sizePolicy().hasHeightForWidth())
        self.btn_info_venv.setSizePolicy(sizePolicy)
        self.btn_info_venv.setMaximumSize(QSize(40, 16777215))
        icon = QIcon()
        icon.addFile(u":/icons/Images/icons/about.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_info_venv.setIcon(icon)
        self.btn_info_venv.setIconSize(QSize(40, 40))
        self.btn_info_venv.setFlat(True)

        self.horizontalLayout_14.addWidget(self.btn_info_venv)


        self.verticalLayout_2.addWidget(self.frame_pcm_venv)

        self.frame_start_date = QFrame(self.groupBox_pcm_config)
        self.frame_start_date.setObjectName(u"frame_start_date")
        self.frame_start_date.setFrameShape(QFrame.NoFrame)
        self.frame_start_date.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_start_date)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, 0)
        self.label_start_date = QLabel(self.frame_start_date)
        self.label_start_date.setObjectName(u"label_start_date")

        self.horizontalLayout_13.addWidget(self.label_start_date)

        self.dateEdit_start_date = QDateEdit(self.frame_start_date)
        self.dateEdit_start_date.setObjectName(u"dateEdit_start_date")
        self.dateEdit_start_date.setMaximumDate(QDate(7999, 12, 31))
        self.dateEdit_start_date.setCurrentSection(QDateTimeEdit.MonthSection)
        self.dateEdit_start_date.setDate(QDate(2020, 1, 8))

        self.horizontalLayout_13.addWidget(self.dateEdit_start_date)

        self.btn_info_start_date = QPushButton(self.frame_start_date)
        self.btn_info_start_date.setObjectName(u"btn_info_start_date")
        sizePolicy.setHeightForWidth(self.btn_info_start_date.sizePolicy().hasHeightForWidth())
        self.btn_info_start_date.setSizePolicy(sizePolicy)
        self.btn_info_start_date.setMaximumSize(QSize(40, 16777215))
        self.btn_info_start_date.setIcon(icon)
        self.btn_info_start_date.setIconSize(QSize(40, 40))
        self.btn_info_start_date.setFlat(True)

        self.horizontalLayout_13.addWidget(self.btn_info_start_date)


        self.verticalLayout_2.addWidget(self.frame_start_date)

        self.frame_solver = QFrame(self.groupBox_pcm_config)
        self.frame_solver.setObjectName(u"frame_solver")
        self.frame_solver.setFrameShape(QFrame.NoFrame)
        self.frame_solver.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_solver)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, 0)
        self.label_solver = QLabel(self.frame_solver)
        self.label_solver.setObjectName(u"label_solver")

        self.horizontalLayout_12.addWidget(self.label_solver)

        self.comboBox_solver = QComboBox(self.frame_solver)
        self.comboBox_solver.addItem("")
        self.comboBox_solver.addItem("")
        self.comboBox_solver.addItem("")
        self.comboBox_solver.setObjectName(u"comboBox_solver")

        self.horizontalLayout_12.addWidget(self.comboBox_solver)

        self.btn_info_solver = QPushButton(self.frame_solver)
        self.btn_info_solver.setObjectName(u"btn_info_solver")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_info_solver.sizePolicy().hasHeightForWidth())
        self.btn_info_solver.setSizePolicy(sizePolicy1)
        self.btn_info_solver.setMaximumSize(QSize(40, 16777215))
        self.btn_info_solver.setIcon(icon)
        self.btn_info_solver.setIconSize(QSize(40, 40))
        self.btn_info_solver.setFlat(True)

        self.horizontalLayout_12.addWidget(self.btn_info_solver)


        self.verticalLayout_2.addWidget(self.frame_solver)

        self.frame_mini_gap = QFrame(self.groupBox_pcm_config)
        self.frame_mini_gap.setObjectName(u"frame_mini_gap")
        self.frame_mini_gap.setFrameShape(QFrame.NoFrame)
        self.frame_mini_gap.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_mini_gap)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(12, 0, 12, 0)
        self.label_mini_gap = QLabel(self.frame_mini_gap)
        self.label_mini_gap.setObjectName(u"label_mini_gap")

        self.horizontalLayout_10.addWidget(self.label_mini_gap)

        self.doubleSpin_mini_gap = QDoubleSpinBox(self.frame_mini_gap)
        self.doubleSpin_mini_gap.setObjectName(u"doubleSpin_mini_gap")
        self.doubleSpin_mini_gap.setValue(0.050000000000000)

        self.horizontalLayout_10.addWidget(self.doubleSpin_mini_gap)

        self.btn_info_mipgap = QPushButton(self.frame_mini_gap)
        self.btn_info_mipgap.setObjectName(u"btn_info_mipgap")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_info_mipgap.sizePolicy().hasHeightForWidth())
        self.btn_info_mipgap.setSizePolicy(sizePolicy2)
        self.btn_info_mipgap.setMaximumSize(QSize(40, 16777215))
        self.btn_info_mipgap.setIcon(icon)
        self.btn_info_mipgap.setIconSize(QSize(40, 40))
        self.btn_info_mipgap.setFlat(True)

        self.horizontalLayout_10.addWidget(self.btn_info_mipgap)


        self.verticalLayout_2.addWidget(self.frame_mini_gap)

        self.frame_solve_pricing = QFrame(self.groupBox_pcm_config)
        self.frame_solve_pricing.setObjectName(u"frame_solve_pricing")
        self.frame_solve_pricing.setFrameShape(QFrame.NoFrame)
        self.frame_solve_pricing.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_solve_pricing)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, 0)
        self.label_solve_pricing = QLabel(self.frame_solve_pricing)
        self.label_solve_pricing.setObjectName(u"label_solve_pricing")

        self.horizontalLayout_9.addWidget(self.label_solve_pricing)

        self.radio_solve_pricing_true = QRadioButton(self.frame_solve_pricing)
        self.radio_solve_pricing_true.setObjectName(u"radio_solve_pricing_true")

        self.horizontalLayout_9.addWidget(self.radio_solve_pricing_true)

        self.radio_solve_pricing_false = QRadioButton(self.frame_solve_pricing)
        self.radio_solve_pricing_false.setObjectName(u"radio_solve_pricing_false")
        self.radio_solve_pricing_false.setChecked(True)

        self.horizontalLayout_9.addWidget(self.radio_solve_pricing_false)

        self.btn_info_pricing = QPushButton(self.frame_solve_pricing)
        self.btn_info_pricing.setObjectName(u"btn_info_pricing")
        sizePolicy1.setHeightForWidth(self.btn_info_pricing.sizePolicy().hasHeightForWidth())
        self.btn_info_pricing.setSizePolicy(sizePolicy1)
        self.btn_info_pricing.setMaximumSize(QSize(40, 16777215))
        self.btn_info_pricing.setIcon(icon)
        self.btn_info_pricing.setIconSize(QSize(40, 40))
        self.btn_info_pricing.setFlat(True)

        self.horizontalLayout_9.addWidget(self.btn_info_pricing)


        self.verticalLayout_2.addWidget(self.frame_solve_pricing)

        self.frame_storage_as_mode = QFrame(self.groupBox_pcm_config)
        self.frame_storage_as_mode.setObjectName(u"frame_storage_as_mode")
        self.frame_storage_as_mode.setFrameShape(QFrame.NoFrame)
        self.frame_storage_as_mode.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_storage_as_mode)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.label_storage_mode = QLabel(self.frame_storage_as_mode)
        self.label_storage_mode.setObjectName(u"label_storage_mode")

        self.horizontalLayout_8.addWidget(self.label_storage_mode)

        self.label_storage_mode_true = QRadioButton(self.frame_storage_as_mode)
        self.label_storage_mode_true.setObjectName(u"label_storage_mode_true")

        self.horizontalLayout_8.addWidget(self.label_storage_mode_true)

        self.label_storage_mode_false = QRadioButton(self.frame_storage_as_mode)
        self.label_storage_mode_false.setObjectName(u"label_storage_mode_false")
        self.label_storage_mode_false.setChecked(True)

        self.horizontalLayout_8.addWidget(self.label_storage_mode_false)

        self.btn_info_storage_mode = QPushButton(self.frame_storage_as_mode)
        self.btn_info_storage_mode.setObjectName(u"btn_info_storage_mode")
        sizePolicy1.setHeightForWidth(self.btn_info_storage_mode.sizePolicy().hasHeightForWidth())
        self.btn_info_storage_mode.setSizePolicy(sizePolicy1)
        self.btn_info_storage_mode.setMaximumSize(QSize(40, 16777215))
        self.btn_info_storage_mode.setIcon(icon)
        self.btn_info_storage_mode.setIconSize(QSize(40, 40))
        self.btn_info_storage_mode.setFlat(True)

        self.horizontalLayout_8.addWidget(self.btn_info_storage_mode)


        self.verticalLayout_2.addWidget(self.frame_storage_as_mode)


        self.verticalLayout.addWidget(self.groupBox_pcm_config)

        self.line_seperator = QFrame(PCMConfigPage)
        self.line_seperator.setObjectName(u"line_seperator")
        self.line_seperator.setFrameShape(QFrame.HLine)
        self.line_seperator.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_seperator)

        self.frame_btns = QFrame(PCMConfigPage)
        self.frame_btns.setObjectName(u"frame_btns")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_btns.sizePolicy().hasHeightForWidth())
        self.frame_btns.setSizePolicy(sizePolicy3)
        self.frame_btns.setFrameShape(QFrame.NoFrame)
        self.frame_btns.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_btns)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_save_config = QPushButton(self.frame_btns)
        self.btn_save_config.setObjectName(u"btn_save_config")

        self.horizontalLayout.addWidget(self.btn_save_config)

        self.btn_exit_config = QPushButton(self.frame_btns)
        self.btn_exit_config.setObjectName(u"btn_exit_config")

        self.horizontalLayout.addWidget(self.btn_exit_config)


        self.verticalLayout.addWidget(self.frame_btns)


        self.retranslateUi(PCMConfigPage)

        QMetaObject.connectSlotsByName(PCMConfigPage)
    # setupUi

    def retranslateUi(self, PCMConfigPage):
        PCMConfigPage.setWindowTitle(QCoreApplication.translate("PCMConfigPage", u"Form", None))
        self.groupBox_pcm_config.setTitle(QCoreApplication.translate("PCMConfigPage", u"PCM Parameters", None))
        self.label_pcm_venv.setText(QCoreApplication.translate("PCMConfigPage", u"PCM Venv Path", None))
        self.lineEdit_pcm_venv.setPlaceholderText(QCoreApplication.translate("PCMConfigPage", u"/path/to/pcm_virtual_env/Scripts/python.exe", None))
        self.btn_info_venv.setText("")
        self.label_start_date.setText(QCoreApplication.translate("PCMConfigPage", u"Start Date", None))
        self.dateEdit_start_date.setDisplayFormat(QCoreApplication.translate("PCMConfigPage", u"MM/dd/yyyy", None))
        self.btn_info_start_date.setText("")
        self.label_solver.setText(QCoreApplication.translate("PCMConfigPage", u"Solver", None))
        self.comboBox_solver.setItemText(0, QCoreApplication.translate("PCMConfigPage", u"gurobi", None))
        self.comboBox_solver.setItemText(1, QCoreApplication.translate("PCMConfigPage", u"cplex", None))
        self.comboBox_solver.setItemText(2, QCoreApplication.translate("PCMConfigPage", u"cbc", None))

        self.btn_info_solver.setText("")
        self.label_mini_gap.setText(QCoreApplication.translate("PCMConfigPage", u"Mipgap", None))
        self.btn_info_mipgap.setText("")
        self.label_solve_pricing.setText(QCoreApplication.translate("PCMConfigPage", u"Solve Pricing Problem", None))
        self.radio_solve_pricing_true.setText(QCoreApplication.translate("PCMConfigPage", u"True", None))
        self.radio_solve_pricing_false.setText(QCoreApplication.translate("PCMConfigPage", u"False", None))
        self.btn_info_pricing.setText("")
        self.label_storage_mode.setText(QCoreApplication.translate("PCMConfigPage", u"Storage AS Mode", None))
        self.label_storage_mode_true.setText(QCoreApplication.translate("PCMConfigPage", u"True", None))
        self.label_storage_mode_false.setText(QCoreApplication.translate("PCMConfigPage", u"False", None))
        self.btn_info_storage_mode.setText("")
        self.btn_save_config.setText(QCoreApplication.translate("PCMConfigPage", u"Save Config", None))
        self.btn_exit_config.setText(QCoreApplication.translate("PCMConfigPage", u"Exit Config", None))
    # retranslateUi

