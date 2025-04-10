# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'results_viewerggbxQm.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)
import progress.resources_rc

class Ui_results_widget(object):
    def setupUi(self, results_widget):
        if not results_widget.objectName():
            results_widget.setObjectName(u"results_widget")
        results_widget.resize(1062, 695)
        results_widget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(results_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.frame = QFrame(results_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(230, 0))
        self.frame.setMaximumSize(QSize(230, 16777215))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.frame)

        self.file_min = QPushButton(results_widget)
        self.file_min.setObjectName(u"file_min")
        icon = QIcon()
        icon.addFile(u":/icons/Images/icons/more_vert_24dp_666666_FILL0_wght200_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.file_min.setIcon(icon)
        self.file_min.setIconSize(QSize(16, 24))
        self.file_min.setFlat(True)

        self.horizontalLayout.addWidget(self.file_min)

        self.frame_2 = QFrame(results_widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.frame_2)

        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(results_widget)

        QMetaObject.connectSlotsByName(results_widget)
    # setupUi

    def retranslateUi(self, results_widget):
        results_widget.setWindowTitle(QCoreApplication.translate("results_widget", u"Form", None))
        self.file_min.setText("")
    # retranslateUi

