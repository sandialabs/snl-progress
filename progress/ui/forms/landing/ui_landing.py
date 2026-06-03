# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'landing.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_LandingPage(object):
    def setupUi(self, LandingPage):
        if not LandingPage.objectName():
            LandingPage.setObjectName(u"LandingPage")
        LandingPage.resize(1122, 928)
        self.mainLayout = QVBoxLayout(LandingPage)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.hero_card = QFrame(LandingPage)
        self.hero_card.setObjectName(u"hero_card")
        self.heroLayout = QVBoxLayout(self.hero_card)
        self.heroLayout.setObjectName(u"heroLayout")
        self.hero_logo_label = QLabel(self.hero_card)
        self.hero_logo_label.setObjectName(u"hero_logo_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hero_logo_label.sizePolicy().hasHeightForWidth())
        self.hero_logo_label.setSizePolicy(sizePolicy)
        self.hero_logo_label.setMinimumSize(QSize(1098, 400))
        self.hero_logo_label.setMaximumSize(QSize(16777215, 400))
        self.hero_logo_label.setPixmap(QPixmap(u":/logos/Images/logos/progress_transparent_alt.png"))
        self.hero_logo_label.setScaledContents(False)
        self.hero_logo_label.setAlignment(Qt.AlignCenter)
        self.hero_logo_label.setWordWrap(False)
        self.hero_logo_label.setMargin(-30)

        self.heroLayout.addWidget(self.hero_logo_label)

        self.title_label = QLabel(self.hero_card)
        self.title_label.setObjectName(u"title_label")
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(45, 105, 46, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(127, 127, 127, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        self.title_label.setPalette(palette)
        font = QFont()
        font.setPointSize(60)
        font.setBold(False)
        font.setKerning(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWordWrap(True)

        self.heroLayout.addWidget(self.title_label)

        self.verticalSpacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.heroLayout.addItem(self.verticalSpacer)

        self.actionLayout = QHBoxLayout()
        self.actionLayout.setObjectName(u"actionLayout")
        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.actionLayout.addItem(self.spacerItem)

        self.get_started_button = QPushButton(self.hero_card)
        self.get_started_button.setObjectName(u"get_started_button")

        self.actionLayout.addWidget(self.get_started_button)

        self.documentation_button = QPushButton(self.hero_card)
        self.documentation_button.setObjectName(u"documentation_button")

        self.actionLayout.addWidget(self.documentation_button)

        self.spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.actionLayout.addItem(self.spacerItem1)


        self.heroLayout.addLayout(self.actionLayout)


        self.mainLayout.addWidget(self.hero_card)

        self.acknowledgement_card = QFrame(LandingPage)
        self.acknowledgement_card.setObjectName(u"acknowledgement_card")
        self.ackLayout = QVBoxLayout(self.acknowledgement_card)
        self.ackLayout.setObjectName(u"ackLayout")
        self.ack_title = QLabel(self.acknowledgement_card)
        self.ack_title.setObjectName(u"ack_title")
        sizePolicy.setHeightForWidth(self.ack_title.sizePolicy().hasHeightForWidth())
        self.ack_title.setSizePolicy(sizePolicy)
        self.ack_title.setMinimumSize(QSize(0, 50))
        self.ack_title.setMaximumSize(QSize(16777215, 50))
        self.ack_title.setAlignment(Qt.AlignCenter)

        self.ackLayout.addWidget(self.ack_title)

        self.ack_text = QLabel(self.acknowledgement_card)
        self.ack_text.setObjectName(u"ack_text")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ack_text.sizePolicy().hasHeightForWidth())
        self.ack_text.setSizePolicy(sizePolicy1)
        self.ack_text.setMinimumSize(QSize(0, 100))
        self.ack_text.setMaximumSize(QSize(16777215, 50))
        font1 = QFont()
        font1.setBold(True)
        self.ack_text.setFont(font1)
        self.ack_text.setAlignment(Qt.AlignCenter)
        self.ack_text.setWordWrap(True)
        self.ack_text.setMargin(0)

        self.ackLayout.addWidget(self.ack_text)


        self.mainLayout.addWidget(self.acknowledgement_card)

        self.footer_frame = QFrame(LandingPage)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footerLayout = QHBoxLayout(self.footer_frame)
        self.footerLayout.setObjectName(u"footerLayout")
        self.spacerItem2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footerLayout.addItem(self.spacerItem2)

        self.sandia_logo_label = QLabel(self.footer_frame)
        self.sandia_logo_label.setObjectName(u"sandia_logo_label")
        self.sandia_logo_label.setMinimumSize(QSize(80, 40))
        self.sandia_logo_label.setMaximumSize(QSize(160, 64))
        self.sandia_logo_label.setPixmap(QPixmap(u":/logos/Images/logos/Quest_Logo_RGB.png"))
        self.sandia_logo_label.setScaledContents(True)
        self.sandia_logo_label.setAlignment(Qt.AlignCenter)

        self.footerLayout.addWidget(self.sandia_logo_label)

        self.spacerItem3 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footerLayout.addItem(self.spacerItem3)

        self.doe_logo_label = QLabel(self.footer_frame)
        self.doe_logo_label.setObjectName(u"doe_logo_label")
        sizePolicy.setHeightForWidth(self.doe_logo_label.sizePolicy().hasHeightForWidth())
        self.doe_logo_label.setSizePolicy(sizePolicy)
        self.doe_logo_label.setMinimumSize(QSize(150, 150))
        self.doe_logo_label.setMaximumSize(QSize(120, 135))
        self.doe_logo_label.setPixmap(QPixmap(u":/logos/Images/logos/DOE_transparent.png"))
        self.doe_logo_label.setScaledContents(True)
        self.doe_logo_label.setAlignment(Qt.AlignCenter)

        self.footerLayout.addWidget(self.doe_logo_label)

        self.spacerItem4 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footerLayout.addItem(self.spacerItem4)

        self.quest_logo_label = QLabel(self.footer_frame)
        self.quest_logo_label.setObjectName(u"quest_logo_label")
        self.quest_logo_label.setMinimumSize(QSize(80, 40))
        self.quest_logo_label.setMaximumSize(QSize(180, 100))
        self.quest_logo_label.setPixmap(QPixmap(u":/logos/Images/logos/SNL_logo.png"))
        self.quest_logo_label.setScaledContents(True)
        self.quest_logo_label.setAlignment(Qt.AlignCenter)

        self.footerLayout.addWidget(self.quest_logo_label)

        self.spacerItem5 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footerLayout.addItem(self.spacerItem5)


        self.mainLayout.addWidget(self.footer_frame)


        self.retranslateUi(LandingPage)

        QMetaObject.connectSlotsByName(LandingPage)
    # setupUi

    def retranslateUi(self, LandingPage):
        self.hero_logo_label.setText("")
        self.title_label.setText(QCoreApplication.translate("LandingPage", u"Probabilistic Grid Reliability Analysis with Energy Storage Systems", None))
        self.get_started_button.setText(QCoreApplication.translate("LandingPage", u"Get Started", None))
        self.documentation_button.setText(QCoreApplication.translate("LandingPage", u"Documentation", None))
        self.ack_title.setText(QCoreApplication.translate("LandingPage", u"A Python-based open-source tool for assessing the resource adequacy of the evolving electric power grid integrated with energy storage systems.", None))
        self.ack_text.setText(QCoreApplication.translate("LandingPage", u"Acknowledgement: This material is based upon work supported by the U.S. Department of Energy Office of Electricity, Energy Storage Division.", None))
        self.sandia_logo_label.setText("")
        self.doe_logo_label.setText("")
        self.quest_logo_label.setText("")
        pass
    # retranslateUi

