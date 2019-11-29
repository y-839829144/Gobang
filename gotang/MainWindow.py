import os,PySide2,sys
from PySide2 .QtWidgets import QApplication,QPushButton,QWidget
from PySide2.QtCore import *
from PySide2.QtGui import *
from Doubleplayer import Doublewindow,Chessman
from MyButton import Mybutton
from SinglePlayer import Singlewindow
from NetPlayer import *
import cgitb
cgitb.enable( format = 'error')
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins','platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path




class Mainwindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("五子棋")
        self.setWindowIcon(QIcon('source/icon.ico'))


        p = QPalette(self.palette())
        b = QBrush(QImage('source/五子棋界面.png'))
        p.setBrush(QPalette.Background,b)
        self.setPalette(p)
        self.setFixedSize(760,650)

        self.singlebtn= Mybutton('source/人机对战_normal.png','source/人机对战_hover.png','source/人机对战_press.png',parent=self)
        self.singlebtn.move(300,300)
        self.doublebtn= Mybutton('source/双人对战_normal.png','source/双人对战_hover.png','source/双人对战_press.png',parent=self)
        self.doublebtn.move(300,400)
        self.netbtn= Mybutton('source/联机对战_normal.png','source/联机对战_hover.png','source/联机对战_press.png',parent=self)
        self.netbtn.move(300,500)

        self.doublebtn.clicked.connect(self.startDoublePlayer)
        self.singlebtn.clicked.connect(self.tartSinglePlayer)
        self.netbtn.clicked.connect(self.startNetPlayer)

    def tartSinglePlayer(self):
        self.gameWindow = Singlewindow()
        self.gameWindow.back.connect(self.restart)
        self.gameWindow.show()
        self.close()
    def startNetPlayer(self):
        self.netconfig = NetConfig()
        self.netconfig.netconfig_back.connect(self.restart2)
        self.netconfig.netconfigBtn_clicked.connect(self.createNetWindow)

        self.netconfig.show()
        self.close()

    def createNetWindow(self,t,ip,port,name):
        if t == 's':
            self.netObject = NetServer(ip,port,name)
        else:
            self.netObject = NetClient(ip,port,name)
        self.gameWindow = NetPlayerwindow(self.netObject)
        self.gameWindow.back.connect(self.restart)
        self.gameWindow.show()
        self.close()


    def startDoublePlayer(self):
        self.gameWindow = Doublewindow()
        self.gameWindow.back.connect(self.restart)
        self.gameWindow.show()
        self.close()


    def restart(self):
        # print(a0)
        self.show()
        self.gameWindow.close()

    def restart2(self):
        self.show()











if __name__ =="__main__":
    app = QApplication(sys.argv)
    mainWindow = Mainwindow()
    mainWindow.show()
    sys.exit(app.exec_())





