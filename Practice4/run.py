from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from Auth import Ui_MainWindow
from adminLK import AdminLK
from API import API

class Auth(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.input_user)

    def input_user(self):
        address = self.ui.addressLine.text()
        password = self.ui.passwordLine.text()
        self.api = API(address, password)
        try:
            self.api.auth()
            if (address == '0xCae62C21d7A26B3c7057714BEa4111f4376B1f99'):
                self.open = AdminLK()
                self.open.set_api(address, password)
                self.open.redraw()
                self.open.show()
            self.close()
        except:
            self.errorMsg = QtWidgets.QErrorMessage()
            self.errorMsg.setWindowTitle('Ошибка авторизации')
            self.errorMsg.showMessage('Был введён неправильный логин или пароль')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Auth()
    myapp.show()

    sys.exit(app.exec())
