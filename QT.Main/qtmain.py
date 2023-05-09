import sys
import design
import mainwindow
import os
from PyQt6 import QtCore, QtGui, QtWidgets
import win32security
import subprocess

current_domain=subprocess.run(["powershell.exe", "(Get-CimInstance Win32_ComputerSystem).Domain"], stdout=subprocess.PIPE, text=True).stdout.strip()

class MainWindow(QtWidgets.QMainWindow,mainwindow.Ui_MainWindow):
     def __init__(self,parent=None):
          super(MainWindow,self).__init__()
          self.setupUi(self)


class AutorizationWindow(QtWidgets.QMainWindow, design.Ui_AutorizationWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
            self.retranslateUi(self)
            self.groupBox.setTitle("АВТОРИЗАЦИЯ (" + 
                    current_domain +"\\"+ 
                    os.getlogin()+')'
                    )
            self.login_input.setText(os.getlogin())
            self.autorizationbtn.clicked.connect(self.autorization)


        def autorization(self):
            print(self.login_input.text())
            print(self.password_input.text())
            try:
                win32security.LogonUser(
                    self.login_input.text(),
                    current_domain,
                    self.password_input.text(),
                    win32security.LOGON32_LOGON_NETWORK,
                    win32security.LOGON32_PROVIDER_DEFAULT)
            except:
                 print('Something wrong')
                 self.badautorization.setText("НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ")
            else:
                print('ok')
                self.into_main_menu()
        def into_main_menu(self):
            self.mainwindow=MainWindow(self)
            self.hide()
            self.mainwindow.show()
                 


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AutorizationWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()