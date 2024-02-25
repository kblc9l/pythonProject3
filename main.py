
import sys
import sqlite3
from PyQt5 import uic

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)

        self.con = sqlite3.connect("coffee.sqlite")
        self.titles = None

        self.setup_table()

    def setup_table(self):
        cur = self.con.cursor()
        result = None

        result = cur.execute(
            f"""SELECT coffee.name, coffee.roasting_lvl, coffee.beans, coffee.taste, coffee.price, coffee.volume 
                        FROM coffee""").fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = ["Название", "Степень обжарки", "В зернах?", "Описание вкуса", "Стоимость пачки", "Объем пачки"]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
