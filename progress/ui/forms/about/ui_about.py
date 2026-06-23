# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_AboutPage(object):
    def setupUi(self, AboutPage):
        if not AboutPage.objectName():
            AboutPage.setObjectName(u"AboutPage")
        AboutPage.resize(1183, 928)
        self.verticalLayout = QVBoxLayout(AboutPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.text_browser = QTextBrowser(AboutPage)
        self.text_browser.setObjectName(u"text_browser")

        self.verticalLayout.addWidget(self.text_browser)


        self.retranslateUi(AboutPage)

        QMetaObject.connectSlotsByName(AboutPage)
    # setupUi

    def retranslateUi(self, AboutPage):
        AboutPage.setWindowTitle(QCoreApplication.translate("AboutPage", u"Form", None))
    # retranslateUi

