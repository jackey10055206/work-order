# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 933)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(100, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 1891, 841))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.wdg_topContent = QWidget(self.widget)
        self.wdg_topContent.setObjectName(u"wdg_topContent")
        self.wdg_topContent.setMinimumSize(QSize(0, 101))
        self.widget1 = QWidget(self.wdg_topContent)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(10, 10, 1161, 81))
        self.lay_topgrid = QGridLayout(self.widget1)
        self.lay_topgrid.setObjectName(u"lay_topgrid")
        self.lay_topgrid.setContentsMargins(0, 0, 0, 0)
        self.wdg_workNum = QWidget(self.widget1)
        self.wdg_workNum.setObjectName(u"wdg_workNum")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.wdg_workNum.sizePolicy().hasHeightForWidth())
        self.wdg_workNum.setSizePolicy(sizePolicy1)
        self.wdg_workNum.setMinimumSize(QSize(0, 20))
        self.widget2 = QWidget(self.wdg_workNum)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(10, 10, 211, 23))
        self.horizontalLayout = QHBoxLayout(self.widget2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_workNum = QLabel(self.widget2)
        self.lbl_workNum.setObjectName(u"lbl_workNum")

        self.horizontalLayout.addWidget(self.lbl_workNum)

        self.le_worknum = QLineEdit(self.widget2)
        self.le_worknum.setObjectName(u"le_worknum")

        self.horizontalLayout.addWidget(self.le_worknum)


        self.lay_topgrid.addWidget(self.wdg_workNum, 0, 0, 1, 1)

        self.wdg_customerName = QWidget(self.widget1)
        self.wdg_customerName.setObjectName(u"wdg_customerName")
        sizePolicy1.setHeightForWidth(self.wdg_customerName.sizePolicy().hasHeightForWidth())
        self.wdg_customerName.setSizePolicy(sizePolicy1)
        self.wdg_customerName.setMinimumSize(QSize(0, 20))
        self.widget3 = QWidget(self.wdg_customerName)
        self.widget3.setObjectName(u"widget3")
        self.widget3.setGeometry(QRect(0, 10, 221, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.widget3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lbl_customerName = QLabel(self.widget3)
        self.lbl_customerName.setObjectName(u"lbl_customerName")

        self.horizontalLayout_3.addWidget(self.lbl_customerName)

        self.cb_customerName = QComboBox(self.widget3)
        self.cb_customerName.setObjectName(u"cb_customerName")
        self.cb_customerName.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_3.addWidget(self.cb_customerName)


        self.lay_topgrid.addWidget(self.wdg_customerName, 0, 1, 1, 1)

        self.wdg_contactName = QWidget(self.widget1)
        self.wdg_contactName.setObjectName(u"wdg_contactName")
        sizePolicy1.setHeightForWidth(self.wdg_contactName.sizePolicy().hasHeightForWidth())
        self.wdg_contactName.setSizePolicy(sizePolicy1)
        self.wdg_contactName.setMinimumSize(QSize(150, 20))
        self.widget4 = QWidget(self.wdg_contactName)
        self.widget4.setObjectName(u"widget4")
        self.widget4.setGeometry(QRect(0, 10, 451, 23))
        self.horizontalLayout_5 = QHBoxLayout(self.widget4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lbl_contactName = QLabel(self.widget4)
        self.lbl_contactName.setObjectName(u"lbl_contactName")
        self.lbl_contactName.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.lbl_contactName)

        self.le_contactName = QLineEdit(self.widget4)
        self.le_contactName.setObjectName(u"le_contactName")

        self.horizontalLayout_5.addWidget(self.le_contactName)


        self.lay_topgrid.addWidget(self.wdg_contactName, 0, 2, 1, 1)

        self.wdg_startTime = QWidget(self.widget1)
        self.wdg_startTime.setObjectName(u"wdg_startTime")
        sizePolicy1.setHeightForWidth(self.wdg_startTime.sizePolicy().hasHeightForWidth())
        self.wdg_startTime.setSizePolicy(sizePolicy1)
        self.wdg_startTime.setMinimumSize(QSize(150, 20))
        self.widget5 = QWidget(self.wdg_startTime)
        self.widget5.setObjectName(u"widget5")
        self.widget5.setGeometry(QRect(0, 10, 211, 23))
        self.horizontalLayout_7 = QHBoxLayout(self.widget5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lbl_startTime = QLabel(self.widget5)
        self.lbl_startTime.setObjectName(u"lbl_startTime")

        self.horizontalLayout_7.addWidget(self.lbl_startTime)

        self.le_startTime = QLineEdit(self.widget5)
        self.le_startTime.setObjectName(u"le_startTime")

        self.horizontalLayout_7.addWidget(self.le_startTime)


        self.lay_topgrid.addWidget(self.wdg_startTime, 0, 3, 1, 1)

        self.wdg_caseName = QWidget(self.widget1)
        self.wdg_caseName.setObjectName(u"wdg_caseName")
        self.wdg_caseName.setMinimumSize(QSize(0, 20))
        self.widget6 = QWidget(self.wdg_caseName)
        self.widget6.setObjectName(u"widget6")
        self.widget6.setGeometry(QRect(10, 0, 211, 23))
        self.horizontalLayout_2 = QHBoxLayout(self.widget6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lbl_caseName = QLabel(self.widget6)
        self.lbl_caseName.setObjectName(u"lbl_caseName")

        self.horizontalLayout_2.addWidget(self.lbl_caseName)

        self.le_caseName = QLineEdit(self.widget6)
        self.le_caseName.setObjectName(u"le_caseName")

        self.horizontalLayout_2.addWidget(self.le_caseName)


        self.lay_topgrid.addWidget(self.wdg_caseName, 1, 0, 1, 1)

        self.wdg_phone = QWidget(self.widget1)
        self.wdg_phone.setObjectName(u"wdg_phone")
        self.wdg_phone.setMinimumSize(QSize(0, 20))
        self.widget7 = QWidget(self.wdg_phone)
        self.widget7.setObjectName(u"widget7")
        self.widget7.setGeometry(QRect(0, 0, 221, 23))
        self.horizontalLayout_4 = QHBoxLayout(self.widget7)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lbl_phone = QLabel(self.widget7)
        self.lbl_phone.setObjectName(u"lbl_phone")

        self.horizontalLayout_4.addWidget(self.lbl_phone)

        self.le_phone = QLineEdit(self.widget7)
        self.le_phone.setObjectName(u"le_phone")

        self.horizontalLayout_4.addWidget(self.le_phone)


        self.lay_topgrid.addWidget(self.wdg_phone, 1, 1, 1, 1)

        self.wdg_address = QWidget(self.widget1)
        self.wdg_address.setObjectName(u"wdg_address")
        self.wdg_address.setMinimumSize(QSize(150, 20))
        self.widget8 = QWidget(self.wdg_address)
        self.widget8.setObjectName(u"widget8")
        self.widget8.setGeometry(QRect(0, 0, 451, 23))
        self.horizontalLayout_6 = QHBoxLayout(self.widget8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.lbl_address = QLabel(self.widget8)
        self.lbl_address.setObjectName(u"lbl_address")

        self.horizontalLayout_6.addWidget(self.lbl_address)

        self.lle_address = QLineEdit(self.widget8)
        self.lle_address.setObjectName(u"lle_address")
        self.lle_address.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_6.addWidget(self.lle_address)


        self.lay_topgrid.addWidget(self.wdg_address, 1, 2, 1, 1)

        self.wdg_endTime = QWidget(self.widget1)
        self.wdg_endTime.setObjectName(u"wdg_endTime")
        self.wdg_endTime.setMinimumSize(QSize(150, 20))
        self.widget9 = QWidget(self.wdg_endTime)
        self.widget9.setObjectName(u"widget9")
        self.widget9.setGeometry(QRect(0, 0, 211, 23))
        self.horizontalLayout_8 = QHBoxLayout(self.widget9)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.lbl_endTime = QLabel(self.widget9)
        self.lbl_endTime.setObjectName(u"lbl_endTime")

        self.horizontalLayout_8.addWidget(self.lbl_endTime)

        self.le_endTime = QLineEdit(self.widget9)
        self.le_endTime.setObjectName(u"le_endTime")

        self.horizontalLayout_8.addWidget(self.le_endTime)


        self.lay_topgrid.addWidget(self.wdg_endTime, 1, 3, 1, 1)

        self.lay_topgrid.setRowStretch(0, 1)
        self.lay_topgrid.setRowStretch(1, 1)
        self.lay_topgrid.setColumnStretch(0, 1)
        self.lay_topgrid.setColumnStretch(1, 1)
        self.lay_topgrid.setColumnStretch(2, 2)
        self.lay_topgrid.setColumnStretch(3, 1)

        self.verticalLayout_2.addWidget(self.wdg_topContent)

        self.wdg_lineItems = QWidget(self.widget)
        self.wdg_lineItems.setObjectName(u"wdg_lineItems")
        sizePolicy1.setHeightForWidth(self.wdg_lineItems.sizePolicy().hasHeightForWidth())
        self.wdg_lineItems.setSizePolicy(sizePolicy1)
        self.wdg_lineItems.setMinimumSize(QSize(0, 550))
        self.verticalLayout = QVBoxLayout(self.wdg_lineItems)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tbl_lineItems = QTableWidget(self.wdg_lineItems)
        if (self.tbl_lineItems.columnCount() < 14):
            self.tbl_lineItems.setColumnCount(14)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(12, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tbl_lineItems.setHorizontalHeaderItem(13, __qtablewidgetitem13)
        if (self.tbl_lineItems.rowCount() < 15):
            self.tbl_lineItems.setRowCount(15)
        self.tbl_lineItems.setObjectName(u"tbl_lineItems")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tbl_lineItems.sizePolicy().hasHeightForWidth())
        self.tbl_lineItems.setSizePolicy(sizePolicy2)
        self.tbl_lineItems.setMinimumSize(QSize(0, 400))
        self.tbl_lineItems.setRowCount(15)
        self.tbl_lineItems.setColumnCount(14)
        self.tbl_lineItems.horizontalHeader().setCascadingSectionResizes(False)
        self.tbl_lineItems.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tbl_lineItems.horizontalHeader().setStretchLastSection(False)
        self.tbl_lineItems.verticalHeader().setVisible(False)
        self.tbl_lineItems.verticalHeader().setCascadingSectionResizes(False)
        self.tbl_lineItems.verticalHeader().setProperty(u"showSortIndicator", False)
        self.tbl_lineItems.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tbl_lineItems)


        self.verticalLayout_2.addWidget(self.wdg_lineItems)

        self.wdg_bottomSection = QWidget(self.widget)
        self.wdg_bottomSection.setObjectName(u"wdg_bottomSection")
        self.wdg_bottomSection.setMinimumSize(QSize(0, 200))
        self.widget10 = QWidget(self.wdg_bottomSection)
        self.widget10.setObjectName(u"widget10")
        self.widget10.setGeometry(QRect(30, -20, 1481, 321))
        self.horizontalLayout_17 = QHBoxLayout(self.widget10)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.grp_remark = QGroupBox(self.widget10)
        self.grp_remark.setObjectName(u"grp_remark")
        self.horizontalLayout_9 = QHBoxLayout(self.grp_remark)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.te_remark = QTextEdit(self.grp_remark)
        self.te_remark.setObjectName(u"te_remark")

        self.horizontalLayout_9.addWidget(self.te_remark)


        self.horizontalLayout_17.addWidget(self.grp_remark)

        self.wdg_summaryActions = QWidget(self.widget10)
        self.wdg_summaryActions.setObjectName(u"wdg_summaryActions")
        self.wdg_summaryActions.setMinimumSize(QSize(791, 0))
        self.wdg_amountSummary = QWidget(self.wdg_summaryActions)
        self.wdg_amountSummary.setObjectName(u"wdg_amountSummary")
        self.wdg_amountSummary.setGeometry(QRect(10, 10, 871, 61))
        self.horizontalLayout_13 = QHBoxLayout(self.wdg_amountSummary)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.wdg_productionAmountField = QWidget(self.wdg_amountSummary)
        self.wdg_productionAmountField.setObjectName(u"wdg_productionAmountField")
        self.widget11 = QWidget(self.wdg_productionAmountField)
        self.widget11.setObjectName(u"widget11")
        self.widget11.setGeometry(QRect(10, 10, 187, 23))
        self.horizontalLayout_10 = QHBoxLayout(self.widget11)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.lbl_productionAmount = QLabel(self.widget11)
        self.lbl_productionAmount.setObjectName(u"lbl_productionAmount")

        self.horizontalLayout_10.addWidget(self.lbl_productionAmount)

        self.le_productionAmount = QLineEdit(self.widget11)
        self.le_productionAmount.setObjectName(u"le_productionAmount")

        self.horizontalLayout_10.addWidget(self.le_productionAmount)


        self.horizontalLayout_13.addWidget(self.wdg_productionAmountField)

        self.wdg_taxAmountField = QWidget(self.wdg_amountSummary)
        self.wdg_taxAmountField.setObjectName(u"wdg_taxAmountField")
        self.widget12 = QWidget(self.wdg_taxAmountField)
        self.widget12.setObjectName(u"widget12")
        self.widget12.setGeometry(QRect(10, 10, 161, 23))
        self.horizontalLayout_11 = QHBoxLayout(self.widget12)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.lbl_taxAmount = QLabel(self.widget12)
        self.lbl_taxAmount.setObjectName(u"lbl_taxAmount")

        self.horizontalLayout_11.addWidget(self.lbl_taxAmount)

        self.le_taxAmount = QLineEdit(self.widget12)
        self.le_taxAmount.setObjectName(u"le_taxAmount")

        self.horizontalLayout_11.addWidget(self.le_taxAmount)


        self.horizontalLayout_13.addWidget(self.wdg_taxAmountField)

        self.wdg_totalAmountField = QWidget(self.wdg_amountSummary)
        self.wdg_totalAmountField.setObjectName(u"wdg_totalAmountField")
        self.widget13 = QWidget(self.wdg_totalAmountField)
        self.widget13.setObjectName(u"widget13")
        self.widget13.setGeometry(QRect(10, 10, 161, 23))
        self.horizontalLayout_12 = QHBoxLayout(self.widget13)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.lbl_totalAmount = QLabel(self.widget13)
        self.lbl_totalAmount.setObjectName(u"lbl_totalAmount")

        self.horizontalLayout_12.addWidget(self.lbl_totalAmount)

        self.le_totalAmount = QLineEdit(self.widget13)
        self.le_totalAmount.setObjectName(u"le_totalAmount")

        self.horizontalLayout_12.addWidget(self.le_totalAmount)


        self.horizontalLayout_13.addWidget(self.wdg_totalAmountField)

        self.wdg_actionButtons = QWidget(self.wdg_summaryActions)
        self.wdg_actionButtons.setObjectName(u"wdg_actionButtons")
        self.wdg_actionButtons.setGeometry(QRect(10, 70, 791, 80))
        self.widget14 = QWidget(self.wdg_actionButtons)
        self.widget14.setObjectName(u"widget14")
        self.widget14.setGeometry(QRect(10, 10, 744, 78))
        self.verticalLayout_3 = QVBoxLayout(self.widget14)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.btn_open = QPushButton(self.widget14)
        self.btn_open.setObjectName(u"btn_open")

        self.horizontalLayout_14.addWidget(self.btn_open)

        self.btn_save = QPushButton(self.widget14)
        self.btn_save.setObjectName(u"btn_save")

        self.horizontalLayout_14.addWidget(self.btn_save)

        self.btn_reset = QPushButton(self.widget14)
        self.btn_reset.setObjectName(u"btn_reset")

        self.horizontalLayout_14.addWidget(self.btn_reset)

        self.btn_billing = QPushButton(self.widget14)
        self.btn_billing.setObjectName(u"btn_billing")

        self.horizontalLayout_14.addWidget(self.btn_billing)

        self.btn_subtotal = QPushButton(self.widget14)
        self.btn_subtotal.setObjectName(u"btn_subtotal")

        self.horizontalLayout_14.addWidget(self.btn_subtotal)

        self.btn_calcuate = QPushButton(self.widget14)
        self.btn_calcuate.setObjectName(u"btn_calcuate")

        self.horizontalLayout_14.addWidget(self.btn_calcuate)


        self.verticalLayout_3.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.btn_import = QPushButton(self.widget14)
        self.btn_import.setObjectName(u"btn_import")
        self.btn_import.setMinimumSize(QSize(125, 0))

        self.horizontalLayout_15.addWidget(self.btn_import)

        self.btn_invoice = QPushButton(self.widget14)
        self.btn_invoice.setObjectName(u"btn_invoice")
        self.btn_invoice.setMinimumSize(QSize(125, 0))

        self.horizontalLayout_15.addWidget(self.btn_invoice)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_15)

        self.horizontalSpacer = QSpacerItem(478, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)


        self.horizontalLayout_17.addWidget(self.wdg_summaryActions)


        self.verticalLayout_2.addWidget(self.wdg_bottomSection)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 30))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.lbl_workNum.setText(QCoreApplication.translate("MainWindow", u"\u5de5\u55ae\u7de8\u865f:", None))
        self.lbl_customerName.setText(QCoreApplication.translate("MainWindow", u"\u5ba2\u6236\u540d\u7a31:", None))
        self.lbl_contactName.setText(QCoreApplication.translate("MainWindow", u"\u806f\u7d61\u4eba:", None))
        self.lbl_startTime.setText(QCoreApplication.translate("MainWindow", u"\u9032\u5834\u6642\u9593:", None))
        self.lbl_caseName.setText(QCoreApplication.translate("MainWindow", u"\u6848\u4ef6\u540d\u7a31:", None))
        self.lbl_phone.setText(QCoreApplication.translate("MainWindow", u"\u96fb\u8a71:", None))
        self.lbl_address.setText(QCoreApplication.translate("MainWindow", u"\u5730\u5740:", None))
        self.lbl_endTime.setText(QCoreApplication.translate("MainWindow", u"\u64a4\u5834\u6642\u9593:", None))
        ___qtablewidgetitem = self.tbl_lineItems.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u88fd\u4f5c\u9805\u76ee", None))
        ___qtablewidgetitem1 = self.tbl_lineItems.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u5bec\u5ea6", None))
        ___qtablewidgetitem2 = self.tbl_lineItems.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u9577\u5ea6", None))
        ___qtablewidgetitem3 = self.tbl_lineItems.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u6578\u91cf", None))
        ___qtablewidgetitem4 = self.tbl_lineItems.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u6750\u8cea", None))
        ___qtablewidgetitem5 = self.tbl_lineItems.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u51b7\u9336\u52a0\u5de5", None))
        ___qtablewidgetitem6 = self.tbl_lineItems.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u677f\u6750\u7a2e\u985e", None))
        ___qtablewidgetitem7 = self.tbl_lineItems.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u677f\u6750\u539a\u5ea6", None))
        ___qtablewidgetitem8 = self.tbl_lineItems.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u5176\u4ed6\u5099\u6599", None))
        ___qtablewidgetitem9 = self.tbl_lineItems.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u6578\u91cf", None))
        ___qtablewidgetitem10 = self.tbl_lineItems.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"\u624d\u6578", None))
        ___qtablewidgetitem11 = self.tbl_lineItems.horizontalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"\u55ae\u50f9", None))
        ___qtablewidgetitem12 = self.tbl_lineItems.horizontalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"\u8a08\u50f9", None))
        ___qtablewidgetitem13 = self.tbl_lineItems.horizontalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"\u5099\u6599\u8a08\u50f9", None))
        self.grp_remark.setTitle(QCoreApplication.translate("MainWindow", u"\u5099\u8a3b", None))
        self.lbl_productionAmount.setText(QCoreApplication.translate("MainWindow", u"\u88fd\u4f5c\u91d1\u984d", None))
        self.lbl_taxAmount.setText(QCoreApplication.translate("MainWindow", u"\u7a05\u984d", None))
        self.lbl_totalAmount.setText(QCoreApplication.translate("MainWindow", u"\u7e3d\u8a08", None))
        self.btn_open.setText(QCoreApplication.translate("MainWindow", u"\u958b\u555f", None))
        self.btn_save.setText(QCoreApplication.translate("MainWindow", u"\u5132\u5b58", None))
        self.btn_reset.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e", None))
        self.btn_billing.setText(QCoreApplication.translate("MainWindow", u"\u8acb\u6b3e", None))
        self.btn_subtotal.setText(QCoreApplication.translate("MainWindow", u"\u5c0f\u8a08", None))
        self.btn_calcuate.setText(QCoreApplication.translate("MainWindow", u"\u8a08\u7b97", None))
        self.btn_import.setText(QCoreApplication.translate("MainWindow", u"\u5c0e\u5165", None))
        self.btn_invoice.setText(QCoreApplication.translate("MainWindow", u"\u958b\u7968", None))
    # retranslateUi

