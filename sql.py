from asyncio.windows_events import NULL
import sys
import math
from project import Ui_Form as ui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tkinter import *


import pymysql
import project as ui
import main as m

connection = pymysql.connect(host='192.168.1.2',
                             port=3306,
                             user='root',
                             passwd='root',
                             database='work_order',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

#print(bool(connection))
cursor = connection.cursor()
# def create_table():
#     SQL="""CREATE TABLE central_data(
#         `product` char(50),
#         `material` char(50),
#         `process` char(50),
#         `plate` char(50),
#         `plate_thickness` char(50),
#         `others` char(50)
#     )"""
#     cursor.execute(SQL)
#     connection.commit()

def create_table():
    SQL="""CREATE TABLE save_central_data(
        `worknum` char(50) NOT NULL,
        `comboBox_product_1`char(50),
        `comboBox_product_2` char(50),
        `comboBox_product_3` char(50),
        `comboBox_product_4` char(50),
        `comboBox_product_5` char(50),
        `comboBox_product_6` char(50),
        `comboBox_product_7` char(50),
        `comboBox_product_8` char(50),
        `comboBox_product_9` char(50),
        `comboBox_product_10` char(50),
        `comboBox_product_11` char(50),
        `comboBox_product_12` char(50),
        `comboBox_product_13` char(50),
        `comboBox_product_14` char(50),
        `comboBox_product_15` char(50),
        `lineEdit_width_1`char(50),
        `lineEdit_width_2` char(50),
        `lineEdit_width_3` char(50),
        `lineEdit_width_4` char(50),
        `lineEdit_width_5` char(50),
        `lineEdit_width_6` char(50),
        `lineEdit_width_7` char(50),
        `lineEdit_width_8` char(50),
        `lineEdit_width_9` char(50),
        `lineEdit_width_10` char(50),
        `lineEdit_width_11` char(50),
        `lineEdit_width_12` char(50),
        `lineEdit_width_13` char(50),
        `lineEdit_width_14` char(50),
        `lineEdit_width_15` char(50),
        `lineEdit_height_1`char(50),
        `lineEdit_height_2` char(50),
        `lineEdit_height_3` char(50),
        `lineEdit_height_4` char(50),
        `lineEdit_height_5` char(50),
        `lineEdit_height_6` char(50),
        `lineEdit_height_7` char(50),
        `lineEdit_height_8` char(50),
        `lineEdit_height_9` char(50),
        `lineEdit_height_10` char(50),
        `lineEdit_height_11` char(50),
        `lineEdit_height_12` char(50),
        `lineEdit_height_13` char(50),
        `lineEdit_height_14` char(50),
        `lineEdit_height_15` char(50),
        `lineEdit_amount_1`char(50),
        `lineEdit_amount_2` char(50),
        `lineEdit_amount_3` char(50),
        `lineEdit_amount_4` char(50),
        `lineEdit_amount_5` char(50),
        `lineEdit_amount_6` char(50),
        `lineEdit_amount_7` char(50),
        `lineEdit_amount_8` char(50),
        `lineEdit_amount_9` char(50),
        `lineEdit_amount_10` char(50),
        `lineEdit_amount_11` char(50),
        `lineEdit_amount_12` char(50),
        `lineEdit_amount_13` char(50),
        `lineEdit_amount_14` char(50),
        `lineEdit_amount_15` char(50),
        `comboBox_material_1`char(50),
        `comboBox_material_2` char(50),
        `comboBox_material_3` char(50),
        `comboBox_material_4` char(50),
        `comboBox_material_5` char(50),
        `comboBox_material_6` char(50),
        `comboBox_material_7` char(50),
        `comboBox_material_8` char(50),
        `comboBox_material_9` char(50),
        `comboBox_material_10` char(50),
        `comboBox_material_11` char(50),
        `comboBox_material_12` char(50),
        `comboBox_material_13` char(50),
        `comboBox_material_14` char(50),
        `comboBox_material_15` char(50),
        `comboBox_process_1`char(50),
        `comboBox_process_2` char(50),
        `comboBox_process_3` char(50),
        `comboBox_process_4` char(50),
        `comboBox_process_5` char(50),
        `comboBox_process_6` char(50),
        `comboBox_process_7` char(50),
        `comboBox_process_8` char(50),
        `comboBox_process_9` char(50),
        `comboBox_process_10` char(50),
        `comboBox_process_11` char(50),
        `comboBox_process_12` char(50),
        `comboBox_process_13` char(50),
        `comboBox_process_14` char(50),
        `comboBox_process_15` char(50),
        `comboBox_plate_1`char(50),
        `comboBox_plate_2` char(50),
        `comboBox_plate_3` char(50),
        `comboBox_plate_4` char(50),
        `comboBox_plate_5` char(50),
        `comboBox_plate_6` char(50),
        `comboBox_plate_7` char(50),
        `comboBox_plate_8` char(50),
        `comboBox_plate_9` char(50),
        `comboBox_plate_10` char(50),
        `comboBox_plate_11` char(50),
        `comboBox_plate_12` char(50),
        `comboBox_plate_13` char(50),
        `comboBox_plate_14` char(50),
        `comboBox_plate_15` char(50),
        `comboBox_thicknes_1`char(50),
        `comboBox_thicknes_2` char(50),
        `comboBox_thicknes_3` char(50),
        `comboBox_thicknes_4` char(50),
        `comboBox_thicknes_5` char(50),
        `comboBox_thicknes_6` char(50),
        `comboBox_thicknes_7` char(50),
        `comboBox_thicknes_8` char(50),
        `comboBox_thicknes_9` char(50),
        `comboBox_thicknes_10` char(50),
        `comboBox_thicknes_11` char(50),
        `comboBox_thicknes_12` char(50),
        `comboBox_thicknes_13` char(50),
        `comboBox_thicknes_14` char(50),
        `comboBox_thicknes_15` char(50),
        `comboBox_others_1`char(50),
        `comboBox_others_2` char(50),
        `comboBox_others_3` char(50),
        `comboBox_others_4` char(50),
        `comboBox_others_5` char(50),
        `comboBox_others_6` char(50),
        `comboBox_others_7` char(50),
        `comboBox_others_8` char(50),
        `comboBox_others_9` char(50),
        `comboBox_others_10` char(50),
        `comboBox_others_11` char(50),
        `comboBox_others_12` char(50),
        `comboBox_others_13` char(50),
        `comboBox_others_14` char(50),
        `comboBox_others_15` char(50),
        `lineEdit_others_amount_1`char(50),
        `lineEdit_others_amount_2` char(50),
        `lineEdit_others_amount_3` char(50),
        `lineEdit_others_amount_4` char(50),
        `lineEdit_others_amount_5` char(50),
        `lineEdit_others_amount_6` char(50),
        `lineEdit_others_amount_7` char(50),
        `lineEdit_others_amount_8` char(50),
        `lineEdit_others_amount_9` char(50),
        `lineEdit_others_amount_10` char(50),
        `lineEdit_others_amount_11` char(50),
        `lineEdit_others_amount_12` char(50),
        `lineEdit_others_amount_13` char(50),
        `lineEdit_others_amount_14` char(50),
        `lineEdit_others_amount_15` char(50),
        PRIMARY KEY(worknum)
    )"""
    cursor.execute(SQL)
    connection.commit()


def add_employee():
    SQL = """INSERT INTO employee(name)
                VALUES(''),
                ('羅浩強'),
                ('羅韋杰'),
                ('鄭志豪'),
                ('盧俊達')
          """
    cursor.execute(SQL)
    connection.commit()

def add_pack_transport():
    SQL = """INSERT INTO pack_transport (pack,transport)
                VALUES('',''),
                ('廢版','自送'),
                ('紙箱','派車'),
                ('離形紙','快遞'),
                ('瓦楞紙版','自取')  
          """
    cursor.execute(SQL)
    connection.commit()

def add_central_data():
    SQL = """INSERT INTO central_data (product,material,process,plate,plate_thickness,others)
             VALUES('','','','','',''),
             ('舞台背板','PP','亮面冷錶','合成板','5mm','150cm直角鐵腳架'),
             ('接待背板','PVC','霧面冷錶','豪卡板','1cm','180cm直角鐵角架'),
             ('展示背板','燈片','亮面+正面雙面膠','黑合成','1.5cm','150cm斜角鐵角架'),
             ('攤位背板','弱黏PVC','地板膠','瓦楞板','2cm','180cm斜角鐵角架'),
             ('媒體背板','弱黏導氣PVC','地板膠','黑瓦楞','1mm','橫桿'),
             ('報到處板','單透布300D','特殊加工','發泡板','2mm','貼條'),
             ('講台背板','雙透布150D','厚磅紙板','','','機台切型'),
             ('桌前背板','油畫布600D','','','','易拉展'),
             ('議程背板','油畫布900D','','','','X展架'),
             ('人型立牌','半透PVC','','','','紙腳架'),
             ('橫幅背板','全透PVC','','','','組合框租用'),
             ('三角桌牌','單向透視','','','','TRUSS'),
             ('桌上立牌','膠膜','','','','燈光'),
             ('指引牌','帆布','','','','吊工'),
             ('箭頭','壓克力','','','','鷹架搭設'),
             ('名牌','保麗龍','','','',''),
             ('桌次表','全透PET','','','',''),
             ('摸彩箱','','','','',''),
             ('手舉牌','','','','',''),
             ('易拉展','','','','',''),
             ('X展架','','','','',''),
             ('MIC牌','','','','',''),
             ('海報','','','','',''),
             ('簽名綢','','','','',''),
             ('掛軸','','','','',''),
             ('旗幟','','','','',''),
             ('帆布','','','','',''),
             ('關東旗','','','','',''),
             ('地貼','','','','',''),
             ('窗貼','','','','',''),
             ('道具','','','','',''),
             ('包裝','','','','',''),
             ('外發','','','','',''),
             ('其他','','','','','')
    """
    cursor.execute(SQL)
    connection.commit()

def add_client():
    SQL = """INSERT INTO client(name,full_name,phone,address,taxID)
             VALUES('','','','',''),
             ('6636','陸陸參拾陸有限公司','66368606','10694台北市忠孝東路四段320號10樓','27541768'),
             ('228基金會','財團法人二二八事件紀念基金會','23326228','10066台北市南海路54號','97971614'),
             ('228共生','社團法人台灣共生青年協會','無','10351台北市大同區長安西路84號4樓之一','85202463'),
             ('KING','誠全整合行銷有限公司','0938616260','10049台北市中正區北平東路30-2號4樓','83231490'),
             ('Eric','','0935888727','',''),
             ('AAMA','財團法人台北市創業者共創平台基金會','','10058台北市中正區八德路一段1號2樓','77793991'),
             ('九天馬','九天馬整合行銷有限公司','27207070','11061台北市忠孝東路五段412號6樓','84909060'),
             ('中央社','財團法人中央通訊社','25051180','10485台北市松江路209號','97991169'),
             ('可樂旅遊','康福旅行社(股)公司','25112556','10457台北市中山區南京東路二段90號17樓','04315397'),
             ('心連結書佾','眾好行銷有限公司','0933092714','231新北市新店區如意街13巷3弄3號6樓','50776098'),
             ('加密實驗','加密實驗股份有限公司','0988189451','10061台北市中正區信義路二段253號','5077293'),
             ('台灣原色','台灣原色創意行銷有限公司','0937549598','33052桃園市大有路489號7樓之一','28728713'),
             ('石盤公關','石盤公關顧問有限公司','27082678','10682台北市大安區信義路四段96號5樓之2','12939918'),
             ('禾睿','禾睿整合行銷有限公司','','10491台北市中山區建國北路一段78巷36號1樓','24324824'),
             ('亞洲黃龍','亞洲黃隆有限公司','27906028','11470台北市內湖區南京東路六段346號12樓之一','80132215'),
             ('林思宏醫師','財團法人台北市林思宏X5醫師慈善基金會','27036988','106台北市大安區復興南路二段210巷9號','77603660'),
             ('采月廣告','采月設計有限公司','86478840','22172新北市汐止區茄苳路240號','24496570'),
             ('冠銘廣告','冠銘廣告企業社','23250209','10695台北市光復南路420巷26號','81615718'),
             ('美味生活','美味生活股份有限公司','0981307638','10487台北市南京東路三段89巷27弄19號1樓','21931519'),
             ('時代基金會','財團法人時代基金會','25112678','10449台北市中山北路二段96號後棟9樓','76942403'),
             ('Lingumi','Lingumi','','10449台北市中山區中山北路二段96號後棟9樓','82947905'),
             ('區塊鏈','台灣區塊鏈愛好者協會','0905935509','115台北市南港區經貿二路2號','76312926'),
             ('國泰人壽','國泰人壽保險(股)公司','27551399','10687台北市仁愛路四段296號18樓','03374707'),
             ('陳椿樺','','','',''),
             ('麥點公關','麥點創意行銷有限公司','','10478台北市中山區合江街105巷21號','27555544'),
             ('富邦金控','台北富邦商業銀行股份有限公司','66027527','105台北市松山區敦化南路一段108號6樓','03750168'),
             ('台灣人壽','台灣人壽保險(股)公司','','11568台北市南港區經貿二陸188號7樓','03557017'),
             ('聯廣','格威傳媒股份有限公司','26278806','1692台北市大安區忠孝東路四段285號3樓','1133055'),
             ('富越','富越空間計畫公司有限公司','','23147新北市新店區新店路129號2樓','84139350'),
             ('華碩雲端','華碩雲端股份有限公司','28987477','25159新北市淡水區中正東路二段177號4樓','70538068'),
             ('傳揚行銷','傳揚行銷廣告(股)公司','25021929','10489台北市南京東路三段26號11樓','89963035'),
             ('新巨企業','新巨企業(股)公司','','23141新北市新店區民權路50號10樓','20970807'),
             ('新綠','新綠主義(股)公司','77294877','22055新北市板橋區縣民大道一段285號3樓','28498923'),
             ('宏綠','宏綠景觀(股)公司','22720552','22055新北市板橋區明德街2巷8號','53705055'),
             ('源子設計','源子創作館','','10667台北市大安區大安路二段142巷5號1樓','10340534'),
             ('遠雄人壽','遠雄人壽保險事業(股)公司','','11073台北市信義區松高路1號26樓','84703052'),
             ('數位時代','巨思文化(股)有限公司','','10694台北市光復南路二102號9樓','16780474'),
             ('尚凡','尚凡國際創新科技股份有限公司','23650103','106台北市大安區羅斯福路三段37號12樓','80283629'),
             ('內湖扶輪社','台北內湖扶輪社','','104台北市中山區松江路328號8樓之6',''),
             ('創新扶輪社','社團法人台日國際扶輪親善會','','23141新北市新店區民權路100號13樓','25281631'),
             ('國際扶輪社','社團法人國際扶輪3482地區','','','42521538'),
             ('雲端扶輪社','台北雲端扶輪社','25238638','104台北市中山區松江路328號8樓之6','38583949'),
             ('憾聲音響','撼聲影音有限公司','','23512新北市中和區立德街138號4樓','23618744'),
             ('彥儒','默默的有限公司','0928160214','','83448245'),
             ('鴻榮','參拾參創意行銷有限公司','','10352台北市大同區承德路二段1巷8號1樓','54055163'),
             ('宣彩印刷','宣彩印刷有限公司','28421106','23585新北市中和區建康路','50856851'),
             ('試富社會','試附社會企業有限公司','23912288','10652台北市忠孝東路三段96號4樓之一','52932476'),
             ('繁葵','繁葵實業股份有限公司','0911068081','231新北市新店區寶橋路235巷2號7樓','97404268'),
             ('無設Ivan','無設制作設計有限公司','','24155新北市三重區仁愛街178號3樓','83566018'),
             ('燈光小尤','意象聲動創設實業社','','24254新北市新莊區復興路二段130號2樓','41381355'),
             ('林彥岑','台灣數位媒體應用暨行銷協會','77180056','10683台北市大安區敦化南路2段2號3樓-1','42543218'),
             ('優越廣告','優越廣告(股)公司','','10478台北市中山區合江街105巷21號1樓','80694833'),
             ('薔薇杉婚禮','薔薇杉婚禮設計有限公司','','11680台北市文山區景隆街1巷7號1樓','55800603'),
             ('芝山綠園','社團法人台北市野鳥學會芝山岩管理處','','111台北市士林區雨聲街120號','29207509'),
             ('波賽頓','波賽頓科技有限公司','77515558','22246新北市深坑區北深路一段181號3樓','24723723'),
             ('永達保險','永達保險經紀人(股)公司','25212019','10448台北市中山區中山北路二段79號4樓','12684149'),
             ('黑森林','黑森林知識文化產業(股)公司','27952230','11490台北市內湖區民權東路6段216號','54363289'),
             ('心心相印','心心相印(股)公司','','22068新北市板橋區中山路二段403-6號9樓','83666430'),
             ('資廚','資廚管理顧問(股)公司','27130120','106465台北市大安區仁愛路三段136號15樓 1501室','53750585'),
             ('龍骨王','龍骨王股份有限公司','77236027','11577台北市南港區八德路四段768巷1弄20號B1樓A02室','54158175')
          """
    cursor.execute(SQL)
    connection.commit()
        
def update_client():
    SQL = """UPDATE client SET full_name='',phone = '', address = '104台北市中山區松江路328號8樓之6',taxID='' WHERE name = '內湖扶輪社'"""  
    print(SQL)
    cursor.execute(SQL)
    connection.commit()    

def company_name():
    SQL = """SELECT name FROM client"""

    cursor.execute(SQL)
    data = cursor.fetchall()
    connection.commit()

    Cname = []

    def store(name_in):
        Cname.append(name_in)

    for row in data:
        name_in = row['name']
        store(name_in)    
    
    return Cname

def company_name_change(Cname):
    
    #print(Cname)
    SQL="""SELECT * FROM client WHERE name = '%s'""" % Cname
    #print(SQL)
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()

    for row in data:
        full_name = row['full_name']
        phone = row['phone']
        address = row['address']
        taxID = row['taxID']       
    return full_name,phone,address,taxID
    
def employee_name():
    SQL = """SELECT name FROM employee"""

    cursor.execute(SQL)
    data = cursor.fetchall()
    connection.commit()

    Ename = []

    def store(name_in):
        Ename.append(name_in)

    for row in data:
        name_in = row['name']
        store(name_in)    
    
    return Ename

def pack_name():
    SQL = """SELECT pack FROM pack_transport"""
    cursor.execute(SQL)
    data = cursor.fetchall()
    connection.commit()

    Pname = []
    def store(name_in):
        Pname.append(name_in)

    for row in data:
        name_in = row['pack']
        store(name_in)
    return Pname

def transport_name():
    SQL = """SELECT transport FROM pack_transport"""
    cursor.execute(SQL)
    data = cursor.fetchall()
    connection.commit()
    
    Tname = []
    def store(name_in):
        Tname.append(name_in)

    for row in data:
        name_in = row['transport']
        store(name_in)
    return Tname

def product_name():
    SQL = """SELECT product FROM central_data"""
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()

    Pname = []
    def store(name_in):
        Pname.append(name_in)

    for row in data:
        name_in = row['product']
        store(name_in)
    return Pname

def material_name():
    SQL = """SELECT material FROM central_data"""
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()

    Mname = []
    def store(name_in):
        Mname.append(name_in)

    for row in data:
        name_in = row['material']
        store(name_in)
    return Mname

def process_name():
    SQL = """SELECT process FROM central_data"""
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()

    Pname = []
    def store(name_in):
        Pname.append(name_in)

    for row in data:
        name_in = row['process']
        store(name_in)
    return Pname

def plate_name():
    SQL = """SELECT plate FROM central_data"""
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()

    Pname = []
    def store(name_in):
        Pname.append(name_in)

    for row in data:
        name_in = row['plate']
        store(name_in)
    return Pname

def thickness_name():
    SQL = """SELECT plate_thickness FROM central_data"""
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()

    Pname = []
    def store(name_in):
        Pname.append(name_in)

    for row in data:
        name_in = row['plate_thickness']
        store(name_in)
    return Pname

def others_name():

    SQL = """SELECT others FROM central_data"""
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()

    Oname = []
    def store(name_in):
        Oname.append(name_in)

    for row in data:
        name_in = row['others']
        store(name_in)
    return Oname



#######################################
def check_database(Wnum):
    SQL = """SELECT * FROM save_basic_data WHERE worknum = '%s'""" % Wnum
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()
    if data == ():
        return True
    else:
        return False
#######################################
def Update_basic_data(data):
    SQL ="""UPDATE save_basic_data 
             SET worknum='%s',case_name='%s',company_name='%s',phone='%s',client_name='%s',worktime='%s',cleanuptime='%s',workaddress='%s',pack='%s',transport='%s',cemployee1='%s',cemployee2='%s',cemployee3='%s',cemployee4='%s',cemployee5='%s',crossbar_width='%s',crossbar_amount='%s',crossbar_remark='%s',150shelter='%s',180shelter='%s',iron_Shelter_amount='%s',iron_Shelter_remark='%s',paper_Shelter_height='%s',paper_Shelter_amount='%s',paper_Shelter_remark='%s',stand_style='%s',stand_amount='%s',stand_remark='%s',rent1='%s',rent2='%s',remark='%s'
             WHERE worknum = '%s'
         """ % (data['worknum']  , data['case_name'] , data['company_name'] , data['phone'] ,data['client_name'] , data['worktime'] , data['cleanuptime'] , data['workaddress'] , data['pack'] , data['transport'] , data['cemployee1'] , data['cemployee2'] , data['cemployee3'] , data['cemployee4'] , data['cemployee5'] , data['crossbar_width'] , data['crossbar_amount'] , data['crossbar_remark'] , str(data['150shelter']) , str(data['180shelter']) , data['iron_Shelter_amount'] , data['iron_Shelter_remark'] , data['paper_Shelter_height'] , data['paper_Shelter_amount'] , data['paper_Shelter_remark'] , data['stand_style'] , data['stand_amount'] , data['stand_remark'] , data['rent1'] , data['rent2'] , data['remark'],data['worknum'])
    cursor.execute(SQL)
    connection.commit

def call__basic_data(Wnum):
    SQL = """SELECT * FROM save_basic_data WHERE worknum = '%s'""" % Wnum

    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()
    dict_data = data[0]
    return dict_data

#######################################

def Update_central_data(data):
    SQL = """UPDATE save_central_data
             SET comboBox_product_1='%s',comboBox_product_2='%s',comboBox_product_3='%s',comboBox_product_4='%s',comboBox_product_5='%s',comboBox_product_6='%s',comboBox_product_7='%s',comboBox_product_8='%s',comboBox_product_9='%s',comboBox_product_10='%s',comboBox_product_11='%s',comboBox_product_12='%s',comboBox_product_13='%s',comboBox_product_14='%s',comboBox_product_15='%s',
                 lineEdit_width_1='%s',lineEdit_width_2='%s',lineEdit_width_3='%s',lineEdit_width_4='%s',lineEdit_width_5='%s',lineEdit_width_6='%s',lineEdit_width_7='%s',lineEdit_width_8='%s',lineEdit_width_9='%s',lineEdit_width_10='%s',lineEdit_width_11='%s',lineEdit_width_12='%s',lineEdit_width_13='%s',lineEdit_width_14='%s',lineEdit_width_15='%s',
                 lineEdit_height_1='%s',lineEdit_height_2='%s',lineEdit_height_3='%s',lineEdit_height_4='%s',lineEdit_height_5='%s',lineEdit_height_6='%s',lineEdit_height_7='%s',lineEdit_height_8='%s',lineEdit_height_9='%s',lineEdit_height_10='%s',lineEdit_height_11='%s',lineEdit_height_12='%s',lineEdit_height_13='%s',lineEdit_height_14='%s',lineEdit_height_15='%s',
                 lineEdit_amount_1='%s',lineEdit_amount_2='%s',lineEdit_amount_3='%s',lineEdit_amount_4='%s',lineEdit_amount_5='%s',lineEdit_amount_6='%s',lineEdit_amount_7='%s',lineEdit_amount_8='%s',lineEdit_amount_9='%s',lineEdit_amount_10='%s',lineEdit_amount_11='%s',lineEdit_amount_12='%s',lineEdit_amount_13='%s',lineEdit_amount_14='%s',lineEdit_amount_15='%s',
                 comboBox_material_1='%s',comboBox_material_2='%s',comboBox_material_3='%s',comboBox_material_4='%s',comboBox_material_5='%s',comboBox_material_6='%s',comboBox_material_7='%s',comboBox_material_8='%s',comboBox_material_9='%s',comboBox_material_10='%s',comboBox_material_11='%s',comboBox_material_12='%s',comboBox_material_13='%s',comboBox_material_14='%s',comboBox_material_15='%s',
                 comboBox_process_1='%s',comboBox_process_2='%s',comboBox_process_3='%s',comboBox_process_4='%s',comboBox_process_5='%s',comboBox_process_6='%s',comboBox_process_7='%s',comboBox_process_8='%s',comboBox_process_9='%s',comboBox_process_10='%s',comboBox_process_11='%s',comboBox_process_12='%s',comboBox_process_13='%s',comboBox_process_14='%s',comboBox_process_15='%s',
                 comboBox_plate_1='%s',comboBox_plate_2='%s',comboBox_plate_3='%s',comboBox_plate_4='%s',comboBox_plate_5='%s',comboBox_plate_6='%s',comboBox_plate_7='%s',comboBox_plate_8='%s',comboBox_plate_9='%s',comboBox_plate_10='%s',comboBox_plate_11='%s',comboBox_plate_12='%s',comboBox_plate_13='%s',comboBox_plate_14='%s',comboBox_plate_15='%s',
                 comboBox_thicknes_1='%s',comboBox_thicknes_2='%s',comboBox_thicknes_3='%s',comboBox_thicknes_4='%s',comboBox_thicknes_5='%s',comboBox_thicknes_6='%s',comboBox_thicknes_7='%s',comboBox_thicknes_8='%s',comboBox_thicknes_9='%s',comboBox_thicknes_10='%s',comboBox_thicknes_11='%s',comboBox_thicknes_12='%s',comboBox_thicknes_13='%s',comboBox_thicknes_14='%s',comboBox_thicknes_15='%s',
                 comboBox_others_1='%s',comboBox_others_2='%s',comboBox_others_3='%s',comboBox_others_4='%s',comboBox_others_5='%s',comboBox_others_6='%s',comboBox_others_7='%s',comboBox_others_8='%s',comboBox_others_9='%s',comboBox_others_10='%s',comboBox_others_11='%s',comboBox_others_12='%s',comboBox_others_13='%s',comboBox_others_14='%s',comboBox_others_15='%s',
                 lineEdit_others_amount_1='%s',lineEdit_others_amount_2='%s',lineEdit_others_amount_3='%s',lineEdit_others_amount_4='%s',lineEdit_others_amount_5='%s',lineEdit_others_amount_6='%s',lineEdit_others_amount_7='%s',lineEdit_others_amount_8='%s',lineEdit_others_amount_9='%s',lineEdit_others_amount_10='%s',lineEdit_others_amount_11='%s',lineEdit_others_amount_12='%s',lineEdit_others_amount_13='%s',lineEdit_others_amount_14='%s',lineEdit_others_amount_15='%s'
             WHERE worknum='%s'
          """% (data['product_1'],data['product_2'],data['product_3'],data['product_4'],data['product_5'],data['product_6'],data['product_7'],data['product_8'],data['product_9'],data['product_10'],data['product_11'],data['product_12'],data['product_13'],data['product_14'],data['product_15'],data['width_1'],data['width_2'],data['width_3'],data['width_4'],data['width_5'],data['width_6'],data['width_7'],data['width_8'],data['width_9'],data['width_10'],data['width_11'],data['width_12'],data['width_13'],data['width_14'],data['width_15'],data['height_1'],data['height_2'],data['height_3'],data['height_4'],data['height_5'],data['height_6'],data['height_7'],data['height_8'],data['height_9'],data['height_10'],data['height_11'],data['height_12'],data['height_13'],data['height_14'],data['height_15'],data['amount_1'],data['amount_2'],data['amount_3'],data['amount_4'],data['amount_5'],data['amount_6'],data['amount_7'],data['amount_8'],data['amount_9'],data['amount_10'],data['amount_11'],data['amount_12'],data['amount_13'],data['amount_14'],data['amount_15'],data['material_1'],data['material_2'],data['material_3'],data['material_4'],data['material_5'],data['material_6'],data['material_7'],data['material_8'],data['material_9'],data['material_10'],data['material_11'],data['material_12'],data['material_13'],data['material_14'],data['material_15'],data['process_1'],data['process_2'],data['process_3'],data['process_4'],data['process_5'],data['process_6'],data['process_7'],data['process_8'],data['process_9'],data['process_10'],data['process_11'],data['process_12'],data['process_13'],data['process_14'],data['process_15'],data['plate_1'],data['plate_2'],data['plate_3'],data['plate_4'],data['plate_5'],data['plate_6'],data['plate_7'],data['plate_8'],data['plate_9'],data['plate_10'],data['plate_11'],data['plate_12'],data['plate_13'],data['plate_14'],data['plate_15'],data['thicknes_1'],data['thicknes_2'],data['thicknes_3'],data['thicknes_4'],data['thicknes_5'],data['thicknes_6'],data['thicknes_7'],data['thicknes_8'],data['thicknes_9'],data['thicknes_10'],data['thicknes_11'],data['thicknes_12'],data['thicknes_13'],data['thicknes_14'],data['thicknes_15'],data['others_1'],data['others_2'],data['others_3'],data['others_4'],data['others_5'],data['others_6'],data['others_7'],data['others_8'],data['others_9'],data['others_10'],data['others_11'],data['others_12'],data['others_13'],data['others_14'],data['others_15'],data['others_amount_1'],data['others_amount_2'],data['others_amount_3'],data['others_amount_4'],data['others_amount_5'],data['others_amount_6'],data['others_amount_7'],data['others_amount_8'],data['others_amount_9'],data['others_amount_10'],data['others_amount_11'],data['others_amount_12'],data['others_amount_13'],data['others_amount_14'],data['others_amount_15'],data['worknum'])
    cursor.execute(SQL)
    print(SQL)
    connection.commit()

def call_central_data(Wnum):
    SQL = """SELECT * FROM save_central_data WHERE worknum = '%s'""" % Wnum
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()
    print(data)
#######################################


def Update_price_data(data):
    SQL = """UPDATE save_price_data
             SET lineEdit_CBM_1='%s',lineEdit_CBM_2='%s',lineEdit_CBM_3='%s',lineEdit_CBM_4='%s',lineEdit_CBM_5='%s',lineEdit_CBM_6='%s',lineEdit_CBM_7='%s',lineEdit_CBM_8='%s',lineEdit_CBM_9='%s',lineEdit_CBM_10='%s',lineEdit_CBM_11='%s',lineEdit_CBM_12='%s',lineEdit_CBM_13='%s',lineEdit_CBM_14='%s',lineEdit_CBM_15='%s',
                 lineEdit_CBMprice_1='%s',lineEdit_CBMprice_2='%s',lineEdit_CBMprice_3='%s',lineEdit_CBMprice_4='%s',lineEdit_CBMprice_5='%s',lineEdit_CBMprice_6='%s',lineEdit_CBMprice_7='%s',lineEdit_CBMprice_8='%s',lineEdit_CBMprice_9='%s',lineEdit_CBMprice_10='%s',lineEdit_CBMprice_11='%s',lineEdit_CBMprice_12='%s',lineEdit_CBMprice_13='%s',lineEdit_CBMprice_14='%s',lineEdit_CBMprice_15='%s',
                 lineEdit_single_price_1='%s',lineEdit_single_price_2='%s',lineEdit_single_price_3='%s',lineEdit_single_price_4='%s',lineEdit_single_price_5='%s',lineEdit_single_price_6='%s',lineEdit_single_price_7='%s',lineEdit_single_price_8='%s',lineEdit_single_price_9='%s',lineEdit_single_price_10='%s',lineEdit_single_price_11='%s',lineEdit_single_price_12='%s',lineEdit_single_price_13='%s',lineEdit_single_price_14='%s',lineEdit_single_price_15='%s',
                 lineEdit_single_price_16='%s',lineEdit_single_price_17='%s',lineEdit_single_price_18='%s',lineEdit_single_price_19='%s',lineEdit_single_price_20='%s',lineEdit_single_price_21='%s',lineEdit_single_price_22='%s',lineEdit_single_price_23='%s',lineEdit_single_price_24='%s',lineEdit_single_price_25='%s',lineEdit_single_price_26='%s',lineEdit_single_price_27='%s',lineEdit_single_price_28='%s',lineEdit_single_price_29='%s',lineEdit_single_price_30='%s',
                 lineEdit_tmpprice='%s',lineEdit_tax='%s',lineEdit_final_price='%s'             
             WHERE worknum='%s'
          """ %( data['lineEdit_CBM_1'],data['lineEdit_CBM_2'],data['lineEdit_CBM_3'],data['lineEdit_CBM_4'],data['lineEdit_CBM_5'],data['lineEdit_CBM_6'],data['lineEdit_CBM_7'],data['lineEdit_CBM_8'],data['lineEdit_CBM_9'],data['lineEdit_CBM_10'],data['lineEdit_CBM_11'],data['lineEdit_CBM_12'],data['lineEdit_CBM_13'],data['lineEdit_CBM_14'],data['lineEdit_CBM_15'],data['lineEdit_CBMprice_1'],data['lineEdit_CBMprice_2'],data['lineEdit_CBMprice_3'],data['lineEdit_CBMprice_4'],data['lineEdit_CBMprice_5'],data['lineEdit_CBMprice_6'],data['lineEdit_CBMprice_7'],data['lineEdit_CBMprice_8'],data['lineEdit_CBMprice_9'],data['lineEdit_CBMprice_10'],data['lineEdit_CBMprice_11'],data['lineEdit_CBMprice_12'],data['lineEdit_CBMprice_13'],data['lineEdit_CBMprice_14'],data['lineEdit_CBMprice_15'],data['lineEdit_single_price_1'],data['lineEdit_single_price_2'],data['lineEdit_single_price_3'],data['lineEdit_single_price_4'],data['lineEdit_single_price_5'],data['lineEdit_single_price_6'],data['lineEdit_single_price_7'],data['lineEdit_single_price_8'],data['lineEdit_single_price_9'],data['lineEdit_single_price_10'],data['lineEdit_single_price_11'],data['lineEdit_single_price_12'],data['lineEdit_single_price_13'],data['lineEdit_single_price_14'],data['lineEdit_single_price_15'],data['lineEdit_single_price_16'],data['lineEdit_single_price_17'],data['lineEdit_single_price_18'],data['lineEdit_single_price_19'],data['lineEdit_single_price_20'],data['lineEdit_single_price_21'],data['lineEdit_single_price_22'],data['lineEdit_single_price_23'],data['lineEdit_single_price_24'],data['lineEdit_single_price_25'],data['lineEdit_single_price_26'],data['lineEdit_single_price_27'],data['lineEdit_single_price_28'],data['lineEdit_single_price_29'],data['lineEdit_single_price_30'],data['lineEdit_tmpprice'],data['lineEdit_tax'],data['lineEdit_final_price'],data['worknum'])
    cursor.execute(SQL)
    connection.commit()

def call_price_data(Wnum):
    pass
#######################################

def create_work_order(Wnum):

    if (check_database(Wnum)):
        SQL1 = """INSERT INTO save_basic_data(worknum) VALUES('%s')""" % Wnum
        SQL2 = """INSERT INTO save_central_data(worknum) VALUES('%s')""" % Wnum
        SQL3 = """INSERT INTO save_price_data(worknum) VALUES('%s')""" % Wnum
        
        cursor.execute(SQL1)
        cursor.execute(SQL2)
        cursor.execute(SQL3)
        connection.commit()
    else:
        pass

def del_data():
    SQL = """DELETE FROM save_central_data"""
    SQL2 = """DELETE FROM save_basic_data"""
    SQL3 = """DELETE FROM save_price_data"""
    cursor.execute(SQL)
    cursor.execute(SQL2)
    cursor.execute(SQL3)
    connection.commit()

#worknum,case_name,company_name,phone,client_name,worktime,cleanuptime,workaddress,pack,transport,cemployee1,cemployee2,cemployee3,cemployee4,cemployee5,crossbar_width,crossbar_amount,crossbar_remark,150shelter,180shelter,iron_Shelter_amount,iron_Shelter_remark,paper_Shelter_height,paper_Shelter_amount,paper_Shelter_remark,stand_style,stand_amount,stand_remark,rent1,rent2,remark
# data['worknum'],
# data['product_1'],data['product_2'],data['product_3'],data['product_4'],data['product_5'],data['product_6'],data['product_7'],data['product_8'],data['product_9'],data['product_10'],data['product_11'],data['product_12'],data['product_13'],data['product_14'],data['product_15'],
# data['width_1'],data['width_2'],data['width_3'],data['width_4'],data['width_5'],data['width_6'],data['width_7'],data['width_8'],data['width_9'],data['width_10'],data['width_11'],data['width_12'],data['width_13'],data['width_14'],data['width_15'],
# data['height_1'],data['height_2'],data['height_3'],data['height_4'],data['height_5'],data['height_6'],data['height_7'],data['height_8'],data['height_9'],data['height_10'],data['height_11'],data['height_12'],data['height_13'],data['height_14'],data['height_15'],
# data['amount_1'],data['amount_2'],data['amount_3'],data['amount_4'],data['amount_5'],data['amount_6'],data['amount_7'],data['amount_8'],data['amount_9'],data['amount_10'],data['amount_11'],data['amount_12'],data['amount_13'],data['amount_14'],data['amount_15'],
# data['material_1'],data['material_2'],data['material_3'],data['material_4'],data['material_5'],data['material_6'],data['material_7'],data['material_8'],data['material_9'],data['material_10'],data['material_11'],data['material_12'],data['material_13'],data['material_14'],data['material_15'],
# data['process_1'],data['process_2'],data['process_3'],data['process_4'],data['process_5'],data['process_6'],data['process_7'],data['process_8'],data['process_9'],data['process_10'],data['process_11'],data['process_12'],data['process_13'],data['process_14'],data['process_15'],
# data['plate_1'],data['plate_2'],data['plate_3'],data['plate_4'],data['plate_5'],data['plate_6'],data['plate_7'],data['plate_8'],data['plate_9'],data['plate_10'],data['plate_11'],data['plate_12'],data['plate_13'],data['plate_14'],data['plate_15'],
# data['thicknes_1'],data['thicknes_2'],data['thicknes_3'],data['thicknes_4'],data['thicknes_5'],data['thicknes_6'],data['thicknes_7'],data['thicknes_8'],data['thicknes_9'],data['thicknes_10'],data['thicknes_11'],data['thicknes_12'],data['thicknes_13'],data['thicknes_14'],data['thicknes_15'],
# data['others_1'],data['others_2'],data['others_3'],data['others_4'],data['others_5'],data['others_6'],data['others_7'],data['others_8'],data['others_9'],data['others_10'],data['others_11'],data['others_12'],data['others_13'],data['others_14'],data['others_15'],
# data['others_amount_1'],data['others_amount_2'],data['others_amount_3'],data['others_amount_4'],data['others_amount_5'],data['others_amount_6'],data['others_amount_7'],data['others_amount_8'],data['others_amount_9'],data['others_amount_10'],data['others_amount_11'],data['others_amount_12'],data['others_amount_13'],data['others_amount_14'],data['others_amount_15']











# def Insert_basic_data(data):
#     SQL = """INSERT INTO save_basic_data (worknum,case_name,company_name,phone,client_name,worktime,cleanuptime,workaddress,pack,transport,cemployee1,cemployee2,cemployee3,cemployee4,cemployee5,crossbar_width,crossbar_amount,crossbar_remark,150shelter,180shelter,iron_Shelter_amount,iron_Shelter_remark,paper_Shelter_height,paper_Shelter_amount,paper_Shelter_remark,stand_style,stand_amount,stand_remark,rent1,rent2,remark)
#              VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (data['worknum']  , data['case_name'] , data['company_name'] , data['phone'] ,data['client_name'] , data['worktime'] , data['cleanuptime'] , data['workaddress'] , data['pack'] , data['transport'] , data['cemployee1'] , data['cemployee2'] , data['cemployee3'] , data['cemployee4'] , data['cemployee5'] , data['crossbar_width'] , data['crossbar_amount'] , data['crossbar_remark'] , str(data['150shelter']) , str(data['180shelter']) , data['iron_Shelter_amount'] , data['iron_Shelter_remark'] , data['paper_Shelter_height'] , data['paper_Shelter_amount'] , data['paper_Shelter_remark'] , data['stand_style'] , data['stand_amount'] , data['stand_remark'] , data['rent1'] , data['rent2'] , data['remark'])

#     cursor.execute(SQL)
#     connection.commit()




# def Insert_central_data(data):
    # SQL = """INSERT INTO save_central_data(worknum,
    # comboBox_product_1,comboBox_product_2,comboBox_product_3,comboBox_product_4,comboBox_product_5,comboBox_product_6,comboBox_product_7,comboBox_product_8,comboBox_product_9,comboBox_product_10,comboBox_product_11,comboBox_product_12,comboBox_product_13,comboBox_product_14,comboBox_product_15,
    # lineEdit_width_1,lineEdit_width_2,lineEdit_width_3,lineEdit_width_4,lineEdit_width_5,lineEdit_width_6,lineEdit_width_7,lineEdit_width_8,lineEdit_width_9,lineEdit_width_10,lineEdit_width_11,lineEdit_width_12,lineEdit_width_13,lineEdit_width_14,lineEdit_width_15,
    # lineEdit_height_1,lineEdit_height_2,lineEdit_height_3,lineEdit_height_4,lineEdit_height_5,lineEdit_height_6,lineEdit_height_7,lineEdit_height_8,lineEdit_height_9,lineEdit_height_10,lineEdit_height_11,lineEdit_height_12,lineEdit_height_13,lineEdit_height_14,lineEdit_height_15,
    # lineEdit_amount_1,lineEdit_amount_2,lineEdit_amount_3,lineEdit_amount_4,lineEdit_amount_5,lineEdit_amount_6,lineEdit_amount_7,lineEdit_amount_8,lineEdit_amount_9,lineEdit_amount_10,lineEdit_amount_11,lineEdit_amount_12,lineEdit_amount_13,lineEdit_amount_14,lineEdit_amount_15,
    # comboBox_material_1,comboBox_material_2,comboBox_material_3,comboBox_material_4,comboBox_material_5,comboBox_material_6,comboBox_material_7,comboBox_material_8,comboBox_material_9,comboBox_material_10,comboBox_material_11,comboBox_material_12,comboBox_material_13,comboBox_material_14,comboBox_material_15,
    # comboBox_process_1,comboBox_process_2,comboBox_process_3,comboBox_process_4,comboBox_process_5,comboBox_process_6,comboBox_process_7,comboBox_process_8,comboBox_process_9,comboBox_process_10,comboBox_process_11,comboBox_process_12,comboBox_process_13,comboBox_process_14,comboBox_process_15,
    # comboBox_plate_1,comboBox_plate_2,comboBox_plate_3,comboBox_plate_4,comboBox_plate_5,comboBox_plate_6,comboBox_plate_7,comboBox_plate_8,comboBox_plate_9,comboBox_plate_10,comboBox_plate_11,comboBox_plate_12,comboBox_plate_13,comboBox_plate_14,comboBox_plate_15,
    # comboBox_thicknes_1,comboBox_thicknes_2,comboBox_thicknes_3,comboBox_thicknes_4,comboBox_thicknes_5,comboBox_thicknes_6,comboBox_thicknes_7,comboBox_thicknes_8,comboBox_thicknes_9,comboBox_thicknes_10,comboBox_thicknes_11,comboBox_thicknes_12,comboBox_thicknes_13,comboBox_thicknes_14,comboBox_thicknes_15,
    # comboBox_others_1,comboBox_others_2,comboBox_others_3,comboBox_others_4,comboBox_others_5,comboBox_others_6,comboBox_others_7,comboBox_others_8,comboBox_others_9,comboBox_others_10,comboBox_others_11,comboBox_others_12,comboBox_others_13,comboBox_others_14,comboBox_others_15,
    # lineEdit_others_amount_1,lineEdit_others_amount_2,lineEdit_others_amount_3,lineEdit_others_amount_4,lineEdit_others_amount_5,lineEdit_others_amount_6,lineEdit_others_amount_7,lineEdit_others_amount_8,lineEdit_others_amount_9,lineEdit_others_amount_10,lineEdit_others_amount_11,lineEdit_others_amount_12,lineEdit_others_amount_13,lineEdit_others_amount_14,lineEdit_others_amount_15)
    # VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',)"""% (data['worknum'],data['product_1'],data['product_2'],data['product_3'],data['product_4'],data['product_5'],data['product_6'],data['product_7'],data['product_8'],data['product_9'],data['product_10'],data['product_11'],data['product_12'],data['product_13'],data['product_14'],data['product_15'],data['width_1'],data['width_2'],data['width_3'],data['width_4'],data['width_5'],data['width_6'],data['width_7'],data['width_8'],data['width_9'],data['width_10'],data['width_11'],data['width_12'],data['width_13'],data['width_14'],data['width_15'],data['height_1'],data['height_2'],data['height_3'],data['height_4'],data['height_5'],data['height_6'],data['height_7'],data['height_8'],data['height_9'],data['height_10'],data['height_11'],data['height_12'],data['height_13'],data['height_14'],data['height_15'],data['amount_1'],data['amount_2'],data['amount_3'],data['amount_4'],data['amount_5'],data['amount_6'],data['amount_7'],data['amount_8'],data['amount_9'],data['amount_10'],data['amount_11'],data['amount_12'],data['amount_13'],data['amount_14'],data['amount_15'],data['material_1'],data['material_2'],data['material_3'],data['material_4'],data['material_5'],data['material_6'],data['material_7'],data['material_8'],data['material_9'],data['material_10'],data['material_11'],data['material_12'],data['material_13'],data['material_14'],data['material_15'],data['process_1'],data['process_2'],data['process_3'],data['process_4'],data['process_5'],data['process_6'],data['process_7'],data['process_8'],data['process_9'],data['process_10'],data['process_11'],data['process_12'],data['process_13'],data['process_14'],data['process_15'],data['plate_1'],data['plate_2'],data['plate_3'],data['plate_4'],data['plate_5'],data['plate_6'],data['plate_7'],data['plate_8'],data['plate_9'],data['plate_10'],data['plate_11'],data['plate_12'],data['plate_13'],data['plate_14'],data['plate_15'],data['thicknes_1'],data['thicknes_2'],data['thicknes_3'],data['thicknes_4'],data['thicknes_5'],data['thicknes_6'],data['thicknes_7'],data['thicknes_8'],data['thicknes_9'],data['thicknes_10'],data['thicknes_11'],data['thicknes_12'],data['thicknes_13'],data['thicknes_14'],data['thicknes_15'],data['others_1'],data['others_2'],data['others_3'],data['others_4'],data['others_5'],data['others_6'],data['others_7'],data['others_8'],data['others_9'],data['others_10'],data['others_11'],data['others_12'],data['others_13'],data['others_14'],data['others_15'],data['others_amount_1'],data['others_amount_2'],data['others_amount_3'],data['others_amount_4'],data['others_amount_5'],data['others_amount_6'],data['others_amount_7'],data['others_amount_8'],data['others_amount_9'],data['others_amount_10'],data['others_amount_11'],data['others_amount_12'],data['others_amount_13'],data['others_amount_14'],data['others_amount_15'])

    # cursor.execute(SQL)
    # connection.commit