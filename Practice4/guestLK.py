import time
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from Guest import Ui_GuestWindow
from API import API

class GuestLK(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_GuestWindow()
        self.ui.setupUi(self)

        self.ui.takeATableButton.clicked.connect(self.get_table)
        self.ui.makeCheckButton.clicked.connect(self.make_check)
        self.ui.payNLeaveButton.clicked.connect(self.pay_n_leave)

    def set_api(self, address, password):
        self.api = API(address, password)

    def draw(self):
        self.table_num = -1
        for i in range(0,20):
            if self.api.GetTableInfo(i)[1] == self.api.current_user:
                self.table_num = i
        if self.table_num == -1:
            self.ui.tableNumLine.hide()
            self.ui.label_2.hide()
            self.ui.label_3.hide()
            self.ui.makeCheckButton.hide()
            self.ui.makeCheckButton.hide()
            self.ui.payNLeaveButton.hide()
            self.ui.orderSumLine.hide()
        else:
            self.ui.tableNumLine.show()
            self.ui.label_2.show()
            self.ui.label_3.show()
            self.ui.makeCheckButton.show()
            self.ui.makeCheckButton.show()
            self.ui.payNLeaveButton.show()
            self.ui.orderSumLine.show()
            self.ui.takeATableButton.hide()
            self.ui.tableNumLine.setText(str(self.table_num + 1))


    def get_table(self):
        try:
            self.api.GetATable()
            self.ui.tableNumLine.show()
            self.ui.label_2.show()
            self.ui.label_3.show()
            self.ui.makeCheckButton.show()
            self.ui.makeCheckButton.show()
            self.ui.payNLeaveButton.show()
            self.ui.orderSumLine.show()
            self.ui.takeATableButton.hide()
            self.table_num = self.api.last_gotten_table()
            self.ui.tableNumLine.setText(str(self.table_num+1))
        except:
            self.errorMsg = QtWidgets.QErrorMessage()
            self.errorMsg.setWindowTitle('Ошибка при занятии столика!')
            self.errorMsg.showMessage('Возможно Вы пытаетесь занять еще один стол!')
            self.close()

    def make_check(self):
        try:
            self.api.MakeCheck(self.table_num)
            self.ui.orderSumLine.setText(str(self.api.GetTableInfo(self.table_num)[0]))
            self.ui.orderSumLine.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        except:
            self.errorMsg = QtWidgets.QErrorMessage()
            self.errorMsg.setWindowTitle('Ошибка при вводе')
            self.errorMsg.showMessage('Что-то пошло не так')


    def pay_n_leave(self):
        try:
            value = int(self.ui.orderSumLine.text()) * 10**9
            self.api.PayNLeave(self.table_num, value)
            self.errorMsg = QtWidgets.QErrorMessage()
            self.errorMsg.setWindowTitle('Успешная оплата')
            self.errorMsg.showMessage('Вы оплатили свой счёт! Спасибо, приходите ещё!')
            time.sleep(3)
            self.close()
        except:
            self.errorMsg = QtWidgets.QErrorMessage()
            self.errorMsg.setWindowTitle('Ошибка оплаты')
            self.errorMsg.showMessage('У вас недостаточно средств для оплаты')


