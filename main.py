import sys
import sqlite3
from PyQt5 import QtCore

from PyQt5.QtWidgets import QApplication, QWidget
from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeFor_ui import Ui_Form
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.info_form = None
        self.setupUi(self)

        self.con = sqlite3.connect("data/coffee.sqlite")
        self.titles = None

        self.setup_table()

        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.update)

    def setup_table(self):
        cur = self.con.cursor()
        result = None

        result = cur.execute(
            f"""SELECT coffee.id,coffee.name, coffee.roasting_lvl, coffee.beans, coffee.taste, coffee.price, coffee.volume 
                        FROM coffee""").fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = ["ID", "Название", "Степень обжарки", "В зернах?", "Описание вкуса", "Стоимость пачки",
                       "Объем пачки"]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add(self):
        self.info_form = CoffeeInfo("add", self.setup_table)
        self.info_form.show()

    def update(self):
        self.info_form = CoffeeInfo("upd", self.setup_table,
                                    [int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text()),
                                     str(self.tableWidget.item(self.tableWidget.currentRow(), 1).text()),
                                     str(self.tableWidget.item(self.tableWidget.currentRow(), 2).text()),
                                     str(self.tableWidget.item(self.tableWidget.currentRow(), 3).text()),
                                     str(self.tableWidget.item(self.tableWidget.currentRow(), 4).text()),
                                     str(self.tableWidget.item(self.tableWidget.currentRow(), 5).text()),
                                     str(self.tableWidget.item(self.tableWidget.currentRow(), 6).text())])
        self.info_form.show()


class CoffeeInfo(QWidget, Ui_Form):
    def __init__(self, type: str, update, update_data: list = None):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.save)

        self.con = sqlite3.connect("data/coffee.sqlite")
        self.type = type
        self.update = update

        if update_data:
            self.update_data = update_data
            self.lineEdit.setText(self.update_data[1])
            self.lineEdit_2.setText(self.update_data[2])

            index = self.comboBox.findText(self.update_data[3], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.comboBox.setCurrentIndex(index)

            self.lineEdit_3.setText(self.update_data[4])
            self.lineEdit_4.setText(self.update_data[5])
            self.lineEdit_5.setText(self.update_data[6])

        self.setupComboBox()

    def setupComboBox(self):
        self.comboBox.addItems(["Да", "Нет"])

    def save(self):
        if self.type == "add":
            if str(self.lineEdit.text()):
                cur = self.con.cursor()
                cur.execute(
                    f"""INSERT INTO coffee(name, roasting_lvl, beans, taste, price, volume) 
                    VALUES('{str(self.lineEdit.text())}', '{str(self.lineEdit_2.text())}', '{str(self.comboBox.currentText())}', 
                    '{str(self.lineEdit_3.text())}', '{str(self.lineEdit_4.text())}', '{str(self.lineEdit_5.text())}')""")
                self.con.commit()

                self.update()
                self.setupComboBox()
                self.hide()

        if self.type == "upd":
            cur = self.con.cursor()

            if str(self.lineEdit.text()):
                cur.execute(
                    f"""UPDATE coffee
                        SET name = '{str(self.lineEdit.text())}',
                        roasting_lvl = '{str(self.lineEdit_2.text())}',
                        beans = '{str(self.comboBox.currentText())}',
                        taste = '{str(self.lineEdit_3.text())}',
                        price = '{str(self.lineEdit_4.text())}',
                        volume = '{str(self.lineEdit_5.text())}'
                        WHERE id = {int(self.update_data[0])}""")
                self.con.commit()

                self.update()
                self.setupComboBox()
                self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
