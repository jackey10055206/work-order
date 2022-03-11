from audioop import add
import sys
from venv import create
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tkinter import *
from sql import *

import sql
import project as ui
import pymysql


# import openpyxl

connection = pymysql.connect(host='192.168.101.59',
                             port=3306,
                             user='root',
                             passwd='root',
                             database='work_order',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
#print(bool(connection))
cursor = connection.cursor()



class Main(QMainWindow, ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.comboBox_company_name.addItems(company_name())
        
        def index_change():
            full_name,phone,address,taxID = company_name_change(self.comboBox_company_name.currentText())
            #print(full_name,phone,address,taxID)
            self.lineEdit_phone.setText(phone)
        self.comboBox_company_name.currentIndexChanged.connect(index_change)
        
        self.comboBox_employee_1.addItems(employee_name())
        self.comboBox_employee_2.addItems(employee_name())
        self.comboBox_employee_3.addItems(employee_name())
        self.comboBox_employee_4.addItems(employee_name())
        self.comboBox_employee_5.addItems(employee_name())
        
        self.comboBox_pack.addItems(pack_name())
        self.comboBox_transport.addItems(transport_name())

        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())