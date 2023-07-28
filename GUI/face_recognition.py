import sys
import cv2

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class FaceRecognitionWidget(QWidget):
    def __init__(self):
        super(FaceRecognitionWidget, self).__init__()

        self.label = QVBoxLayout()

        self.lblFaceRecognition = QLabel("Face recognition", self)
        self.lblFaceRecognition.move(400, 15)
        self.lblFaceRecognition.resize(200, 30)
        self.lblFaceRecognition.setFont(QFont("Arial", 16))
        self.label.addWidget(self.lblFaceRecognition, alignment=Qt.AlignCenter)

        self.feed_label = QLabel()
        self.feed_label.setFixedSize(600, 400)
        self.label.addWidget(self.feed_label, alignment=Qt.AlignCenter)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.label.addWidget(self.CancelBTN)

        self.setLayout(self.label)

        self.face_recognition_frame = FaceRecognitionFrame()
        self.face_recognition_frame.image_update.connect(self.ImageUpdateSlot)
        self.face_recognition_frame.start()
        self.is_video_active = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(237, 152, 102))
        painter.drawRect(self.rect())

        fill_color_rectangles = QColor(255, 255, 255)
        brush = QBrush(fill_color_rectangles, Qt.SolidPattern)
        painter.setBrush(brush)

    def ImageUpdateSlot(self, image):
        if self.is_video_active:
            self.feed_label.setPixmap(QPixmap.fromImage(image))

    def CancelFeed(self):
        self.is_video_active = False
        self.face_recognition_frame.stop()
        image = QImage(r"C:\Users\vlad.lazar\Desktop\SmartCar\aproved.png")
        self.feed_label.setPixmap(QPixmap.fromImage(image))
        self.feed_label.setAlignment(Qt.AlignCenter)


class FaceRecognitionFrame(QThread):
    image_update = pyqtSignal(QImage)

    def run(self):
        self.thread_active = True
        capture = cv2.VideoCapture(0)
        while self.thread_active:
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipped_image = cv2.flip(image, 1)
                convert_to_qt_format = QImage(flipped_image.data, flipped_image.shape[1], flipped_image.shape[0], QImage.Format_RGB888)
                Pic = convert_to_qt_format.scaled(600, 400) #Qt.KeepAspectRatio
                self.image_update.emit(Pic)

    def stop(self):
        self.thread_active = False
        self.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget_face_recognition = FaceRecognitionWidget()
    widget_face_recognition.resize(1000, 500)
    widget_face_recognition.show()
    sys.exit(app.exec_())
