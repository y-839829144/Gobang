from Doubleplayer import *



class Singlewindow(Doublewindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("人机对战")
        self.startFlag = False
        self.regretFlag = False
        self.loseFlag = False
        self.chessmanColor = False
        self.backBtn.clicked.connect(self.backSlot)
        self.startBtn.clicked.connect(self.starteve)
        self.regretBtn.clicked.connect(self.regreteven)
        self.loseBtn.clicked.connect(self.loseeve)



    def mousePressEvent(self, event:PySide2.QtGui.QMouseEvent):
        super().mousePressEvent(event)
        self.autoplay()

    def autoplay(self):
        if self.startFlag ==True:
            self.chessmanColor = not self.chessmanColor
            self.chessman = self.getAutoChess()
            x = self.chessman.x_index*30 +50 -15
            y = self.chessman.y_index*30 +50 -15
            self.chessman.move(x,y)
            self.chessman.show()
            self.chessmanboard[self.chessman.y_index][self.chessman.x_index]=self.chessman
            self.isWin(self.chessman)

    def getAutoChess(self):
        #获取棋盘上所有白子的分数
        #获取棋盘上所有黑子的分数
        #取他们的最大值
        w_score = []
        b_score = []
        for i in  range(19):
            for j in range(19):
                if self.chessmanboard[i][j]:
                    w_score.append(0)
                else:

                    w_score.append(self.getScore(i,j,1))


        for i in  range(19):
            for j in range(19):
                if self.chessmanboard[i][j]:
                    b_score.append(0)
                else:

                    b_score.append(self.getScore(i,j,0))



        tmp = [ max(x,y) for x,y in zip(w_score,b_score)]
        res = tmp.index(max(tmp))
        x_index = res % 19
        y_index = res //19
        c = Chessman(self.chessmanColor,parent=self)
        c.x_index = x_index
        c.y_index = y_index
        return c


    def getScore(self,i,j,color):
        color = color
        score = [0,0,0,0]
        y = i
        x = j
        #遍历四个方向计算棋子分数
        # 上 y -1 x +0
        for c in range(4):
            if y - 1 <0:
                break
            if self.chessmanboard[y-1][x] and self.chessmanboard[y-1][x].color == color:
                score[0]+=1
            else:
                break
            y -=1
        y=i
        for c in range(4):
            if y + 1 >18:
                break
            if self.chessmanboard[y+1][x] and self.chessmanboard[y+1][x].color == color:
                score[0]+=1
            else:
                break
            y +=1

        y = i
        x = j
        # 遍历四个方向计算棋子分数
        # 左 x -1 y +0
        for c in range(4):
            if x - 1 < 0:
                break
            if self.chessmanboard[y+0][x-1] and self.chessmanboard[y+0][x-1].color == color:
                score[1] += 1
            else:
                break
            x -= 1
        x = j
        for c in range(4):
            if x + 1 > 18:
                break
            if self.chessmanboard[y+0][x+1] and self.chessmanboard[y+0][x+1].color == color:
                score[0] += 1
            else:
                break
            x += 1

        y = i
        x = j
        # 遍历四个方向计算棋子分数
        # 左上 y-1 x-1
        for c in range(4):
            if y-1<0 or x - 1 < 0:
                break
            if self.chessmanboard[y -1][x - 1] and self.chessmanboard[y -1][x - 1].color == color:
                score[2] += 1
            else:
                break
            x -= 1
            y -= 1
        y =i
        x =j
        for c in range(4):
            if y+1>18 or x+1>18:
                break
            if self.chessmanboard[y + 0][x + 1] and self.chessmanboard[y + 0][x + 1].color == color:
                score[2] += 1
            else:
                break
            x += 1
            y += 1

        y = i
        x = j
        # 遍历四个方向计算棋子分数
        # 右上 y-1 x+1
        for c in range(4):
            if y - 1 < 0 or x + 1 >18:
                break
            if self.chessmanboard[y - 1][x + 1] and self.chessmanboard[y - 1][x + 1].color == color:
                score[3] += 1
            else:
                break
            x += 1
            y -= 1
        y = i
        x = j
        for c in range(4):
            if y + 1 > 18 or x - 1 <0:
                break
            if self.chessmanboard[y + 1][x - 1] and self.chessmanboard[y + 1][x - 1].color == color:
                score[3] += 1
            else:
                break
            x -= 1
            y += 1
        return max(score)
    def regreteven(self):
        if self.renjixiaqiFlag:
            self.chessman.deleteLater()








