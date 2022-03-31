from asyncio.windows_events import NULL
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
            print(tax)
            answer = result + tax
            self.lineEdit_tmpprice.setText(str(result))
            self.lineEdit_tax.setText(str(tax))
            self.lineEdit_final_price.setText(str(answer))
        self.pushButton_finalcal.clicked.connect(lambda:cal_final_price(self))
       
        def save_central_data():
            pass
        ###點擊儲存，把東西分別放進對應的資料庫
        def save_basic_data():
            save_central_data
            dict_data = {
                'worknum' : self.lineEdit_worknum.text(),
                'case_name' : self.lineEdit_case_name.text(),
                'company_name' :self.comboBox_company_name.currentText(),
                'phone' : self.lineEdit_phone.text(),
                'client_name' : self.lineEdit_client_name.text(),
                'worktime' : self.lineEdit_worktime.text(),
                'cleanuptime' : self.lineEdit_cleanup_time.text(),
                'workaddress' : self.lineEdit_workaddress.text(),
                'pack' : self.comboBox_pack.currentText(),
                'transport' : self.comboBox_transport.currentText(),
                'cemployee1' : self.comboBox_employee_1.currentText(),
                'cemployee2' : self.comboBox_employee_2.currentText(),
                'cemployee3' : self.comboBox_employee_3.currentText(),
                'cemployee4' : self.comboBox_employee_4.currentText(),
                'cemployee5' : self.comboBox_employee_5.currentText(),
                'crossbar_width' : self.lineEdit_crossbar_width.text(),
                'crossbar_amount': self.lineEdit_crossbar_amount.text(),
                'crossbar_remark': self.lineEdit_crossbar_remark.text(),
                '150shelter':self.checkBox_150iron_shelter.isChecked(),
                '180shelter':self.checkBox_180iron_shelter.isChecked(),
                'iron_Shelter_amount':self.lineEdit_iron_shelter_amount.text(),
                'iron_Shelter_remark':self.lineEdit_iron_shelter_remark.text(),
                'paper_Shelter_height':self.lineEdit_paper_shelter_height.text(),
                'paper_Shelter_amount':self.lineEdit_paper_shelter_amount.text(),
                'paper_Shelter_remark':self.lineEdit_paper_shelter_remark.text(),
                'stand_style' : self.lineEdit_stand_style.text(),
                'stand_amount' : self.lineEdit_stand_amount.text(),
                'stand_remark' : self.lineEdit_stand_remark.text(),
                'rent1' : self.lineEdit_rent_1.text(),
                'rent2' : self.lineEdit_rent_2.text(),
                'remark' : self.textEdit_remark.toPlainText()
            }
            check = check_database(self.lineEdit_worknum.text())
            if check == True:
                Insert_data(dict_data)
            else:
                Updata_data(dict_data)
        self.pushButton_save.clicked.connect(save_basic_data)


        ###點擊開啟
        def call_data():
            data = call__basic_data(self.lineEdit_worknum.text())
        self.pushButton_open.clicked.connect(call_data)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())