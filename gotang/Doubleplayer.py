
from PySide2.QtWidgets import QWidget,QPushButton,QApplication,QLabel
from PySide2.QtGui import QPalette,QImage,QBrush,QIcon,QPixmap
from PySide2.QtCore import Signal
from Base import Basewindow
import os,PySide2,sys
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins','platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

#自定义棋子
class Chessman(QLabel):
    def __init__(self,color=False,parent=None):
        super().__init__(parent)
        #0 黑色 1 白色
        if color:
            self.setPixmap(QPixmap('source/白子.png'))
        else:
            self.setPixmap(QPixmap('source/黑子.png'))
        self.x_index =0
        self.y_index =0
        self.color = color



    def getindex(self,x,y):
        #计算棋子位置
        self.x_index = (x-50+15)//30
        self.y_index = (y-50+15)//30
        x = 50 + self.x_index*30
        y = 50 + self.y_index*30
        return x,y
class Whowin(QLabel):
    def __init__(self,color = False,parent = None):
        super().__init__(parent)
        if color:
            self.setPixmap(QPixmap('source/白棋胜利.png'))
        else:
            self.setPixmap(QPixmap('source/黑棋胜利.png'))






class Doublewindow(Basewindow):
    back = Signal()#实例化自定义信号（参数类型）


    def __init__(self,parent = None):
        super().__init__(parent)

        #False hei true bai
        self.setWindowTitle('五子棋-双人对战')
        # self.color = color
        self.record = []
        self.win_imag = []
        self.startFlag = False
        self.regretFlag = False
        self.loseFlag = False
        self.chessmanColor = False
        self.backBtn.clicked.connect(self.backSlot)
        self.startBtn.clicked.connect(self.starteve)
        self.regretBtn.clicked.connect(self.regreteve)
        self.loseBtn.clicked.connect(self.loseeve)
        #空白棋盘
        self.chessmanboard = [[None for y in range(19)] for x in range(19)]


        #绑定返回事件
        self.backBtn.clicked.connect(self.backSlot)
    def backSlot(self):
        self.back.emit()#发射自定义信号（参数）


    def starteve(self):
        self.startFlag = True
        self.regretFlag = True
        self.loseFlag = True
        for x in self.win_imag:
            x.close()
        for x in self.record:
            x.close()
        self.record = []
        self.chessmanColor = False
        self.chessmanboard = [[None for x in range(19)] for x in range(19)]

    def loseeve(self):
        if self.loseFlag:
            self.whowin = Whowin(self.chessmanColor, parent=self)
            self.whowin.move(60, 50)
            self.whowin.show()
            self.win_imag.append(self.winwh)
            self.startFlag = False
            self.regretFlag = False
            self.loseFlag = False

    def regreteve(self):
        if self.regretFlag:
            tmp = self.record.pop()
            tmp.deleteLater()
            self.chessmanboard[tmp.y_index][tmp.x_index] = None
            self.chessmanColor = not tmp.color




    def mousePressEvent(self, event:PySide2.QtGui.QMouseEvent):
        if not self.startFlag:
            return
        # event.pos()
        x = event.x()
        y = event.y()
        if x < 35 or x > 605:
            return
        if y < 35 or y > 605:
            return



        if self.chessmanboard[(y-50+15)//30][(x-50+15)//30]:
            return
        self.chessmanColor = not self.chessmanColor

        self.chessman =Chessman(self.chessmanColor,parent=self)
        x,y=self.chessman.getindex(x,y)
        self.chessmanboard[self.chessman.y_index][self.chessman.x_index] = self.chessman
            # print(self.chessmanboard)
        self.chessman.move(x-15,y- 15)
        self.chessman.show()
        self.record.append(self.chessman)
        self.regretFlag = True
        self.renjixiaqiFlag = True
        self.isWin(self.chessman)
        return True









    def isWin(self,chessman):






        #斜对角方向
        count = 1
        x = chessman.x_index
        y = chessman.y_index
        color = chessman.color


        #先找左上再找左下
        #右下
        while True:
            if x >= 18 or x < 0 or y > 18 or y < 0:
                break
            if self.chessmanboard[y+1][x+1] and self.chessmanboard[y+1][x+1].color == color:
                count+=1
                y+=1
                x+=1

            else:
                break
            #左上

        count = 1
        x = chessman.x_index
        y = chessman.y_index
        color = chessman.color
        while True:
            if x >= 18 or x <= 0 or y >= 18 or y <= 0:
                break
            if self.chessmanboard[y-1][x-1] and  self.chessmanboard[y-1][x-1].color == color:
                count+=1
                y-=1
                x-=1

            else:
                break
            #右上
        x = chessman.x_index
        y = chessman.y_index
        while True:
            if x >= 18 or x <= 0 or y >= 18 or y <= 0:
                break
            if self.chessmanboard[y - 1][x + 1] and self.chessmanboard[y - 1][x + 1].color == color:
                count += 1
                y -= 1
                x += 1

            else:
                break

            #左下

        x = chessman.x_index
        y = chessman.y_index
        while True:
            if x >= 18 or x <= 0 or y >= 18 or y <= 0:
                break
            if self.chessmanboard[y + 1][x - 1] and self.chessmanboard[y + 1][x - 1].color == color:
                count += 1
                y += 1
                x -= 1

            else:
                break


        #上
        x = chessman.x_index
        y = chessman.y_index
        while True:
            if x >= 18 or x <= 0 or y >= 18 or y <= 0:
                break
            if self.chessmanboard[y - 1][x - 0] and self.chessmanboard[y - 1][x - 0].color == color:
                count += 1
                y -= 1
                x -= 0

            else:
                break
        #下
        x = chessman.x_index
        y = chessman.y_index
        while True:
            if x >= 18 or x <= 0 or y >= 18 or y <= 0:
                break
            if self.chessmanboard[y + 1][x - 0] and self.chessmanboard[y + 1][x - 0].color == color:
                count += 1
                y += 1
                x -= 0

            else:
                break
        #左
        x = chessman.x_index
        y = chessman.y_index
        while True:
            if x >= 18 or x <= 0 or y >= 18 or y <= 0:
                break
            if self.chessmanboard[y + 0][x - 1] and self.chessmanboard[y + 0][x - 1].color == color:
                count += 1
                y += 0
                x -= 1

            else:
                break
        #右
        x = chessman.x_index
        y = chessman.y_index
        while True:
            if x >= 18 or x <= 0 or y >= 18 or y <= 0:
                break
            if self.chessmanboard[y + 0][x + 1] and self.chessmanboard[y + 0][x + 1].color == color:
                count += 1
                y += 0
                x += 1

            else:
                break


            #判断胜利
        if count == 5:
            self.whowin = Whowin(self.chessmanColor, parent=self)
            self.whowin.move(60, 50)
            self.whowin.show()
            self.startFlag = False
            self.regretFlag = False
            self.loseFlag = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    b = Basewindow()
    b.show()
    sys.exit(app.exec_())


