import sys
import cv2
from time import sleep

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect

class FaceRecognition(QWidget):
    def __init__(self):
        super().__init__()
        self.raise_()

        self.lblFaceRecognition = QLabel("Face recognition", self)
        self.lblFaceRecognition.move(400, 15)
        self.lblFaceRecognition.resize(200,30)
        self.lblFaceRecognition.setFont(QFont("Arial", 16))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.addStretch()



        self.activate_frame()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(237, 152, 102))
        painter.drawRect(self.rect())

        fill_color_rectangles = QColor(255, 255, 255)
        brush = QBrush(fill_color_rectangles, Qt.SolidPattern)
        painter.setBrush(brush)

    def activate_frame(self):
        vid = cv2.VideoCapture(0)
        while (True):
            ret, frame = vid.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget_face_recognition = FaceRecognition()
    widget_face_recognition.resize(1000, 500)
    widget_face_recognition.show()
    sys.exit(app.exec_())