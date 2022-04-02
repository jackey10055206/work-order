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

connection = pymysql.connect(host='192.168.1.2',
                             port=3306,
                             user='root',
                             passwd='root',
                             database='work_order',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
#print(bool(connection))
# cursor = connection.cursor()



class Main(QMainWindow, ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #create_table()
        #del_data()
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
       

       ### 直接存basic_data
        def save_basic_data():
            dict_data = {
                'worknum' : self.lineEdit_worknum.text(),
                'case_name' : self.lineEdit_case_name.text(),
                'company_name' :str(self.comboBox_company_name.currentIndex()),
                'phone' : self.lineEdit_phone.text(),
                'client_name' : self.lineEdit_client_name.text(),
                'worktime' : self.lineEdit_worktime.text(),
                'cleanuptime' : self.lineEdit_cleanup_time.text(),
                'workaddress' : self.lineEdit_workaddress.text(),
                'pack' : str(self.comboBox_pack.currentIndex()),
                'transport' : str(self.comboBox_transport.currentIndex()),
                'cemployee1' : str(self.comboBox_employee_1.currentIndex()),
                'cemployee2' : str(self.comboBox_employee_2.currentIndex()),
                'cemployee3' : str(self.comboBox_employee_3.currentIndex()),
                'cemployee4' : str(self.comboBox_employee_4.currentIndex()),
                'cemployee5' : str(self.comboBox_employee_5.currentIndex()),
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
            Update_basic_data(dict_data)


        ###直接存central_data
        def save_central_data():
            dict_data = {
                'worknum':self.lineEdit_worknum.text(),
                'product_1':str(self.comboBox_product_1.currentIndex()),
                'product_2':str(self.comboBox_product_2.currentIndex()),
                'product_3':str(self.comboBox_product_3.currentIndex()),
                'product_4':str(self.comboBox_product_4.currentIndex()),
                'product_5':str(self.comboBox_product_5.currentIndex()),
                'product_6':str(self.comboBox_product_6.currentIndex()),
                'product_7':str(self.comboBox_product_7.currentIndex()),
                'product_8':str(self.comboBox_product_8.currentIndex()),
                'product_9':str(self.comboBox_product_9.currentIndex()),
                'product_10':str(self.comboBox_product_10.currentIndex()),
                'product_11':str(self.comboBox_product_11.currentIndex()),
                'product_12':str(self.comboBox_product_12.currentIndex()),
                'product_13':str(self.comboBox_product_13.currentIndex()),
                'product_14':str(self.comboBox_product_14.currentIndex()),
                'product_15':str(self.comboBox_product_15.currentIndex()),
                'width_1':self.lineEdit_width_1.text(),
                'width_2':self.lineEdit_width_2.text(),
                'width_3':self.lineEdit_width_3.text(),
                'width_4':self.lineEdit_width_4.text(),
                'width_5':self.lineEdit_width_5.text(),
                'width_6':self.lineEdit_width_6.text(),
                'width_7':self.lineEdit_width_7.text(),
                'width_8':self.lineEdit_width_8.text(),
                'width_9':self.lineEdit_width_9.text(),
                'width_10':self.lineEdit_width_10.text(),
                'width_11':self.lineEdit_width_11.text(),
                'width_12':self.lineEdit_width_12.text(),
                'width_13':self.lineEdit_width_13.text(),
                'width_14':self.lineEdit_width_14.text(),
                'width_15':self.lineEdit_width_15.text(),
                'height_1':self.lineEdit_height_1.text(),
                'height_2':self.lineEdit_height_2.text(),
                'height_3':self.lineEdit_height_3.text(),
                'height_4':self.lineEdit_height_4.text(),
                'height_5':self.lineEdit_height_5.text(),
                'height_6':self.lineEdit_height_6.text(),
                'height_7':self.lineEdit_height_7.text(),
                'height_8':self.lineEdit_height_8.text(),
                'height_9':self.lineEdit_height_9.text(),
                'height_10':self.lineEdit_height_10.text(),
                'height_11':self.lineEdit_height_11.text(),
                'height_12':self.lineEdit_height_12.text(),
                'height_13':self.lineEdit_height_13.text(),
                'height_14':self.lineEdit_height_14.text(),
                'height_15':self.lineEdit_height_15.text(),
                'amount_1':self.lineEdit_amount_1.text(),
                'amount_2':self.lineEdit_amount_2.text(),
                'amount_3':self.lineEdit_amount_3.text(),
                'amount_4':self.lineEdit_amount_4.text(),
                'amount_5':self.lineEdit_amount_5.text(),
                'amount_6':self.lineEdit_amount_6.text(),
                'amount_7':self.lineEdit_amount_7.text(),
                'amount_8':self.lineEdit_amount_8.text(),
                'amount_9':self.lineEdit_amount_9.text(),
                'amount_10':self.lineEdit_amount_10.text(),
                'amount_11':self.lineEdit_amount_11.text(),
                'amount_12':self.lineEdit_amount_12.text(),
                'amount_13':self.lineEdit_amount_13.text(),
                'amount_14':self.lineEdit_amount_14.text(),
                'amount_15':self.lineEdit_amount_15.text(),
                'material_1':str(self.comboBox_material_1.currentIndex()),
                'material_2':str(self.comboBox_material_2.currentIndex()),
                'material_3':str(self.comboBox_material_3.currentIndex()),
                'material_4':str(self.comboBox_material_4.currentIndex()),
                'material_5':str(self.comboBox_material_5.currentIndex()),
                'material_6':str(self.comboBox_material_6.currentIndex()),
                'material_7':str(self.comboBox_material_7.currentIndex()),
                'material_8':str(self.comboBox_material_8.currentIndex()),
                'material_9':str(self.comboBox_material_9.currentIndex()),
                'material_10':str(self.comboBox_material_10.currentIndex()),
                'material_11':str(self.comboBox_material_11.currentIndex()),
                'material_12':str(self.comboBox_material_12.currentIndex()),
                'material_13':str(self.comboBox_material_13.currentIndex()),
                'material_14':str(self.comboBox_material_14.currentIndex()),
                'material_15':str(self.comboBox_material_15.currentIndex()),
                'process_1':str(self.comboBox_process_1.currentIndex()),
                'process_2':str(self.comboBox_process_2.currentIndex()),
                'process_3':str(self.comboBox_process_3.currentIndex()),
                'process_4':str(self.comboBox_process_4.currentIndex()),
                'process_5':str(self.comboBox_process_5.currentIndex()),
                'process_6':str(self.comboBox_process_6.currentIndex()),
                'process_7':str(self.comboBox_process_7.currentIndex()),
                'process_8':str(self.comboBox_process_8.currentIndex()),
                'process_9':str(self.comboBox_process_9.currentIndex()),
                'process_10':str(self.comboBox_process_10.currentIndex()),
                'process_11':str(self.comboBox_process_11.currentIndex()),
                'process_12':str(self.comboBox_process_12.currentIndex()),
                'process_13':str(self.comboBox_process_13.currentIndex()),
                'process_14':str(self.comboBox_process_14.currentIndex()),
                'process_15':str(self.comboBox_process_15.currentIndex()),
                'plate_1':str(self.comboBox_plate_1.currentIndex()),
                'plate_2':str(self.comboBox_plate_2.currentIndex()),
                'plate_3':str(self.comboBox_plate_3.currentIndex()),
                'plate_4':str(self.comboBox_plate_4.currentIndex()),
                'plate_5':str(self.comboBox_plate_5.currentIndex()),
                'plate_6':str(self.comboBox_plate_6.currentIndex()),
                'plate_7':str(self.comboBox_plate_7.currentIndex()),
                'plate_8':str(self.comboBox_plate_8.currentIndex()),
                'plate_9':str(self.comboBox_plate_9.currentIndex()),
                'plate_10':str(self.comboBox_plate_10.currentIndex()),
                'plate_11':str(self.comboBox_plate_11.currentIndex()),
                'plate_12':str(self.comboBox_plate_12.currentIndex()),
                'plate_13':str(self.comboBox_plate_13.currentIndex()),
                'plate_14':str(self.comboBox_plate_14.currentIndex()),
                'plate_15':str(self.comboBox_plate_15.currentIndex()),
                'thicknes_1':str(self.comboBox_thicknes_1.currentIndex()),
                'thicknes_2':str(self.comboBox_thicknes_2.currentIndex()),
                'thicknes_3':str(self.comboBox_thicknes_3.currentIndex()),
                'thicknes_4':str(self.comboBox_thicknes_4.currentIndex()),
                'thicknes_5':str(self.comboBox_thicknes_5.currentIndex()),
                'thicknes_6':str(self.comboBox_thicknes_6.currentIndex()),
                'thicknes_7':str(self.comboBox_thicknes_7.currentIndex()),
                'thicknes_8':str(self.comboBox_thicknes_8.currentIndex()),
                'thicknes_9':str(self.comboBox_thicknes_9.currentIndex()),
                'thicknes_10':str(self.comboBox_thicknes_10.currentIndex()),
                'thicknes_11':str(self.comboBox_thicknes_11.currentIndex()),
                'thicknes_12':str(self.comboBox_thicknes_12.currentIndex()),
                'thicknes_13':str(self.comboBox_thicknes_13.currentIndex()),
                'thicknes_14':str(self.comboBox_thicknes_14.currentIndex()),
                'thicknes_15':str(self.comboBox_thicknes_15.currentIndex()),
                'others_1':str(self.comboBox_others_1.currentIndex()),
                'others_2':str(self.comboBox_others_2.currentIndex()),
                'others_3':str(self.comboBox_others_3.currentIndex()),
                'others_4':str(self.comboBox_others_4.currentIndex()),
                'others_5':str(self.comboBox_others_5.currentIndex()),
                'others_6':str(self.comboBox_others_6.currentIndex()),
                'others_7':str(self.comboBox_others_7.currentIndex()),
                'others_8':str(self.comboBox_others_8.currentIndex()),
                'others_9':str(self.comboBox_others_9.currentIndex()),
                'others_10':str(self.comboBox_others_10.currentIndex()),
                'others_11':str(self.comboBox_others_11.currentIndex()),
                'others_12':str(self.comboBox_others_12.currentIndex()),
                'others_13':str(self.comboBox_others_13.currentIndex()),
                'others_14':str(self.comboBox_others_14.currentIndex()),
                'others_15':str(self.comboBox_others_15.currentIndex()),
                'others_amount_1':str(self.lineEdit_others_amount_1.text()),
                'others_amount_2':str(self.lineEdit_others_amount_2.text()),
                'others_amount_3':str(self.lineEdit_others_amount_3.text()),
                'others_amount_4':str(self.lineEdit_others_amount_4.text()),
                'others_amount_5':str(self.lineEdit_others_amount_5.text()),
                'others_amount_6':str(self.lineEdit_others_amount_6.text()),
                'others_amount_7':str(self.lineEdit_others_amount_7.text()),
                'others_amount_8':str(self.lineEdit_others_amount_8.text()),
                'others_amount_9':str(self.lineEdit_others_amount_9.text()),
                'others_amount_10':str(self.lineEdit_others_amount_10.text()),
                'others_amount_11':str(self.lineEdit_others_amount_11.text()),
                'others_amount_12':str(self.lineEdit_others_amount_12.text()),
                'others_amount_13':str(self.lineEdit_others_amount_13.text()),
                'others_amount_14':str(self.lineEdit_others_amount_14.text()),
                'others_amount_15':str(self.lineEdit_others_amount_15.text()),

            }
            Update_central_data(dict_data)

        ###直接存price_data        
        def save_price_data():
            dict_data={
                'worknum':self.lineEdit_worknum.text(),
                'lineEdit_CBM_1':self.lineEdit_CBM_1.text(),
                'lineEdit_CBM_2':self.lineEdit_CBM_2.text(),
                'lineEdit_CBM_3':self.lineEdit_CBM_3.text(),
                'lineEdit_CBM_4':self.lineEdit_CBM_4.text(),
                'lineEdit_CBM_5':self.lineEdit_CBM_5.text(),
                'lineEdit_CBM_6':self.lineEdit_CBM_6.text(),
                'lineEdit_CBM_7':self.lineEdit_CBM_7.text(),
                'lineEdit_CBM_8':self.lineEdit_CBM_8.text(),
                'lineEdit_CBM_9':self.lineEdit_CBM_9.text(),
                'lineEdit_CBM_10':self.lineEdit_CBM_10.text(),
                'lineEdit_CBM_11':self.lineEdit_CBM_11.text(),
                'lineEdit_CBM_12':self.lineEdit_CBM_12.text(),
                'lineEdit_CBM_13':self.lineEdit_CBM_13.text(),
                'lineEdit_CBM_14':self.lineEdit_CBM_14.text(),
                'lineEdit_CBM_15':self.lineEdit_CBM_15.text(),
                'lineEdit_CBMprice_1':self.lineEdit_CBMprice_1.text(),
                'lineEdit_CBMprice_2':self.lineEdit_CBMprice_2.text(),
                'lineEdit_CBMprice_3':self.lineEdit_CBMprice_3.text(),
                'lineEdit_CBMprice_4':self.lineEdit_CBMprice_4.text(),
                'lineEdit_CBMprice_5':self.lineEdit_CBMprice_5.text(),
                'lineEdit_CBMprice_6':self.lineEdit_CBMprice_6.text(),
                'lineEdit_CBMprice_7':self.lineEdit_CBMprice_7.text(),
                'lineEdit_CBMprice_8':self.lineEdit_CBMprice_8.text(),
                'lineEdit_CBMprice_9':self.lineEdit_CBMprice_9.text(),
                'lineEdit_CBMprice_10':self.lineEdit_CBMprice_10.text(),
                'lineEdit_CBMprice_11':self.lineEdit_CBMprice_11.text(),
                'lineEdit_CBMprice_12':self.lineEdit_CBMprice_12.text(),
                'lineEdit_CBMprice_13':self.lineEdit_CBMprice_13.text(),
                'lineEdit_CBMprice_14':self.lineEdit_CBMprice_14.text(),
                'lineEdit_CBMprice_15':self.lineEdit_CBMprice_15.text(),
                'lineEdit_single_price_1':self.lineEdit_single_price_1.text(),
                'lineEdit_single_price_2':self.lineEdit_single_price_2.text(),
                'lineEdit_single_price_3':self.lineEdit_single_price_3.text(),
                'lineEdit_single_price_4':self.lineEdit_single_price_4.text(),
                'lineEdit_single_price_5':self.lineEdit_single_price_5.text(),
                'lineEdit_single_price_6':self.lineEdit_single_price_6.text(),
                'lineEdit_single_price_7':self.lineEdit_single_price_7.text(),
                'lineEdit_single_price_8':self.lineEdit_single_price_8.text(),
                'lineEdit_single_price_9':self.lineEdit_single_price_9.text(),
                'lineEdit_single_price_10':self.lineEdit_single_price_10.text(),
                'lineEdit_single_price_11':self.lineEdit_single_price_11.text(),
                'lineEdit_single_price_12':self.lineEdit_single_price_12.text(),
                'lineEdit_single_price_13':self.lineEdit_single_price_13.text(),
                'lineEdit_single_price_14':self.lineEdit_single_price_14.text(),
                'lineEdit_single_price_15':self.lineEdit_single_price_15.text(),
                'lineEdit_single_price_16':self.lineEdit_single_price_16.text(),
                'lineEdit_single_price_17':self.lineEdit_single_price_17.text(),
                'lineEdit_single_price_18':self.lineEdit_single_price_18.text(),
                'lineEdit_single_price_19':self.lineEdit_single_price_19.text(),
                'lineEdit_single_price_20':self.lineEdit_single_price_20.text(),
                'lineEdit_single_price_21':self.lineEdit_single_price_21.text(),
                'lineEdit_single_price_22':self.lineEdit_single_price_22.text(),
                'lineEdit_single_price_23':self.lineEdit_single_price_23.text(),
                'lineEdit_single_price_24':self.lineEdit_single_price_24.text(),
                'lineEdit_single_price_25':self.lineEdit_single_price_25.text(),
                'lineEdit_single_price_26':self.lineEdit_single_price_26.text(),
                'lineEdit_single_price_27':self.lineEdit_single_price_27.text(),
                'lineEdit_single_price_28':self.lineEdit_single_price_28.text(),
                'lineEdit_single_price_29':self.lineEdit_single_price_29.text(),
                'lineEdit_single_price_30':self.lineEdit_single_price_30.text(),
                'lineEdit_tmpprice':self.lineEdit_tmpprice.text(),
                'lineEdit_tax':self.lineEdit_tax.text(),
                'lineEdit_final_price':self.lineEdit_final_price.text()
            }    
            Update_price_data(dict_data)


        ###點擊儲存，直接生一個工單編號在三個表裡面
        def save_data():
            create_work_order(self.lineEdit_worknum.text())
            save_basic_data()
            save_central_data()
            save_price_data()
        self.pushButton_save.clicked.connect(save_data)

        ### 初始化視窗內所有表格
        def init_data():
            self.lineEdit_worknum.setText("")
            self.lineEdit_case_name.setText("")
            self.comboBox_company_name.setCurrentIndex(0)
            self.lineEdit_phone.setText("")
            self.lineEdit_client_name.setText("")
            self.lineEdit_worktime.setText("")
            self.lineEdit_cleanup_time.setText("")
            self.lineEdit_workaddress.setText("")
            self.comboBox_pack.setCurrentIndex(0)
            self.comboBox_transport.setCurrentIndex(0)
            self.comboBox_employee_1.setCurrentIndex(0)
            self.comboBox_employee_2.setCurrentIndex(0)
            self.comboBox_employee_3.setCurrentIndex(0)
            self.comboBox_employee_4.setCurrentIndex(0)
            self.comboBox_employee_5.setCurrentIndex(0)
            self.lineEdit_crossbar_width.setText("")
            self.lineEdit_crossbar_amount.setText("")
            self.lineEdit_crossbar_remark.setText("")
            self.checkBox_150iron_shelter.setChecked(False)
            self.checkBox_180iron_shelter.setChecked(False)
            self.lineEdit_iron_shelter_amount.setText("")
            self.lineEdit_iron_shelter_remark.setText("")
            self.lineEdit_paper_shelter_height.setText("")
            self.lineEdit_paper_shelter_amount.setText("")
            self.lineEdit_paper_shelter_remark.setText("")
            self.lineEdit_stand_style.setText("")
            self.lineEdit_stand_amount.setText("")
            self.lineEdit_stand_remark.setText("")
            self.lineEdit_rent_1.setText("")
            self.lineEdit_rent_2.setText("")
            self.textEdit_remark.setText("")
        
        ### 顯示basic_data
        def show_basic_data(data):
            self.lineEdit_worknum.setText(data['worknum'])
            self.lineEdit_case_name.setText(data['case_name'])
            self.comboBox_company_name.setCurrentIndex(int(data['company_name']))
            self.lineEdit_phone.setText(data['phone'])
            self.lineEdit_client_name.setText(data['client_name'])
            self.lineEdit_worktime.setText(data['worktime'])
            self.lineEdit_cleanup_time.setText(data['cleanuptime'])
            self.lineEdit_workaddress.setText(data['workaddress'])
            self.comboBox_pack.setCurrentIndex(int(data['pack']))
            self.comboBox_transport.setCurrentIndex(int(data['transport']))
            self.comboBox_employee_1.setCurrentIndex(int(data['cemployee1']))
            self.comboBox_employee_2.setCurrentIndex(int(data['cemployee2']))
            self.comboBox_employee_3.setCurrentIndex(int(data['cemployee3']))
            self.comboBox_employee_4.setCurrentIndex(int(data['cemployee4']))
            self.comboBox_employee_5.setCurrentIndex(int(data['cemployee5']))
            self.lineEdit_crossbar_width.setText(data['crossbar_width'])
            self.lineEdit_crossbar_amount.setText(data['crossbar_amount'])
            self.lineEdit_crossbar_remark.setText(data['crossbar_remark'])
            if data['150shelter'] == "True": 
                self.checkBox_150iron_shelter.toggle()
            if data['180shelter'] == "True": 
                self.checkBox_180iron_shelter.toggle()
            self.lineEdit_iron_shelter_amount.setText(data['iron_Shelter_amount'])
            self.lineEdit_iron_shelter_remark.setText(data['iron_Shelter_remark'])
            self.lineEdit_paper_shelter_height.setText(data['paper_Shelter_height'])
            self.lineEdit_paper_shelter_amount.setText(data['paper_Shelter_amount'])
            self.lineEdit_paper_shelter_remark.setText(data['paper_Shelter_remark'])
            self.lineEdit_stand_style.setText(data['stand_style'])
            self.lineEdit_stand_amount.setText(data['stand_amount'])
            self.lineEdit_stand_remark.setText(data['stand_remark'])
            self.lineEdit_rent_1.setText(data['rent1'])
            self.lineEdit_rent_2.setText(data['rent2'])
            self.textEdit_remark.setText(data['remark'])
        
        ###顯示Central_data
        def show_central_data():
            pass
        
        ###顯示price data
        def show_price_data():
            pass

        ###點擊開啟
        def call_data():
            data = call__basic_data(self.lineEdit_worknum.text())
            init_data()
            show_basic_data(data)
            show_central_data()
            show_price_data()
        self.pushButton_open.clicked.connect(call_data)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())





