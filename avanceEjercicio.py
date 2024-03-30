from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1282, 1271)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(360, 40, 831, 1221))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(10, 20, 371, 40))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(10, 40, 331, 1221))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(90, 480, 71, 81))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../../Downloads/shopping-cart.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(90, 220, 71, 91))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Downloads/car-front.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(90, 360, 71, 81))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../../Downloads/gift.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        # Connect the button's clicked signal to the drawLine slot
        self.pushButton.clicked.connect(self.drawLine)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    def drawLine(self):
        print("Button clicked, draw a line")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Linea"))


class MyForm(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
        self.points = []
        self.drawing_active = False  # Add this line

    def drawLine(self):
        self.drawing_active = not self.drawing_active  # Toggle drawing_active
    def mousePressEvent(self, event):
     if self.drawing_active:  # Only add points if drawing is active
            self.points.append(event.pos())
            if len(self.points) % 2 == 0:  # If we have a pair of points
                self.update()  # Trigger paintEvent

    def paintEvent(self, event):
        if len(self.points) >= 2:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black,  8, Qt.SolidLine))
            for i in range(0, len(self.points), 2):  # Iterate over pairs of points
                painter.drawLine(self.points[i], self.points[i+1])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = MyForm()
    Form.show()
    sys.exit(app.exec_())
    