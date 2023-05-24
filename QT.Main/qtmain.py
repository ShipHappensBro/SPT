import sys
import AutorizationWin
import mainwindow
import os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtSql import QSqlDatabase
import win32security
import subprocess
import qrcode
import copy
import socket
import random
import string
import sqlite3

current_domain=subprocess.run(["powershell.exe", "(Get-CimInstance Win32_ComputerSystem).Domain"], stdout=subprocess.PIPE, text=True).stdout.strip()

class MainWindow(QtWidgets.QMainWindow,mainwindow.Ui_MainWindow,AutorizationWin.Ui_AutorizationWindow):

    def __init__(self,parent=None):
        con=QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName('inv.db')
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.qr_generator.clicked.connect(self.bc_inv)
        self.print_btn.clicked.connect(self.print)
        self.con=sqlite3.connect('inv.db',5,1,'DEFERRED',True,sqlite3.Connection,True)
        self.cur=self.con.cursor()
    def bc_inv(self):

        qr=qrcode.QRCode(version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                        )
        self.rand=''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for n in range(10))
        qr.add_data(self.rand)
        qr.make(fit=True)
        image = qr.make_image(fill_color="black",
                               back_color="white"
                               )
        image.save(self.rand+'.png')
        self.info=(self.SecondName.text(),
                   self.number_workstation_btn.text(),
                   self.department.currentText(),
                   self.rand)
        self.QR.setPixmap(QtGui.QPixmap(self.rand+'.png'))
        self.print_btn.setEnabled(True)
        try:
            self.cur.execute("INSERT INTO inv (Name,Number,Department,QR) VALUES (?,?,?,?)",self.info)
            self.con.commit()
        finally:
             print('Done')
    def print(self):
            try:
                os.startfile(self.rand+".png",
                        "print")
            except:
                 pass


class AutorizationWindow(QtWidgets.QMainWindow, AutorizationWin.Ui_AutorizationWindow):
        
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