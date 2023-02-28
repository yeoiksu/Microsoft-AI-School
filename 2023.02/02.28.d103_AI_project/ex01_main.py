import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

'''ui폼 받아오기'''
# Main
form = resource_path('ex01.ui')
form_class = uic.loadUiType(form)[0]
# Email
form_2 = resource_path('ex02_email.ui')
form_email = uic.loadUiType(form_2)[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # ''' pushButton_email버튼 클릭 시 testclick 함수 실행'''
        # self.pushButton_email.clicked.connect(self.email_clicked)
		
    # 실행될 함수    
    def email_clicked(self):
        # self.hide()                     # 메인윈도우 숨김
        self.second = email_form()    #
        self.second.exec()              # 두번째 창을 닫을 때 까지 기다림
        self.show()  

    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


class email_form(QDialog,QWidget,form_email):
    def __init__(self):
        super(email_form,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)

    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    
    '''상태표시줄'''
    myWindow.statusBar()
    myWindow.statusBar().showMessage("위험 비행물 감지 시스템 동작합니다.")
    app.exec_()