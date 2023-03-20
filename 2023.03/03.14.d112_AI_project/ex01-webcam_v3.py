import cv2, threading, sys, numpy as np, torch, time, argparse, os, glob
from torch import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from important_data import *
from mysql.connector.locales.eng import client_error
# from yolov8_tracking_V4 import track

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

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

################################################################################################################

# Ui 디자인 작업 중
class Ui_MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        '''Ui 디자인'''
        back_Image = QImage("pics/background.png")
        size_Image = back_Image.scaled(QSize(1111, 653))
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap(size_Image))) # <= 원하시는 사진
        self.setPalette(palette)
        self.date = QDate.currentDate()
        self.setupUi(self)

        ''' 웹캠 동작(종료)시키는 클릭 이벤트 처리 연결'''
        self.pushButton_cctv_on.clicked.connect(self.live_webcam_click_on)  # 동작
        self.pushButton_cctv_off.clicked.connect(self.live_webcam_click_off) # 종료 

        # '''Live Webcam 공간 부분''' --> 무쓸모로 판명
        self.box_webcam = QtWidgets.QGroupBox(self.centralwidget)
        self.box_webcam.setGeometry(QtCore.QRect(320, 50, 770, 500)) # 좌측 상단 X좌표, 좌측 상단 Y좌표, X로부터 우측으로의 거리, Y로부터 아래쪽으로의 거리
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.box_webcam.setFont(font)
        self.box_webcam.setObjectName("box_webcam")

        ''' 실제 카메라 화면 출력 부분'''
        self.frame = QLabel(self.box_webcam)
        # self.frame.setGeometry(QtCore.QRect(320, 50, 761, 451))
        self.frame.setObjectName("frame")
        # self.camera = None # 필요 없음
        # self.timer = QTimer() # 필요 없음
        # self.frame_rate = 60 # 필요 없음

    '''on 버튼 눌렀을 시 웹캠 시작'''
    def live_webcam_click_on(self) :
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
        self.frame.show()
        while True:
            ret, img = cap.read()
            if not ret:
                break
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img.shape
            bytesPerLine = ch * w
            qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.frame.setPixmap(pixmap)
            QtWidgets.QApplication.processEvents()
            # print(self.frame)
        cap.release()

    '''off 버튼 눌렀을 시 웹캠 종료'''
    def live_webcam_click_off(self) :
        self.frame.clear() 
        QMessageBox.about(self, 'App Alert', '연결된 카메라를 끕니다.')
        self.frame.hide() # 정확히는 숨김 처리 --> 노트

        
    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    # 2번 버튼
    ''' email버튼 클릭 시 이메일 창 활성화'''    
    def email_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = email_form()
        self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        self.show() 

    '''3번 버튼 클릭 시 연결'''
    def connect_powerbi(self):
        import webbrowser
        webbrowser.open(POWER_BI_LINK)

    # 3번 버튼
    '''Data Analysis 버튼 클릭 시 DB창으로 이동'''
    def bi_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = self.connect_powerbi() 
        # self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        # self.show() 

################################################################################################################

