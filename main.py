import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic
import sqlite3


class Coffee(QMainWindow):
    def __init__(self):
        super(Coffee, self).__init__()

        uic.loadUi('design.ui', self)
        self.open_table()

    def open_table(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM coffe_info").fetchall()
        self.tableWidget.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
