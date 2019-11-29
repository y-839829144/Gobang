from PySide2.QtWidgets import QWidget,QPushButton,QLineEdit,QGridLayout,QLabel,QMessageBox
from PySide2.QtCore import Signal,QObject
import socket
import threading
from Doubleplayer import *
import json
from MyButton import Mybutton

class NetConfig(QWidget):
    netconfig_back = Signal()
    netconfigBtn_clicked = Signal([str,str,str,str])
    def __init__(self,parent=None):
        super().__init__(parent)
        self.name_label = QLabel("玩家名称",self)
        self.name_edit = QLineEdit("玩家——",self)
        self.ip_label = QLabel("IP",self)
        self.ip_edit = QLineEdit("127.0.0.1",self)
        self.port_label = QLabel("PORT",self)
        self.port_edit = QLineEdit("10086",self)
        self.server_btn = QPushButton("服务器",self)
        self.client_btn = QPushButton("客户端",self)
        g = QGridLayout()
        g.addWidget(self.name_label, 0, 1)
        g.addWidget(self.name_edit, 0, 2)
        g.addWidget(self.ip_label, 1, 1)
        g.addWidget(self.ip_edit, 1, 2)
        g.addWidget(self.port_label, 2, 1)
        g.addWidget(self.port_edit, 2, 2)
        g.addWidget(self.server_btn, 3, 1)
        g.addWidget(self.client_btn, 3, 2)
        self.setLayout(g)
        self.server_btn.clicked.connect(self.serverSlot)
        self.client_btn.clicked.connect(self.clientSlot)


    def serverSlot(self):
        self.netconfigBtn_clicked.emit("s",self.ip_edit.text(),self.port_edit.text(),self.name_edit.text())
        self.hide()
    def clientSlot(self):
        self.netconfigBtn_clicked.emit("c", self.ip_edit.text(), self.port_edit.text(), self.name_edit.text())
        self.hide()

    def closeEvent(self, event):
        self.netconfig_back.emit()
        self.close()






class NetPlayerwindow(Doublewindow):
    def __init__(self,netObject,parent=None):
        super().__init__(parent)
        self.setWindowTitle("联机对战")
        self.netObject = netObject
        self.netObject.netConnect()
        self.netObject.msg_signal.connect(self.parseMsg)
        self.urgeBtn.clicked.connect(self.urgeeve)

        #催促


        #是否是自己回合的标记
        self.isOwn = False

    def urgeeve(self):
        data = {
            'msg': 'urge'
        }
        self.netObject.send(json.dumps(data))


    def parseMsg(self,data):
        print(data)
        data = json.loads(data)
        if data['msg'] == 'position':
            x_index = data['x']
            y_index = data['y']
            #棋盘上落子操作
            self.autoChess(x_index,y_index)
        elif data['msg'] =='start':
            res = QMessageBox.information(self,'对方请求开始','是否同意开始?',QMessageBox.Yes|QMessageBox.No)
            print(res)
            if res == QMessageBox.Yes:
                super().starteve()

                data = {
                    'msg':'res',
                    'res_type':'start',
                    'res_data':'yes'
                }
                self.isOwn = False
                self.netObject.send(json.dumps(data))
            else:
                data = {
                    'msg': 'res',
                    'res_type': 'start',
                    'res_data': 'no'
                }
                self.netObject.send(json.dumps(data))
        elif data['msg'] == 'res':
            if data['res_type'] == 'start':
                if data['res_data'] == 'yes':
                    super().starteve()
                    self.isOwn = True
                else:
                    QMessageBox.information(self, "提示", "对方拒绝", QMessageBox.Close)
        elif data['msg'] =='urge':
            res = QMessageBox.information(self, '快点吧', QMessageBox.Yes )
            print(res)



    def starteve(self):
        data = {
            'msg':'start'
        }
        self.netObject.send(json.dumps(data))


    def autoChess(self,x,y):
        self.chessmanColor = not self.chessmanColor
        self.chessman = Chessman(color=self.chessmanColor,parent=self)
        self.chessman.x_index = x
        self.chessman.y_index = y
        self.chessman.move(x*30+50-15,y*30+50-15)
        self.chessman.show()
        self.chessmanboard[y][x] = self.chessman
        self.isWin(self.chessman)
        self.isOwn = not self.isOwn


    def mousePressEvent(self, event:PySide2.QtGui.QMouseEvent):
        if not self.isOwn:
            return
        if not self.startFlag:
            return
        if super().mousePressEvent(event):
            x_index = self.chessman.x_index
            y_index = self.chessman.y_index
            data = {
                'msg':'position',
                'x':x_index,
                'y':y_index
            }
            self.netObject.send(json.dumps(data))
            self.isOwn = not self.isOwn





class NetClient(QObject):
    msg_signal = Signal(str)
    def __init__(self,ip,port,name):
        super().__init__()
        self.ip = ip
        self.port = int(port)
        self.name = name
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def netConnect(self):
        try:
            self.socket.connect((self.ip,self.port))
        except Exception as e:
            QMessageBox.warning(self,"错误",str(e),QMessageBox.close)
            return
        th = threading.Thread(target=self.recv) #target指定线程执行的函数
        th.setDaemon(True)
        th.start()

    def recv(self):
        while True:
            try:
                data = self.socket.recv(4096).decode()
                self.msg_signal.emit(data)
            except Exception as e:
                QMessageBox.warning(self,"错误",str(e),QMessageBox.close)
                break
    def send(self,data):
        self.socket.send(data.encode())

class NetServer(QObject):
    msg_signal = Signal(str)
    def __init__(self,ip,port,name):
        super().__init__()
        self.ip = ip
        self.port = int(port)
        self.name = name
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def netConnect(self):
        try:
            self.socket.bind(('',self.port))
            self.socket.listen(1)
            # self.client_sock,addr = self.socket.accept()
        except Exception as e:
            QMessageBox.warning(self,'错误',str(e),QMessageBox.Close)
            return
        th = threading.Thread(target=self.recv)
        th.setDaemon(True)
        th.start()

    def recv(self):
        self.client_sock, addr = self.socket.accept()
        while True:
            try:
                data = self.client_sock.recv(4096)
                data = data.decode()
            #z做处理
                # print(data)
                self.msg_signal.emit(data)
            except Exception as e:
                QMessageBox.warning(self, "错误", str(e), QMessageBox.close)

                break
    def send(self,data):
        if self.client_sock:
            self.client_sock.send(data.encode())