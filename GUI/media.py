import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

class MediaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.lblSource = QLabel("Source", self)
        self.lblSource.setGeometry(100, 50, 90, 30)
        self.lblSource.setFont(QFont("Arial", 16))

        self.radio_status = 0
        self.bt_status = 0
        self.cd_status = 0

        self.radio_nr = 1
        self.bt_nr = 1
        self.cd_nr = 1

        self.nr_volume = 0

        self.radio_rect = QRect(190, 50, 130, 30)
        self.bt_rect = QRect(400, 50, 130, 30)
        self.cd_rect = QRect(600, 50, 130, 30)
        self.seek_left_rect = QRect(290, 115, 30, 30)
        self.seek_right_rect = QRect(600, 115, 30, 30)
        self.decrease_volume_rect = QRect(400, 450, 30, 30)
        self.increase_volume_rect = QRect(495, 450, 30, 30)

        self.lblRadio = QLabel("Radio", self)
        self.lblRadio.move(200, 55)
        self.lblRadio.setFont(QFont("Arial", 16))

        self.lblBT = QLabel("Bluetooth", self)
        self.lblBT.move(410, 55)
        self.lblBT.setFont(QFont("Arial", 16))

        self.lblCD = QLabel("CD", self)
        self.lblCD.move(610, 55)
        self.lblCD.setFont(QFont("Arial", 16))

        self.lblMedia = QLabel("Media", self)
        self.lblMedia.move(430, 15)
        self.lblMedia.setFont(QFont("Arial", 16))

        self.lblVolume = QLabel("0/10", self)
        self.lblVolume.setGeometry(440, 420, 60, 30)
        self.lblVolume.setFont(QFont("Arial", 16))

        self.lblSeekLeft = QLabel("<", self)
        self.lblSeekLeft.move(300, 120)
        self.lblSeekLeft.setFont(QFont("Arial", 16))

        self.lblSeekRight = QLabel(">", self)
        self.lblSeekRight.move(610, 120)
        self.lblSeekRight.setFont(QFont("Arial", 16))

        self.lblDecreaseVolume = QLabel("-", self)
        self.lblDecreaseVolume.move(410, 453)
        self.lblDecreaseVolume.setFont(QFont("Arial", 16))

        self.lblIncreaseVolume = QLabel("+", self)
        self.lblIncreaseVolume.move(505, 453)
        self.lblIncreaseVolume.setFont(QFont("Arial", 16))

        self.lblCurrentPlay = QLabel(self)
        self.lblCurrentPlay.resize(200, 30)
        self.lblCurrentPlay.move(400, 200)
        self.lblCurrentPlay.setFont(QFont("Arial", 16))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 253, 161))
        painter.drawRect(self.rect())

        # Set the fill color and brush
        fill_color_rectangles = QColor(255, 255, 255)
        brush = QBrush(fill_color_rectangles, Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw radio button
        painter.drawRect(self.radio_rect)
        # Draw BT
        painter.drawRect(self.bt_rect)
        # Draw CD
        painter.drawRect(self.cd_rect)
        # Draw seek left
        painter.drawRect(self.seek_left_rect)
        # Draw seek right
        painter.drawRect(self.seek_right_rect)
        # Draw - button
        painter.drawRect(self.decrease_volume_rect)
        # Draw + button
        painter.drawRect(self.increase_volume_rect)

        # Radio spot
        if self.radio_status == 0:
            fill_color_spots = QColor(128, 128, 128)
        else:
            fill_color_spots = QColor(255, 165, 0)
        brush = QBrush(fill_color_spots, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(300, 58, 15, 15)

        # BT spot
        if self.bt_status == 0:
            fill_color_spots = QColor(128, 128, 128)
        else:
            fill_color_spots = QColor(255, 165, 0)
        brush = QBrush(fill_color_spots, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(510, 58, 15, 15)

        # CD spot
        if self.cd_status == 0:
            fill_color_spots = QColor(128, 128, 128)
        else:
            fill_color_spots = QColor(255, 165, 0)
        brush = QBrush(fill_color_spots, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(710, 58, 15, 15)

        radius = 70
        center_volume = Point(470, 350)
        start_angle_volume = 225 - (self.nr_volume * 270) / 10
        span_angle_volume = (self.nr_volume * 270) / 10

        # Set the fill color and brush
        fill_color_ventilation = QColor(int((255 * self.nr_volume) / 10), int((255 * self.nr_volume) / 10),
                                        int((255 * self.nr_volume) / 10))
        brush = QBrush(fill_color_ventilation, Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw ventilation circle
        painter.drawPie(int(center_volume.x - radius), int(center_volume.y - radius),
                        int(2 * radius), int(2 * radius),
                        int(start_angle_volume * 16), int(span_angle_volume * 16))

    # detect if a button is clicked
    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        if (self.radio_rect.x() <= x <= self.radio_rect.x() + self.radio_rect.width()) and (
                self.radio_rect.y() <= y <= self.radio_rect.y() + self.radio_rect.height()):
            self.change_radio()
        elif (self.bt_rect.x() <= x <= self.bt_rect.x() + self.bt_rect.width()) and (
                self.bt_rect.y() <= y <= self.bt_rect.y() + self.bt_rect.height()):
            self.change_bt()
        elif (self.cd_rect.x() <= x <= self.cd_rect.x() + self.cd_rect.width()) and (
                self.cd_rect.y() <= y <= self.cd_rect.y() + self.cd_rect.height()):
            self.change_cd()
        elif (self.seek_left_rect.x() <= x <= self.seek_left_rect.x() + self.seek_left_rect.width()) and (
                self.seek_left_rect.y() <= y <= self.seek_left_rect.y() + self.seek_left_rect.height()):
            if self.radio_status==1:
                self.decrease_frecv(self.radio_nr-1)
            elif self.cd_status==1:
                self.decrease_frecv(self.cd_nr-1)
            elif self.bt_status==1:
                self.decrease_frecv(self.bt_nr-1)
        elif (self.seek_right_rect.x() <= x <= self.seek_right_rect.x() + self.seek_right_rect.width()) and (
                self.seek_right_rect.y() <= y <= self.seek_right_rect.y() + self.seek_right_rect.height()):
            if self.radio_status == 1:
                self.increase_frecv(self.radio_nr+1)
            elif self.cd_status == 1:
                self.increase_frecv(self.cd_nr+1)
            elif self.bt_status == 1:
                self.increase_frecv(self.bt_nr+1)
        elif (
                self.decrease_volume_rect.x() <= x <= self.decrease_volume_rect.x() + self.decrease_volume_rect.width()) and (
                self.decrease_volume_rect.y() <= y <= self.decrease_volume_rect.y() + self.decrease_volume_rect.height()):
            self.decrease_volume()
        elif (
                self.increase_volume_rect.x() <= x <= self.increase_volume_rect.x() + self.increase_volume_rect.width()) and (
                self.increase_volume_rect.y() <= y <= self.increase_volume_rect.y() + self.increase_volume_rect.height()):
            self.increase_volume()

    def change_radio(self):
        self.radio_status = 1
        self.bt_status = 0
        self.cd_status = 0
        self.lblCurrentPlay.setText("Radio " + str(self.radio_nr))
        self.update()

    def change_bt(self):
        self.bt_status = 1
        self.radio_status = 0
        self.cd_status = 0
        self.lblCurrentPlay.setText("Song " + str(self.bt_nr))
        self.update()

    def change_cd(self):
        self.cd_status = 1
        self.radio_status = 0
        self.bt_status = 0
        self.lblCurrentPlay.setText("Track " + str(self.cd_nr))
        self.update()

    def change_volume(self, new_volume):
        if new_volume >= 0 and new_volume <= 10:
            self.nr_volume = new_volume
            self.lblVolume.setText(str(new_volume) + "/10")
            self.update()
        else:
            print("Volume should be between [0;10]")

    def decrease_frecv(self, new_frecv):
        if self.radio_status == 1:
            if self.radio_nr > 1:
                self.radio_nr = new_frecv
                self.lblCurrentPlay.setText("Radio " + str(self.radio_nr))
        elif self.cd_status == 1:
            if self.cd_nr > 1:
                self.cd_nr = new_frecv
                self.lblCurrentPlay.setText("Track " + str(self.cd_nr))
        elif self.bt_status == 1:
            if self.bt_nr > 1:
                self.bt_nr = new_frecv
                self.lblCurrentPlay.setText("Song " + str(self.bt_nr))

    def increase_frecv(self, new_frecv):
        if self.radio_status == 1:
            if self.radio_nr < 10:
                self.radio_nr = new_frecv
                self.lblCurrentPlay.setText("Radio " + str(self.radio_nr))
        elif self.cd_status == 1:
            if self.cd_nr < 10:
                self.cd_nr = new_frecv
                self.lblCurrentPlay.setText("Track " + str(self.cd_nr))
        elif self.bt_status == 1:
            if self.bt_nr < 10:
                self.bt_nr = new_frecv
                self.lblCurrentPlay.setText("Song " + str(self.bt_nr))

    def decrease_volume(self):
        self.change_volume(self.nr_volume - 1)

    def increase_volume(self):
        self.change_volume(self.nr_volume + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget_media = MediaWidget()
    widget_media.resize(1000, 500)
    widget_media.show()
    sys.exit(app.exec_())