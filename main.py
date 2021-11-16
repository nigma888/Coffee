from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sqlite3
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.show_table()

    def show_table(self):
        req = f"""SELECT * FROM coffee"""
        items = self.con.cursor().execute(req).fetchall()
        self.tableWidget.setColumnCount(len(items[0]))
        self.tableWidget.setRowCount(len(items))
        self.tableWidget.setHorizontalHeaderLabels(['id', 'название', 'сорт', 'обжарка',
                                                    'молотый/в зернах', 'описание вкуса', 'цена',
                                                    'объем'])
        for i, val in enumerate(items):
            for k, elem in enumerate(val):
                self.tableWidget.setItem(i, k, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())