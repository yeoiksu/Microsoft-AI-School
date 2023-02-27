import sys
# 기본적인 UI 구성요소를 제공하는 위젯 (클래스)들은 PyQt5.QtWidgets 모듈에 포함
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QToolTip, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QAction, QMenuBar, QMenu, QDesktopWidget, qApp
from PyQt5.QtWidgets import QSlider, QLabel

from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QCoreApplication, QDateTime, QDate, Qt

X_SIZE, Y_SIZE = 960, 540
x1, y1 = 30, 100
x_gap, y_gap = 120, 50
x2 = x1 + x_gap
x3 = x2 + x_gap
y2 = y1 + y_gap
y3 = y2 + y_gap

# 여기서 self는 MyApp 객체를 말합니다.
class MyApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        #### Font 설정
        QToolTip.setFont(QFont('SansSerif', 8))

    #### Window 창
        self.setWindowTitle('Harzardous Flying Object Detection')
        self.resize(X_SIZE, Y_SIZE)
        self.center()
        self.setWindowIcon(QIcon('./2023.02/02.15.d94_team_study/pics/airplane.png')) # window창에 아이콘 삽입하기

    #### Action      
        # 1. Edit Action
        editAction = QAction(QIcon('./2023.02/02.15.d94_team_study/pics/edit.png'), 'Edit', self)
        editAction.setShortcut("Ctrl+E")
        editAction.setStatusTip('Edit File')
        # saveAction.triggered.connect(self.file_save)        
        
        # 2. Save Action
        saveAction = QAction(QIcon('./2023.02/02.15.d94_team_study/pics/save.png'), 'Save', self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip('Save File')
        # saveAction.triggered.connect(self.file_save)

        # 3. print Action
        printAction = QAction(QIcon('./2023.02/02.15.d94_team_study/pics/print.png'), 'Print', self)
        printAction.setShortcut("Ctrl+P")
        printAction.setStatusTip('Print File')
        # saveAction.triggered.connect(self.file_save)

        # 3. Exit Action
        exitAction = QAction(QIcon('./2023.02/02.15.d94_team_study/pics/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

    #### Status bar
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

    #### Menubar
        # 1. File Menu
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File') # Creating menus using a QMenu object
        fileMenu.addAction(editAction) 
        fileMenu.addAction(saveAction) 
        fileMenu.addAction(printAction) 
        fileMenu.addAction(exitAction)  
        # fileMenu.addAction(saveAction)

        # 2. Edit Menu
        editMenu = menubar.addMenu("&Edit") # "Edit" 추가
        
        # 3. View Menu
        viewMenu = menubar.addMenu("&View") # "Edit" 추가

        # 4. Tools Menu
        toolsMenu = menubar.addMenu("&Tools") # "Edit" 추가

        # 5. Help Menu
        helpMenu = menubar.addMenu("&Help") # "Help" 추가

    #### Toolbar
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(editAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(printAction)
        self.toolbar.addAction(exitAction)

    #### Label & Button
        # 1. Webcam Label & Button    
        label1 = QLabel('1. Webcam', self)
        label1.move(x1, y1)
        
        btn_webcam = QPushButton('&start', self)
        btn_webcam.setToolTip('Click this button to <b>start Webcam</b>.')
        btn_webcam.setGeometry(x2, y1, 80, 30)
        
        # 2. CCTV on/off Label & Button
        label1 = QLabel('2. CCTV Mode', self)
        label1.move(x1, y2)
        
        btn_cctv = QPushButton('&on', self)
        btn_cctv.setCheckable(True) # True시, 누른 상태와 그렇지 않은 상태를 구분
        btn_cctv.setToolTip('Click this button to <b>start CCTV Mode</b>.')
        btn_cctv.toggle() # toggle(): 상태를 바꿉니다.
        btn_cctv.setGeometry(x2, y2, 80, 30)
        
    #### QSliter  추가
        label3 = QLabel('3. Threshold', self)
        label3.move(x1, y3)

        slider = QSlider(Qt.Horizontal, self)
        slider.setGeometry(x2, y3, 200, 30)
        slider.setRange(0, 100)
        slider.setTickInterval(20)
        slider.setTickPosition(QSlider.TicksAbove)
        slider.valueChanged.connect(self.value_changed)

        # QSlider 데이터를 표시할 라벨
        self.label = QLabel(self)
        self.label.setGeometry(x2+220, y3, 50, 30)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setStyleSheet("border-radius: 5px;"
                                  "border: 1px solid gray;"
                                  "background-color: #BBDEFB")

    #### Pixmap
        pixmap = QPixmap('./2023.02/02.15.d94_team_study/pics/dog.jpg')
        # image.setPixmap(pixmap) #image path

        # Quit Button    
        btn_quit = QPushButton('Quit', self)
        btn_quit.setToolTip('Click this button to <b>Quit</b>.')
        btn_quit.move(int(X_SIZE*0.8), int(Y_SIZE*0.9))
        btn_quit.clicked.connect(QCoreApplication.instance().quit)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())   

    # 슬라이드 시그널 valueChanged 연결 함수
    def value_changed(self, value):
        self.label.setText(str(value/100))


if __name__ == '__main__':
   # 모든 PyQt5 어플리케이션은 어플리케이션 객체를 생성
   app = QApplication(sys.argv)
   ex = MyApp()
   ex.show()
   sys.exit(app.exec_())