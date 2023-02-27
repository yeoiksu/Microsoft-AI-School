# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '02_email.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton , QMessageBox

class MyWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1173, 739)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.info_frame = QtWidgets.QFrame(self.centralwidget)
        self.info_frame.setGeometry(QtCore.QRect(50, 90, 721, 431))
        self.info_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.info_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_frame.setObjectName("info_frame")
        self.info_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.info_groupBox.setGeometry(QtCore.QRect(20, 60, 761, 511))
        self.info_groupBox.setObjectName("info_groupBox")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(800, 90, 94, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.name_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.name_textEdit.setGeometry(QtCore.QRect(870, 150, 281, 31))
        self.name_textEdit.setObjectName("name_textEdit")
        self.id_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.id_textEdit.setGeometry(QtCore.QRect(870, 220, 281, 31))
        self.id_textEdit.setObjectName("id_textEdit")
        self.email_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.email_textEdit.setGeometry(QtCore.QRect(870, 290, 281, 31))
        self.email_textEdit.setObjectName("email_textEdit")
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(810, 160, 41, 16))
        self.name_label.setObjectName("name_label")
        self.id_label = QtWidgets.QLabel(self.centralwidget)
        self.id_label.setGeometry(QtCore.QRect(810, 230, 51, 16))
        self.id_label.setObjectName("id_label")
        self.email_label = QtWidgets.QLabel(self.centralwidget)
        self.email_label.setGeometry(QtCore.QRect(810, 300, 51, 16))
        self.email_label.setObjectName("email_label")
        self.info_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.info_pushButton.setGeometry(QtCore.QRect(810, 370, 341, 28))
        self.info_pushButton.setObjectName("info_pushButton")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(790, 60, 371, 511))
        self.groupBox.setObjectName("groupBox")
        self.exit_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.exit_pushButton.setGeometry(QtCore.QRect(260, 470, 93, 28))
        self.exit_pushButton.setObjectName("exit_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1173, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.info_groupBox.setTitle(_translate("MainWindow", "INFO_OUTPUT"))
        self.comboBox.setItemText(0, _translate("MainWindow", "입력"))
        self.comboBox.setItemText(1, _translate("MainWindow", "검색"))
        self.comboBox.setItemText(2, _translate("MainWindow", "삭제"))
        self.name_label.setText(_translate("MainWindow", "이름"))
        self.id_label.setText(_translate("MainWindow", "아이디"))
        self.email_label.setText(_translate("MainWindow", "이메일"))
        self.info_pushButton.setText(_translate("MainWindow", "입력"))
        self.groupBox.setTitle(_translate("MainWindow", "INFO"))
        self.exit_pushButton.setText(_translate("MainWindow", "종료"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
    
        
        
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

