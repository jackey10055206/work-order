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
        
        self.comboBox_employee_1.addItems(employee_name())
        self.comboBox_employee_2.addItems(employee_name())
        self.comboBox_employee_3.addItems(employee_name())
        self.comboBox_employee_4.addItems(employee_name())
        self.comboBox_employee_5.addItems(employee_name())
                
        self.comboBox_pack.addItems(pack_name())
        self.comboBox_transport.addItems(transport_name())

        self.comboBox_product_1.addItems(product_name())
        self.comboBox_product_2.addItems(product_name())
        self.comboBox_product_3.addItems(product_name())
        self.comboBox_product_4.addItems(product_name())
        self.comboBox_product_5.addItems(product_name())
        self.comboBox_product_6.addItems(product_name())
        self.comboBox_product_7.addItems(product_name())
        self.comboBox_product_8.addItems(product_name())
        self.comboBox_product_9.addItems(product_name())
        self.comboBox_product_10.addItems(product_name())
        self.comboBox_product_11.addItems(product_name())
        self.comboBox_product_12.addItems(product_name())
        self.comboBox_product_13.addItems(product_name())
        self.comboBox_product_14.addItems(product_name())
        self.comboBox_product_15.addItems(product_name())

        self.comboBox_material_1.addItems(material_name())
        self.comboBox_material_2.addItems(material_name())
        self.comboBox_material_3.addItems(material_name())
        self.comboBox_material_4.addItems(material_name())
        self.comboBox_material_5.addItems(material_name())
        self.comboBox_material_6.addItems(material_name())
        self.comboBox_material_7.addItems(material_name())
        self.comboBox_material_8.addItems(material_name())
        self.comboBox_material_9.addItems(material_name())
        self.comboBox_material_10.addItems(material_name())
        self.comboBox_material_11.addItems(material_name())
        self.comboBox_material_12.addItems(material_name())
        self.comboBox_material_13.addItems(material_name())
        self.comboBox_material_14.addItems(material_name())
        self.comboBox_material_15.addItems(material_name())

        self.comboBox_process_1.addItems(process_name())
        self.comboBox_process_2.addItems(process_name())
        self.comboBox_process_3.addItems(process_name())
        self.comboBox_process_4.addItems(process_name())
        self.comboBox_process_5.addItems(process_name())
        self.comboBox_process_6.addItems(process_name())
        self.comboBox_process_7.addItems(process_name())
        self.comboBox_process_8.addItems(process_name())
        self.comboBox_process_9.addItems(process_name())
        self.comboBox_process_10.addItems(process_name())
        self.comboBox_process_11.addItems(process_name())
        self.comboBox_process_12.addItems(process_name())
        self.comboBox_process_13.addItems(process_name())
        self.comboBox_process_14.addItems(process_name())
        self.comboBox_process_15.addItems(process_name())

        self.comboBox_plate_1.addItems(plate_name())
        self.comboBox_plate_2.addItems(plate_name())
        self.comboBox_plate_3.addItems(plate_name())
        self.comboBox_plate_4.addItems(plate_name())
        self.comboBox_plate_5.addItems(plate_name())
        self.comboBox_plate_6.addItems(plate_name())
        self.comboBox_plate_7.addItems(plate_name())
        self.comboBox_plate_8.addItems(plate_name())
        self.comboBox_plate_9.addItems(plate_name())
        self.comboBox_plate_10.addItems(plate_name())
        self.comboBox_plate_11.addItems(plate_name())
        self.comboBox_plate_12.addItems(plate_name())
        self.comboBox_plate_13.addItems(plate_name())
        self.comboBox_plate_14.addItems(plate_name())
        self.comboBox_plate_15.addItems(plate_name())

        self.comboBox_thicknes_1.addItems(thickness_name())
        self.comboBox_thicknes_2.addItems(thickness_name())
        self.comboBox_thicknes_3.addItems(thickness_name())
        self.comboBox_thicknes_4.addItems(thickness_name())
        self.comboBox_thicknes_5.addItems(thickness_name())
        self.comboBox_thicknes_6.addItems(thickness_name())
        self.comboBox_thicknes_7.addItems(thickness_name())
        self.comboBox_thicknes_8.addItems(thickness_name())
        self.comboBox_thicknes_9.addItems(thickness_name())
        self.comboBox_thicknes_10.addItems(thickness_name())
        self.comboBox_thicknes_11.addItems(thickness_name())
        self.comboBox_thicknes_12.addItems(thickness_name())
        self.comboBox_thicknes_13.addItems(thickness_name())
        self.comboBox_thicknes_14.addItems(thickness_name())
        self.comboBox_thicknes_15.addItems(thickness_name())

        self.comboBox_others_1.addItems(others_name())
        self.comboBox_others_2.addItems(others_name())
        self.comboBox_others_3.addItems(others_name())
        self.comboBox_others_4.addItems(others_name())
        self.comboBox_others_5.addItems(others_name())
        self.comboBox_others_6.addItems(others_name())
        self.comboBox_others_7.addItems(others_name())
        self.comboBox_others_8.addItems(others_name())
        self.comboBox_others_9.addItems(others_name())
        self.comboBox_others_10.addItems(others_name())
        self.comboBox_others_11.addItems(others_name())
        self.comboBox_others_12.addItems(others_name())
        self.comboBox_others_13.addItems(others_name())
        self.comboBox_others_14.addItems(others_name())
        self.comboBox_others_15.addItems(others_name())

        def cal_CBM():
            width = self.lineEdit_width_1.text()
            height = self.lineEdit_height_1.text()
            CBM=math.ceil(int(width)*int(height)/900)
            self.lineEdit_CBM_1.setText(str(CBM))
            
            
        self.lineEdit_height_1.editingFinished.connect(cal_CBM)
            

        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())