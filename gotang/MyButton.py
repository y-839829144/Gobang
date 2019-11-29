from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap
import PySide2
from PySide2.QtCore import Signal


class Mybutton(QLabel):
    clicked = Signal()
    def __init__(self,*args,parent=None):
        super().__init__(parent)
        # 1 正常 2 进入 3 移除
        self.pic_1 = QPixmap(args[0])
        self.pic_2 = QPixmap(args[1])
        self.pic_3 = QPixmap(args[2])
        self.setFixedSize(self.pic_1.size())
        self.setPixmap(self.pic_1)
        self.enterFlag = False



        # label = QLabel()
        # label.setPixmap(QPixmap('source/'))

    def enterEvent(self, event:PySide2.QtCore.QEvent):
        self.setPixmap(self.pic_2)
        self.enterFlag = True

    def mousePressEvent(self, ev:PySide2.QtGui.QMouseEvent):
        self.setPixmap(self.pic_3)
    def mouseReleaseEvent(self, ev:PySide2.QtGui.QMouseEvent):
        if self.enterFlag:
            self.setPixmap(self.pic_2)
            self.clicked.emit()
        else:
            self.setPixmap(self.pic_1)
        self.clicked.emit()


    def leaveEvent(self, event:PySide2.QtCore.QEvent):
        self.setPixmap(self.pic_1)
        self.enterFlag = False






