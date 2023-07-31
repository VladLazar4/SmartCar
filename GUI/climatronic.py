import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QRect

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


class ClimatronicWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nr_ventilation = 0
        self.deg_temperature = 17
        self.ac_status = 0
        self.left_seat_heat_status = 0
        self.right_seat_heat_status = 0

        self.ac_rect = QRect(450, 50, 70, 30)
        self.left_seat_rect = QRect(190, 50, 170, 30)
        self.right_seat_rect = QRect(620, 50, 180, 30)

        self.decrease_temperature_rect = QRect(210, 440, 30, 30)
        self.increase_temperature_rect = QRect(260, 440, 30, 30)

        self.lblDecreaseTemperature = QLabel("-", self)
        self.lblDecreaseTemperature.move(220, 443)
        self.lblDecreaseTemperature.setFont(QFont("Arial", 16))

        self.lblIncreaseTemperature = QLabel("+", self)
        self.lblIncreaseTemperature.move(270, 443)
        self.lblIncreaseTemperature.setFont(QFont("Arial", 16))

        self.decrease_ventilation_rect = QRect(710, 440, 30, 30)
        self.increase_ventilation_rect = QRect(760, 440, 30, 30)

        self.lblDecreaseVentilation = QLabel("-", self)
        self.lblDecreaseVentilation.move(720, 443)
        self.lblDecreaseVentilation.setFont(QFont("Arial", 16))

        self.lblIncreaseVentilation = QLabel("+", self)
        self.lblIncreaseVentilation.move(770, 443)
        self.lblIncreaseVentilation.setFont(QFont("Arial", 16))

        self.lblVentilation = QLabel("0/10", self)
        self.lblVentilation.setGeometry(720, 220, 60, 30)
        self.lblVentilation.setFont(QFont("Arial", 16))

        self.lblTemperature = QLabel("17 \N{DEGREE SIGN}C", self)
        self.lblTemperature.move(220, 220)
        self.lblTemperature.setFont(QFont("Arial", 16))

        self.lblAC = QLabel("A/C", self)
        self.lblAC.move(460, 55)
        self.lblAC.setFont(QFont("Arial", 16))

        self.lblLeftSeatHeat = QLabel("Left seat heat", self)
        self.lblLeftSeatHeat.move(200, 55)
        self.lblLeftSeatHeat.setFont(QFont("Arial", 16))

        self.lblRightSeatHeat = QLabel("Right seat heat", self)
        self.lblRightSeatHeat.move(630, 55)
        self.lblRightSeatHeat.setFont(QFont("Arial", 16))

        self.lblClimatronic = QLabel("Climatronic", self)
        self.lblClimatronic.move(430, 15)
        self.lblClimatronic.setFont(QFont("Arial", 16))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(178,237,204))
        painter.drawRect(self.rect())

        # Define the circle parameters
        radius = 100
        center_ventilation = Point(750, 350)
        start_angle_ventilation = 225 - (self.nr_ventilation * 270) / 10
        span_angle_ventilation = (self.nr_ventilation * 270) / 10

        center_temperature = Point(250, 350)
        start_angle_temperature = 225 - ((self.deg_temperature - 17) * 270) / 10
        span_angle_temperature = ((self.deg_temperature - 17) * 270) / 10

        # Set the fill color and brush
        fill_color_ventilation = QColor(int(255 * (int(self.nr_ventilation) / 10)), 0,
                                        int(255 * (1 - int(self.nr_ventilation) / 10)))
        brush = QBrush(fill_color_ventilation, Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw ventilation circle
        painter.drawPie(int(center_ventilation.x - radius), int(center_ventilation.y - radius),
                        int(2 * radius), int(2 * radius),
                        int(start_angle_ventilation * 16), int(span_angle_ventilation * 16))

        # Set the fill color and brush
        fill_color_temperature = QColor(int(255 * (int(self.deg_temperature - 17) / 10)), 0,
                                        int(255 * (1 - int(self.deg_temperature - 17) / 10)))
        brush = QBrush(fill_color_temperature, Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw temperature circle
        painter.drawPie(int(center_temperature.x - radius), int(center_temperature.y - radius),
                        int(2 * radius), int(2 * radius),
                        int(start_angle_temperature * 16), int(span_angle_temperature * 16))

        # Set the fill color and brush
        fill_color_rectangles = QColor(255, 255, 255)
        brush = QBrush(fill_color_rectangles, Qt.SolidPattern)
        painter.setBrush(brush)

        # Draw A/C button
        painter.drawRect(self.ac_rect)
        # Draw Left seat heat
        painter.drawRect(self.left_seat_rect)
        # Draw Right seat heat
        painter.drawRect(self.right_seat_rect)

        painter.drawRect(self.decrease_temperature_rect)
        painter.drawRect(self.increase_temperature_rect)
        painter.drawRect(self.decrease_ventilation_rect)
        painter.drawRect(self.increase_ventilation_rect)

        # AC spot
        if self.ac_status == 0:
            fill_color_spots = QColor(128, 128, 128)
        else:
            fill_color_spots = QColor(255, 165, 0)
        brush = QBrush(fill_color_spots, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(500, 58, 15, 15)

        # Left seat heat spot
        if self.left_seat_heat_status == 0:
            fill_color_spots = QColor(128, 128, 128)
        else:
            fill_color_spots = QColor(255, 165, 0)
        brush = QBrush(fill_color_spots, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(335, 58, 15, 15)

        # Right seat heat spot
        if self.right_seat_heat_status == 0:
            fill_color_spots = QColor(128, 128, 128)
        else:
            fill_color_spots = QColor(255, 165, 0)
        brush = QBrush(fill_color_spots, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(777, 58, 15, 15)

    def change_ventilation(self, new_nr):
        if new_nr >= 0 and new_nr <= 10:
            self.nr_ventilation = new_nr
            self.lblVentilation.setText(str(new_nr) + "/10")
            self.update()
        else:
            print("Ventilation should be between [0;10]")

    def change_temperature(self, new_deg):
        if new_deg >= 17 and new_deg <= 27:
            self.deg_temperature = new_deg
            self.lblTemperature.setText(str(new_deg) + " \N{DEGREE SIGN}C")
            self.update()
        else:
            print("Temperature should be between [17;27]")

    # Change buttons state

    def change_ac(self):
        self.ac_status = not self.ac_status
        self.update()

    def turn_on_ac(self):
        self.ac_status = 1
        self.update()

    def turn_off_ac(self):
        self.ac_status = 0
        self.update()

    def change_left_seat_heat(self):
        self.left_seat_heat_status = not self.left_seat_heat_status
        self.update()

    def turn_on_left_seat_heat(self):
        self.left_seat_heat_status = 1
        self.update()

    def turn_off_left_seat_heat(self):
        self.left_seat_heat_status = 0
        self.update()

    def change_right_seat_heat(self):
        self.right_seat_heat_status = not self.right_seat_heat_status
        self.update()

    def turn_on_right_seat_heat(self):
        self.right_seat_heat_status = 1
        self.update()

    def turn_off_right_seat_heat(self):
        self.right_seat_heat_status = 0
        self.update()

    # detect if a button is clicked
    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        if (self.left_seat_rect.x() <= x <= self.left_seat_rect.x() + self.left_seat_rect.width()) and (
                self.left_seat_rect.y() <= y <= self.left_seat_rect.y() + self.left_seat_rect.height()):
            self.change_left_seat_heat()
        elif (self.ac_rect.x() <= x <= self.ac_rect.x() + self.ac_rect.width()) and (
                self.ac_rect.y() <= y <= self.ac_rect.y() + self.ac_rect.height()):
            self.change_ac()
        elif (self.right_seat_rect.x() <= x <= self.right_seat_rect.x() + self.right_seat_rect.width()) and (
                self.right_seat_rect.y() <= y <= self.right_seat_rect.y() + self.right_seat_rect.height()):
            self.change_right_seat_heat()
        elif (
                self.decrease_temperature_rect.x() <= x <= self.decrease_temperature_rect.x() + self.decrease_temperature_rect.width()) and (
                self.decrease_temperature_rect.y() <= y <= self.decrease_temperature_rect.y() + self.decrease_temperature_rect.height()):
            self.decrease_temperature()
        elif (
                self.increase_temperature_rect.x() <= x <= self.increase_temperature_rect.x() + self.increase_temperature_rect.width()) and (
                self.increase_temperature_rect.y() <= y <= self.increase_temperature_rect.y() + self.increase_temperature_rect.height()):
            self.increase_temperature()
        elif (
                self.decrease_ventilation_rect.x() <= x <= self.decrease_ventilation_rect.x() + self.decrease_ventilation_rect.width()) and (
                self.decrease_ventilation_rect.y() <= y <= self.decrease_ventilation_rect.y() + self.decrease_ventilation_rect.height()):
            self.decrease_ventilation()
        elif (
                self.increase_ventilation_rect.x() <= x <= self.increase_ventilation_rect.x() + self.increase_ventilation_rect.width()) and (
                self.increase_ventilation_rect.y() <= y <= self.increase_ventilation_rect.y() + self.increase_ventilation_rect.height()):
            self.increase_ventilation()

    # change temperature and ventilation
    def decrease_temperature(self):
        self.change_temperature(self.deg_temperature - 1)

    def increase_temperature(self):
        self.change_temperature(self.deg_temperature + 1)

    def decrease_ventilation(self):
        self.change_ventilation(self.nr_ventilation - 1)

    def increase_ventilation(self):
        self.change_ventilation(self.nr_ventilation + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget_climatronic = ClimatronicWidget()
    widget_climatronic.resize(1000, 500)
    widget_climatronic.show()
    sys.exit(app.exec_())