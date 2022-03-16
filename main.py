from asyncio.windows_events import NULL
import sys
from this import s
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tkinter import *
from sql import *

import sql
import project as ui
import pymysql
import math

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

        
        for i in range(1,6):
            exec("self.comboBox_employee_"+str(i)+".addItems(employee_name())")
                
        self.comboBox_pack.addItems(pack_name())
        self.comboBox_transport.addItems(transport_name())

        for i in range(1,16):
            exec("self.comboBox_product_"+str(i)+".addItems(product_name())")
            exec("self.comboBox_material_"+str(i)+".addItems(material_name())")
            exec("self.comboBox_process_"+str(i)+".addItems(process_name())")
            exec("self.comboBox_plate_"+str(i)+".addItems(plate_name())")
            exec("self.comboBox_thicknes_"+str(i)+".addItems(thickness_name())")
            exec("self.comboBox_others_"+str(i)+".addItems(others_name())")
            
        # def cal_CBM(i):
        #     width = exec("self.lineEdit_width_"+str(i)+".text()")
        #     height = exec("self.lineEdit_height_"+str(i)+".text()")
        #     CBM=math.ceil(int(width)*int(height)/900)
        #     exec("self.lineEdit_CBM_"+str(i)+".setText(str(CBM))")
        #     exec("self.lineEdit_CBM_"+str(i)+".setText(CBM)")
        
        def cal_CBM(tmp):
            print(tmp)
        
        for i in range(1,16):    
            exec("self.lineEdit_height_"+str(i)+".editingFinished.connect(lambda:cal_CBM(i))")
            
        
    
            

        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())