'''2번 기능 페이지'''
class email_form(QDialog,QWidget,form_email):
    def __init__(self):
        super(email_form,self).__init__()
        back_Image = QImage("./pics/background.png")
        size_Image = back_Image.scaled(QSize(1111, 560))
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap(size_Image))) # <= 원하시는 사진
        self.setPalette(palette)        
        
        self.initUi()
        self.show()

        print(self.info_comboBox.currentText(), '모드 입니다.')
        self.info_comboBox.currentIndexChanged.connect(self.printShtname)

    def initUi(self):
        self.setupUi(self)
        '''버튼 아이콘'''
        # enter
        capture_pixmap = QStyle.StandardPixmap.SP_DialogApplyButton
        capture_icon = myWindow.style().standardIcon(capture_pixmap)
        self.enter_pushButton.setIcon(capture_icon)

        # exit
        exit_pixmap = QStyle.StandardPixmap.SP_MessageBoxCritical
        exit_icon = myWindow.style().standardIcon(exit_pixmap)
        self.exit_pushButton.setIcon(exit_icon)
        
    '''CUSTOMER_TABLE 연결'''
    def connect_table(self):
        from mysql.connector import connection
        conn = connection.MySQLConnection(
            user     = USER,
            password = PASSWORD,
            host     = HOST,
            database = DATABASE
            )
        return conn

    '''info 입력/검색/삭제 부분 업데이트 중'''
    def reset(self):
        self.id_text.clear()
        self.name_text.clear()
        self.email_text.clear()  

    def printShtname(self): # 콤보박스 상태 변경 시 터미널에 출력하는 기능 함수.
        print(self.info_comboBox.currentText(),'모드 입니다.')

    def add_info(self): 
        self.id      = self.id_text.text()    # 아이디
        self.name    = self.name_text.text()  # 이름
        self.email   = self.email_text.text() # 이메일
        self.fn_type = self.info_comboBox.currentText()  # 콤보 박스: 입력, 검색, 삭제    
        set_flag = False

        ## 1. 검색
        if self.fn_type == ' SELECT':
            if self.id or self.name or self.email:
                select_count = self.countData()
                if select_count > 0 :
                    set_flag = True
                    id_list, name_list, email_list = self.SelectData()
                    QMessageBox.information(self, "Select 결과", f"{select_count}개의 데이터를 출력합니다.")
                else:
                    QMessageBox.critical(self, "입력 오류", "입력하신 정보의 데이터가 없습니다")
            else:
                QMessageBox.critical(self, "입력 오류", "정보를 입력해주세요!")
        
        ## 2. 입력
        elif self.fn_type == ' INSERT':
            if self.id and self.name and self.email:
                set_flag = True
                self.InsertData()
            # close event 처럼 하나 필요 !!!
            else:
                QMessageBox.critical(self, "입력 오류", "모든 정보를 입력해주세요!")
                print("모든 정보를 입력해주세요!")

        ## 3. 삭제
        elif self.fn_type == ' DELETE':
            msg = '정말 삭제하시겠습니까?'
            buttonReply = QMessageBox.question(self, '삭제', msg, QMessageBox.Yes | QMessageBox.No)

            # 삭제 메세지에서 YES선택 시
            if buttonReply == QMessageBox.Yes:
                # 3개의 데이터 중 하나만이라도 존재하면
                if self.id and self.name and self.email:
                    delete_count = self.countData()
                    # delete할 행이 있다면
                    if delete_count > 0 :
                        set_flag = self.DeleteData()
                        QMessageBox.information(self, "Delete 결과", f"{delete_count}개의 데이터를 삭제합니다.")
                    # delete할 행이 없다면
                    else:
                        QMessageBox.critical(self, "입력 오류", "입력하신 정보의 데이터가 없습니다.\n데이터를 다시 확인 후 입력해주세요")
                else:
                    QMessageBox.critical(self, "입력 오류", "정보를 다시 입력해주세요!")     
            else: 
                buttonReply == QMessageBox.No
                QMessageBox.critical(self, "취소", "취소되었습니다!")
        ## info table에 입력할 데이터
        if set_flag:
            if self.fn_type == ' DELETE' or self.fn_type == ' INSERT':
                row = self.info_table.rowCount()
                self.info_table.insertRow(row)
                self.info_table.setItem(row, 0, QTableWidgetItem(self.fn_type + f" 완료"))
                self.info_table.setItem(row, 1, QTableWidgetItem(self.id))
                self.info_table.setItem(row, 2, QTableWidgetItem(self.name))
                self.info_table.setItem(row, 3, QTableWidgetItem(self.email))
            elif self.fn_type == ' SELECT':
                for index, item in enumerate(id_list):
                    row = self.info_table.rowCount()
                    self.info_table.insertRow(row)
                    self.info_table.setItem(row, 0, QTableWidgetItem(self.fn_type + f" {index+1} 완료"))
                    self.info_table.setItem(row, 1, QTableWidgetItem(id_list[index]))
                    self.info_table.setItem(row, 2, QTableWidgetItem(name_list[index]))
                    self.info_table.setItem(row, 3, QTableWidgetItem(email_list[index]))
        self.reset()

    '''CUSTOMER_TABLE 연결'''
    def countData(self):
        conn = self.connect_table()
        cur = conn.cursor()    
        # COUNT 문
        if self.fn_type == " SELECT":
            # 1 0 0
            if (len(self.id) != 0) and (len(self.name) == 0) and (len(self.email) == 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}';'''
            # 0 1 0
            elif (len(self.id) == 0) and (len(self.name) != 0 ) and (len(self.email) == 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `name` = '{str(self.name)}';'''
            # 0 0 1
            elif (len(self.id) == 0) and (len(self.name) == 0) and (len(self.email) != 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `email` = '{str(self.email)}';'''
            # 1 1 0
            elif (len(self.id) != 0) and (len(self.name) != 0) and (len(self.email) == 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}';'''
            # 1 0 1
            elif (len(self.id) != 0) and (len(self.name) == 0) and (len(self.email) != 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}' AND `email`='{str(self.email)}';'''
            # 0 1 1
            elif (len(self.id) == 0) and (len(self.name) != 0) and (len(self.email) != 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `name` = '{str(self.name)}' AND `email`='{str(self.email)}';'''
            # 1 1 1
            elif (len(self.id) != 0) and (len(self.name) != 0) and (len(self.email) != 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` 
                WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}' AND `email`='{str(self.email)}';'''

        elif self.fn_type == " DELETE":
            SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}`
            WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}' AND `email`='{str(self.email)}';'''

        cur.execute(SQL_COUNT)
        count = cur.fetchone()[0]
        conn.commit()
        conn.close()

        return count

    ''' Select Data'''
    def SelectData(self):
        id_list, name_list, email_list = [], [], []
        conn = self.connect_table()
        cur = conn.cursor()
        # SELECT 문
        # 1 0 0
        if (len(self.id) != 0) and (len(self.name) == 0) and (len(self.email) == 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}';'''
        # 0 1 0
        elif (len(self.id) == 0) and (len(self.name) != 0 ) and (len(self.email) == 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `name` = '{str(self.name)}';'''
        # 0 0 1
        elif (len(self.id) == 0) and (len(self.name) == 0) and (len(self.email) != 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `email` = '{str(self.email)}';'''
        # 1 1 0
        elif (len(self.id) != 0) and (len(self.name) != 0) and (len(self.email) == 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}';'''
        # 1 0 1
        elif (len(self.id) != 0) and (len(self.name) == 0) and (len(self.email) != 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}' AND `email`='{str(self.email)}';'''
        # 0 1 1
        elif (len(self.id) == 0) and (len(self.name) != 0) and (len(self.email) != 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `name` = '{str(self.name)}' AND `email`='{str(self.email)}';'''
        # 1 1 1
        elif (len(self.id) != 0) and (len(self.name) != 0) and (len(self.email) != 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` 
            WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}' AND `email`='{str(self.email)}';'''

        cur.execute(SQL_SELECT)
        result = cur.fetchall()
        for i in result:
            id_list.append(i[1])
            name_list.append(i[2])
            email_list.append(i[3])

        conn.commit()
        conn.close()

        return id_list, name_list, email_list

    ''' Insert Data'''
    def InsertData(self):
        conn = self.connect_table()
        cur = conn.cursor()
        SQL_INSERT = f'''INSERT INTO `{TABLE_CUSTOMER}`(id, name, email) 
    VALUES ('{str(self.id)}', '{str(self.name)}', '{str(self.email)}');'''
        cur.execute(SQL_INSERT)
        conn.commit()
        conn.close()
        
    ''' Delete Data'''
    def DeleteData(self):
        conn = self.connect_table()
        cur = conn.cursor()

        SQL_DELETE = f'''DELETE FROM `{TABLE_CUSTOMER}` 
        WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}' AND `email`='{str(self.email)}';'''
        cur.execute(SQL_DELETE)
        conn.commit()
        if cur.rowcount >= 1:
            conn.close()
            return True
        else:
            conn.close()
            return False

    '''X 버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore() 
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWindow = Ui_MainWindow()
    myWindow.show()

    '''상태표시줄'''
    # myWindow.statusBar()
    DATE = myWindow.date.toString(Qt.DefaultLocaleLongDate) + " "
    TIME = QTime.currentTime().toString()
    MESSAGE = " 위험비행물 감지시스템 동작 중...   "
    myWindow.statusBar().showMessage(MESSAGE + DATE + TIME)

    app.exec_()

