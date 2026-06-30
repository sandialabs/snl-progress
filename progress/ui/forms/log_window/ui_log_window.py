# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_window.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QPlainTextEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_LogPage(object):
    def setupUi(self, LogPage):
        if not LogPage.objectName():
            LogPage.setObjectName(u"LogPage")
        LogPage.resize(1163, 908)
        self.verticalLayout = QVBoxLayout(LogPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_main = QFrame(LogPage)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_main)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.log_window = QPlainTextEdit(self.frame_main)
        self.log_window.setObjectName(u"log_window")
        self.log_window.setMinimumSize(QSize(500, 400))
        self.log_window.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.log_window)


        self.verticalLayout.addWidget(self.frame_main)


        self.retranslateUi(LogPage)

        QMetaObject.connectSlotsByName(LogPage)
    # setupUi

    def retranslateUi(self, LogPage):
        LogPage.setWindowTitle(QCoreApplication.translate("LogPage", u"Form", None))
        self.log_window.setDocumentTitle(QCoreApplication.translate("LogPage", u"Progress Logs", None))
    # retranslateUi

