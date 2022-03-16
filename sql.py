import sys

from project import Ui_Form as ui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tkinter import *


import pymysql
import project as ui

connection = pymysql.connect(host='192.168.101.59',
                             port=3306,
                             user='root',
                             passwd='root',
                             database='work_order',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
#print(bool(connection))
cursor = connection.cursor()

def create_table():
    SQL="""CREATE TABLE central_data(
        `product` char(50),
        `material` char(50),
        `process` char(50),
        `plate` char(50),
        `plate_thickness` char(50),
        `others` char(50)
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




