import sys
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSlot
from GUI.measure_distance import start_run_rear, start_run_front


class ParkingSensorsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.lblParkingSensors = QLabel("Parking sensors", self)
        self.lblParkingSensors.setGeometry(400, 10, 200, 30)
        self.lblParkingSensors.setFont(QFont("Arial", 16))

        self.lblFront = QLabel("Front", self)
        self.lblFront.setGeometry(100, 110, 200, 30)
        self.lblFront.setFont(QFont("Arial", 16))

        self.lblRear = QLabel("Rear", self)
        self.lblRear.setGeometry(100, 340, 200, 30)
        self.lblRear.setFont(QFont("Arial", 16))

        self.distance_front = 0
        self.distance_rear = 0

        self.sensor_sensibility = 30

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setGeometry((QtCore.QRect(0, 0, 300, 300)))

        # initialize progress bar for front sensor
        self.progress_bar_front = QProgressBar()
        self.progress_bar_front.setMinimum(0)
        self.progress_bar_front.setMaximum(self.sensor_sensibility)
        self.progress_bar_front.setOrientation(Qt.Horizontal)
        self.progress_bar_front.setFixedHeight(30)
        self.progress_bar_front.setFixedWidth(300)
        self.progress_bar_front.setTextVisible(False)
        self.progress_bar_front.setStyleSheet('''
                            QProgressBar {
                                border: 1px solid gray;
                                border-radius: 10px;
                                background-color: #E0E0E0;
                            }
                            QProgressBar::chunk {
                                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                                  stop: 0 #00FF00, stop: 0.33 #00FF00,
                                                                  stop: 0.33 #FFFF00, stop: 0.66 #FFFF00,
                                                                  stop: 0.66 #FF0000, stop: 1.0 #FF0000);

                            }
                        ''')
        self.measure_distance_front = start_run_front()
        self.measure_distance_front.update_progress_signal.connect(self.update_progress_front)
        self.measure_distance_front.start()
        layout.addWidget(self.progress_bar_front, alignment=Qt.AlignCenter)

        # initialize progress bar for rear sensor
        self.progress_bar_rear = QProgressBar()
        self.progress_bar_rear.setMinimum(0)
        self.progress_bar_rear.setMaximum(self.sensor_sensibility)
        self.progress_bar_rear.setOrientation(Qt.Horizontal)
        self.progress_bar_rear.setFixedHeight(30)
        self.progress_bar_rear.setFixedWidth(300)
        self.progress_bar_rear.setTextVisible(False)
        self.progress_bar_rear.setStyleSheet('''
                    QProgressBar {
                        border: 1px solid gray;
                        border-radius: 10px;
                        background-color: #E0E0E0;
                    }
                    QProgressBar::chunk {
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                          stop: 0 #00FF00, stop: 0.33 #00FF00,
                                                          stop: 0.33 #FFFF00, stop: 0.66 #FFFF00,
                                                          stop: 0.66 #FF0000, stop: 1.0 #FF0000);

                    }
                ''')

        self.measure_distance_rear = start_run_rear()
        self.measure_distance_rear.update_progress_signal.connect(self.update_progress_rear)
        self.measure_distance_rear.start()
        layout.addWidget(self.progress_bar_rear, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    @pyqtSlot(int)
    def update_progress_front(self, value):
        if value < self.sensor_sensibility:
            self.distance_front = self.sensor_sensibility - value
            self.progress_bar_front.setValue(self.distance_front)

            if self.distance_front <= self.sensor_sensibility / 3:
                self.progress_bar_front.setStyleSheet('''
                     QProgressBar {
                                border: 1px solid gray;
                                border-radius: 10px;
                                background-color: #E0E0E0;
                            }
                    QProgressBar::chunk {
                        background-color: #00FF00;
                        border-radius: 10px;
                    }
                ''')
            elif self.distance_front <= 2 * self.sensor_sensibility / 3:
                self.progress_bar_front.setStyleSheet('''
                     QProgressBar {
                            border: 1px solid gray;
                            border-radius: 10px;
                            background-color: #E0E0E0;
                        }
                    QProgressBar::chunk {
                        background-color: #FFFF00;
                        border-radius: 10px;
                    }
                ''')
            else:
                self.progress_bar_front.setStyleSheet('''
                     QProgressBar {
                            border: 1px solid gray;
                            border-radius: 10px;
                            background-color: #E0E0E0;
                        }
                    QProgressBar::chunk {
                        background-color: #FF0000;
                        border-radius: 10px;
                    }
                ''')
        else:
            self.progress_bar_front.setValue(0)

    @pyqtSlot(int)
    def update_progress_rear(self, value):
        if value < self.sensor_sensibility:
            self.distance_rear = self.sensor_sensibility - value
            self.progress_bar_rear.setValue(self.distance_rear)

            if self.distance_rear <= self.sensor_sensibility / 3:
                self.progress_bar_rear.setStyleSheet('''
                     QProgressBar {
                                border: 1px solid gray;
                                border-radius: 10px;
                                background-color: #E0E0E0;
                            }
                    QProgressBar::chunk {
                        background-color: #00FF00;
                        border-radius: 10px;
                    }
                ''')
            elif self.distance_rear <= 2 * self.sensor_sensibility / 3:
                self.progress_bar_rear.setStyleSheet('''
                     QProgressBar {
                            border: 1px solid gray;
                            border-radius: 10px;
                            background-color: #E0E0E0;
                        }
                    QProgressBar::chunk {
                        background-color: #FFFF00;
                        border-radius: 10px;
                    }
                ''')
            else:
                self.progress_bar_rear.setStyleSheet('''
                     QProgressBar {
                            border: 1px solid gray;
                            border-radius: 10px;
                            background-color: #E0E0E0;
                        }
                    QProgressBar::chunk {
                        background-color: #FF0000;
                        border-radius: 10px;
                    }
                ''')
        else:
            self.progress_bar_rear.setValue(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(137, 205, 245))
        painter.drawRoundedRect(self.rect(), 10, 10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ParkingSensorsWidget()
    widget.show()
    sys.exit(app.exec_())