import sys
from unittest import result
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tkinter import *

import project as ui
import pymysql
import openpyxl


class Main(QMainWindow, ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    root = Tk()
    monitor_height = root.winfo_screenheight()
    monitor_width = root.winfo_screenwidth()
  
    print("width x height = %d x %d (pixels)" %(monitor_width, monitor_height))
 


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())