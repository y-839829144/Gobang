from PySide2 import QtGui,QtCore
from PySide2.QtWidgets import QWidget,QPushButton,QApplication
from PySide2.QtGui import QPalette,QImage,QBrush,QIcon
import os,PySide2,sys
from MyButton import Mybutton
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins','platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
class Basewindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('五子棋-人机对战')
        self.setWindowIcon(QIcon('source/icon.ico'))
        self.setFixedSize(760,650)

        p = QPalette(self.palette())
        b = QBrush(QImage('source/游戏界面.png'))
        p.setBrush(QPalette.Background, b)
        self.setPalette(p)
        self.setFixedSize(760, 650)


        self.startBtn = Mybutton('source/开始按钮_normal.png','source/开始按钮_hover.png','source/开始按钮_press.png',parent=self)
        self.startBtn.move(630,200)
        self.regretBtn = Mybutton('source/悔棋按钮_normal.png','source/悔棋按钮_hover.png','source/悔棋按钮_press.png',parent=self)
        self.regretBtn.move(630,250)
        self.loseBtn = Mybutton('source/认输按钮_normal.png','source/认输按钮_hover.png','source/认输按钮_press.png',parent=self)
        self.loseBtn.move(630,300)
        self.backBtn = Mybutton('source/返回按钮_normal.png','source/返回按钮_hover.png','source/返回按钮_press.png',parent=self)
        self.backBtn.move(630,50)
        self.urgeBtn = Mybutton('source/催促按钮_normal.png','source/催促按钮_hover.png','source/催促按钮_press.png',parent=self)
        self.urgeBtn.move(630, 400)










if __name__ == "__main__":
    app = QApplication(sys.argv)
    basewindow = Basewindow()
    basewindow.show()
    sys.exit(app.exec_())
