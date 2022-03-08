import sys
from unittest import result
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tkinter import *

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

    SQL = """INSERT INTO client(name,full_name,phone,address,taxID)
             VALUES('228基金會','財團法人二二八事件紀念基金會','23326228','10066台北市南海路54號','97971614'),
             ('228共生','社團法人台灣共生青年協會','無','10351台北市大同區長安西路84號4樓之一','85202463')
          """
    
    cursor.execute(SQL)
    connection.commit()
    



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())