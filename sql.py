import sys
import pymysql
from project import Ui_Form as ui
import main
connection = pymysql.connect(host='192.168.101.59',
                             port=3306,
                             user='root',
                             passwd='root',
                             database='work_order',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
#print(bool(connection))
cursor = connection.cursor()


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

def company_name_change():
    SQL="""SELECT * FROM client WHERE name = '%s'""" % ui.comboBox_company_name.currentText()
    print(SQL)
    cursor.execute(SQL)
    connection.commit()
    data = cursor.fetchall()        
    print(data)


    