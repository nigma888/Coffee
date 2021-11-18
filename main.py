from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog
import sqlite3
import sys
from addEditCoffeeForm import Ui_Dialog
from main_window import Ui_MainWindow


class AddEditCoffeeForm(QDialog, Ui_Dialog):
    def __init__(self, parent, status):
        super().__init__()
        self.setupUi(self)
        self.status = status
        self.parent = parent
        self.to_need_visible()
        if self.status == 1:
            self.update_values()

        self.show()

        self.pushButton.clicked.connect(self.btn_accept)

    def check_cor_data(self):
        if self.lineEdit.text() and self.lineEdit_2.text() and \
                self.lineEdit_3.text() and self.lineEdit_4.text():
            return True
        else:
            return False

    def to_need_visible(self):
        if self.status == 0:
            self.pushButton.setText('Добавить')
            self.comboBox.setVisible(False)
            self.label.setVisible(False)
            self.comboBox_2.addItems(['молотый', 'зерна'])
        elif self.status == 1:
            self.pushButton.setText('Изменить')
            self.comboBox.addItems(map(str, self.parent.get_all_id()))
            self.comboBox_2.addItems(['молотый', 'зерна'])
            self.comboBox.currentTextChanged.connect(self.update_values)

    def update_values(self):
        id = self.comboBox.currentText()
        values = self.parent.con.cursor().execute(f"""SELECT * FROM coffee WHERE id = {id}""")\
            .fetchone()
        self.lineEdit.setText(values[1])
        self.lineEdit_2.setText(values[2])
        self.lineEdit_3.setText(values[3])
        self.comboBox_2.setCurrentText(values[4])
        self.lineEdit_4.setText(values[5])
        self.spinBox.setValue(values[6])
        self.spinBox_2.setValue(values[7])

    def btn_accept(self):
        self.label_error.clear()
        if self.check_cor_data():
            self.do_req()
        else:
            self.label_error.setText('Некорректные данные')

    def do_req(self):
        name = self.lineEdit.text()
        sort = self.lineEdit_2.text()
        roasting = self.lineEdit_3.text()
        type = self.comboBox_2.currentText()
        taste = self.lineEdit_4.text()
        price = self.spinBox.value()
        size = self.spinBox_2.value()
        if self.status == 0:
            self.parent.con.cursor().execute(f"""INSERT INTO coffee(title, sort, roasting, type,
                                                taste, price, size)
                                                values('{name}', '{sort}', '{roasting}', '{type}',
                                                '{taste}', '{price}', '{size}')""")
        elif self.status == 1:
            id = self.comboBox.currentText()
            self.parent.con.cursor().execute(f"""UPDATE coffee 
                                                SET title = '{name}', sort = '{sort}', roasting = 
                                                '{roasting}', type = '{type}', taste = '{taste}',
                                                price = '{price}', size = '{size}'
                                                WHERE id = '{id}'""")
        self.parent.con.commit()
        self.parent.show_table()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('release/data/coffee.sqlite')
        self.show_table()
        self.pushButton.clicked.connect(self.add_row)
        self.pushButton_2.clicked.connect(self.edit_row)

    def get_all_id(self):
        return [i[0] for i in self.con.cursor().execute(f"""SELECT id FROM coffee""").fetchall()]

    def open_second_win(self, status):
        self.w2 = AddEditCoffeeForm(self, status)

    def add_row(self):
        self.open_second_win(0)

    def edit_row(self):
        self.open_second_win(1)

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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())