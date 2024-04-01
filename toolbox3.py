from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QToolBox, QGroupBox, QVBoxLayout, QLabel , QFrame
from PyQt5.QtGui import QPainter, QPen,QPixmap,QDrag
from PyQt5.QtCore import Qt,pyqtSignal,QMimeData

class Ui_Form:
    def setupUi(self, Form):
        self.setupForm(Form)
        self.setupFrames(Form)
        self.setupPushButton()
        self.setupToolbox()
        self.connectSignals(Form)
        self.retranslateUi(Form)

    def setupForm(self, Form):
        Form.setObjectName("Form")
        Form.resize(1282, 1271)

    def setupFrames(self, Form):
        self.setupMainFrame(Form)
        self.setupSecondaryFrame(Form)

    def setupMainFrame(self, Form):
        self.frame = DroppableFrame(Form)
        self.frame.setGeometry(QtCore.QRect(360, 40, 831, 1221))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

    def setupSecondaryFrame(self, Form):
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(10, 40, 331, 1221))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

    def setupPushButton(self):
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(10, 20, 371, 40))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

    def setupToolbox(self):
        self.toolbox = QToolBox(self.frame_2)
        self.toolbox.setGeometry(0, 0, 330, 600)
        self.addToolboxItems()

    def addToolboxItems(self):
        self.addToolboxItem("./Imagenes/Lobo.jpeg", "Toolbox 1")
        self.addToolboxItem("./Imagenes/panda.jpeg", "Toolbox 2")
        self.addToolboxItem("./Imagenes/pinguino.jpeg", "Toolbox 3")

    def addToolboxItem(self, image_path, toolbox_label):
        group = QGroupBox()
        vbox = QVBoxLayout()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
        label = DraggableLabel()
        label.setPixmap(pixmap)
        vbox.addWidget(label)
        group.setLayout(vbox)
        self.toolbox.addItem(group, toolbox_label)

    def connectSignals(self, Form):
        self.pushButton.clicked.connect(self.drawLine)
        QtCore.QMetaObject.connectSlotsByName(Form)

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
            painter.setPen(QPen(Qt.black,  1, Qt.SolidLine))
            for i in range(0, len(self.points), 2):  # Iterate over pairs of points
                painter.drawLine(self.points[i], self.points[i+1])


class DraggableLabel(QLabel):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setImageData(self.pixmap().toImage())
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

class DroppableFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event):
        position = event.pos()
        image = event.mimeData().imageData()
        pixmap = QPixmap.fromImage(image)
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.move(position)
        label.show()
        event.acceptProposedAction()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = MyForm()
    Form.show()
    sys.exit(app.exec_())
    