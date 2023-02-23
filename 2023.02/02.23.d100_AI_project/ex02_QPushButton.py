## QPushButton
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
 
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()
 
    def setUI(self):
        # 첫 번째 파라미터로는 버튼에 나타날 텍스트, 두 번째는 버튼이 속할 부모 클래스를 지정.
        # 버튼에 단축키(shortcut)를 지정: 해당 문자 앞에 ampersand(‘&’)를 넣어준다.이 버튼의 단축키는 ‘Alt + b’.
        btn1 = QPushButton('&Button 1', self)
        # setCheckable(): True 설정 시, 누른 상태와 그렇지 않은 상태를 구분합니다.
        btn1.setCheckable(True)
        # toggle(): 상태를 바꿉니다.
        btn1.toggle()
 
        btn2 = QPushButton(self)
        # setText(): 버튼에 표시될 텍스트를 설정합니다.
        btn2.setText('Button &2')
 
        btn3 = QPushButton('Button 3', self)
        # setEnalbed(): False 설정 시, 버튼을 사용할 수 없습니다.
        btn3.setEnabled(False)
 
        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
 
        self.setLayout(vbox)
        self.setWindowTitle('QPushButton')
        self.setGeometry(300, 300, 300, 200)
        self.show()
 
 
if __name__ == '__main__':
 
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())