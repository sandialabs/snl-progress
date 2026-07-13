# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_SettingsPage(object):
    def setupUi(self, SettingsPage):
        if not SettingsPage.objectName():
            SettingsPage.setObjectName(u"SettingsPage")
        SettingsPage.resize(590, 641)
        self.verticalLayout = QVBoxLayout(SettingsPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.line_seperator_1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.line_seperator_1)

        self.groupBox = QGroupBox(SettingsPage)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_theme = QFrame(self.groupBox)
        self.frame_theme.setObjectName(u"frame_theme")
        self.frame_theme.setFrameShape(QFrame.NoFrame)
        self.frame_theme.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_theme)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_theme = QLabel(self.frame_theme)
        self.label_theme.setObjectName(u"label_theme")

        self.horizontalLayout.addWidget(self.label_theme)

        self.comboBox_theme = QComboBox(self.frame_theme)
        self.comboBox_theme.addItem("")
        self.comboBox_theme.addItem("")
        self.comboBox_theme.setObjectName(u"comboBox_theme")

        self.horizontalLayout.addWidget(self.comboBox_theme)


        self.verticalLayout_2.addWidget(self.frame_theme)


        self.verticalLayout.addWidget(self.groupBox)

        self.line_seperator_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.line_seperator_2)


        self.retranslateUi(SettingsPage)

        QMetaObject.connectSlotsByName(SettingsPage)
    # setupUi

    def retranslateUi(self, SettingsPage):
        SettingsPage.setWindowTitle(QCoreApplication.translate("SettingsPage", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsPage", u"ProGRESS Settings", None))
        self.label_theme.setText(QCoreApplication.translate("SettingsPage", u"Toggle Theme", None))
        self.comboBox_theme.setItemText(0, QCoreApplication.translate("SettingsPage", u"Light", None))
        self.comboBox_theme.setItemText(1, QCoreApplication.translate("SettingsPage", u"Dark", None))

    # retranslateUi

