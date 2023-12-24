from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from Admin import Ui_AdminWindow
from API import API
from datetime import datetime

class AdminLK(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_AdminWindow()
        self.ui.setupUi(self)
        self.ui.AddOrderButton.clicked.connect(self.add_order)
        self.ui.OrderReadyButton.clicked.connect(self.order_ready)


    def set_api(self, address, password):
        self.api = API(address, password)

    def redraw(self):
        self.orders_list = self.api.retorders()
        self.orders_count = len(self.orders_list)
        self.checks = [0] * 20
        self.ui.tableWidget_2.setRowCount(self.orders_count)
        for i in range(0, self.orders_count):
            self.ui.tableWidget_2.setItem(i, 0, QtWidgets.QTableWidgetItem(self.orders_list[self.orders_count-i-1][0]))
            self.ui.tableWidget_2.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.orders_list[self.orders_count-i-1][1])))
            start_time = datetime.fromtimestamp(float(self.orders_list[self.orders_count-i-1][3]))
            self.ui.tableWidget_2.setItem(i, 2, QtWidgets.QTableWidgetItem(str(start_time)[11:]))
            self.ui.tableWidget_2.setItem(i, 3, QtWidgets.QTableWidgetItem(str(self.orders_list[self.orders_count-i-1][4] + 1)))
            self.ui.tableWidget_2.setItem(i, 4, QtWidgets.QTableWidgetItem(self.orders_list[self.orders_count-i-1][2]))
        for i in range(0, 20):
            self.checks[i] = self.api.GetTableInfo(i)[0]
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.checks[i])))  # это надо добавить в кнопку Заказ готов
            self.ui.tableWidget.item(i, 1).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

    def add_order(self):
        table_num = int(self.ui.lineEdit.text())
        dish_name = self.ui.lineEdit_2.text()
        price = int(self.ui.lineEdit_3.text())
        try:
            self.api.AddOrder(table_num - 1, dish_name, price)
            self.redraw()
        except:
            self.errorMsg = QtWidgets.QErrorMessage()
            self.errorMsg.setWindowTitle('Ошибка добавления заказа')
            self.errorMsg.showMessage('Проверьте корректность введённых данных!')

    def order_ready(self):
        self.orders_list = self.api.retorders()
        self.orders_count = len(self.orders_list)
        self.api.OrderIsReady()
        table_num = int(self.orders_list[self.orders_count-1][4])
        self.checks[table_num] += self.orders_list[self.orders_count-1][1]
        self.ui.tableWidget.setItem(table_num, 1, QtWidgets.QTableWidgetItem(str(self.checks[table_num])))  # это надо добавить в кнопку Заказ готов
        self.ui.tableWidget.item(table_num, 1).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.redraw()




