from decimal import ROUND_HALF_UP, Decimal
import sys

from unittest import result
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
import numpy as np
# import openpyxl

connection = pymysql.connect(host='192.168.1.2',
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

        ###增加下拉式選單客戶
        self.comboBox_company_name.addItems(company_name())

        def index_change():
            full_name,phone,address,taxID = company_name_change(self.comboBox_company_name.currentText())
            #print(full_name,phone,address,taxID)
            self.lineEdit_phone.setText(phone)
        self.comboBox_company_name.currentIndexChanged.connect(index_change)

        ###增加下拉式選單工作人員
        for i in range(1,6):
            exec("self.comboBox_employee_"+str(i)+".addItems(employee_name())")
                
        self.comboBox_pack.addItems(pack_name())
        self.comboBox_transport.addItems(transport_name())

        ###增加下拉式選單中間大表
        for i in range(1,16):
            exec("self.comboBox_product_"+str(i)+".addItems(product_name())")
            exec("self.comboBox_material_"+str(i)+".addItems(material_name())")
            exec("self.comboBox_process_"+str(i)+".addItems(process_name())")
            exec("self.comboBox_plate_"+str(i)+".addItems(plate_name())")
            exec("self.comboBox_thicknes_"+str(i)+".addItems(thickness_name())")
            exec("self.comboBox_others_"+str(i)+".addItems(others_name())")
        
    
        ###點擊"小記" 算出價錢   
        def cal_price(self):
            for i in range(1,16):
                exec("width = self.lineEdit_width_"+str(i)+".text()")
                exec("if width == '': width = '0'")
                exec("height = self.lineEdit_height_"+str(i)+".text()")
                exec("if height == '': height = '0'")
                exec("CBM1 = math.ceil(int(width) * int(height) / 900)")
                exec("if CBM1 == 0: CBM1 = ''")
                exec("self.lineEdit_CBM_"+str(i)+".setText(str(CBM1))")
                exec("amount = self.lineEdit_amount_"+str(i)+".text()")
                exec("if amount == '': amount = '1'")
                exec("CBM= self.lineEdit_CBM_"+str(i)+".text()")
                exec("if CBM == '': CBM = '0'")
                exec("CBMprice= self.lineEdit_CBMprice_"+str(i)+".text()")
                exec("if CBMprice == '': CBMprice = '0'")
                exec("result = int(amount)*int(CBM)*int(CBMprice)")
                exec("if result == 0: result = '' ")
                exec("self.lineEdit_single_price_"+str(i)+".setText(str(result))")
        self.pushButton_cal.clicked.connect(lambda:cal_price(self))

        ###點擊"計算"，算出總價
        def cal_final_price(self):
            final_price = []
            for i in range(1,31):
                exec("single_price = self.lineEdit_single_price_"+str(i)+".text()")
                exec("if single_price == '':single_price = '0'")
                exec("final_price.append(single_price)")               
            final_price = list(map(int,final_price))
            result = sum(final_price)
            
            tax = result*0.05
            tax = 0.55
            print(tax)
            tax = int(tax+0.5)
            #tax = np.round(tax)
            print(tax)
            # tax = round(tax,0)
            # print(tax)
            answer = result + tax
            self.lineEdit_tmpprice.setText(str(result))
            self.lineEdit_tax.setText(str(tax))
            self.lineEdit_final_price.setText(str(answer))
        self.pushButton_finalcal.clicked.connect(lambda:cal_final_price(self))
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())