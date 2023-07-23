import sys
from time import sleep

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

class GPSWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.raise_()

        self.gohome_status = 0
        self.gohome_rect = QRect(400, 450, 130, 30)

        self.lblGoHome = QLabel("Go home", self)
        self.lblGoHome.move(415, 453)
        self.lblGoHome.setFont(QFont("Arial", 16))

        self.lblGPS = QLabel("GPS", self)
        self.lblGPS.move(430, 15)
        self.lblGPS.setFont(QFont("Arial", 16))

        self.directions_from = ""
        self.directions_to = ""
        self.directions_pitstop = ""
        self.home_address = "targu mures, centru"

        # Create the web view and load Google Maps
        self.webview = QWebEngineView(self)
        self.webview.setMinimumSize(400, 360)
        self.load_google_maps()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.addWidget(self.webview)
        layout.addStretch()

    def load_google_maps(self):
        if self.directions_pitstop == "":
            map_url = f"https://www.google.com/maps/dir/{self.directions_from}/{self.directions_to}"
        else:
            map_url = f"https://www.google.com/maps/dir/{self.directions_from}/{self.directions_pitstop}/{self.directions_to}"
        self.webview.setUrl(QUrl(map_url))


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(237, 152, 102))
        painter.drawRect(self.rect())

        fill_color_rectangles = QColor(255, 255, 255)
        brush = QBrush(fill_color_rectangles, Qt.SolidPattern)
        painter.setBrush(brush)

        painter.drawRect(self.gohome_rect)

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        if (self.gohome_rect.x() <= x <= self.gohome_rect.x() + self.gohome_rect.width()) and (
                self.gohome_rect.y() <= y <= self.gohome_rect.y() + self.gohome_rect.height()):
            self.change_gohome()

    def current_location(self):
        driver = webdriver.Chrome()  # r'C:\Users\vlad.lazar\Downloads\chromedriver_win32\chromedriver.exe'
        driver.set_window_position(2000, 2000)
        driver.get(
            "https://www.gps-coordinates.net/my-location")
        sleep(2)

        location = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[2]/div[2]/p/span")
        current_location = location.text
        driver.quit()
        return current_location

    def change_gohome(self):
        self.directions_from = self.current_location()
        self.directions_pitstop = ""
        self.directions_to = self.home_address
        self.load_google_maps()

    def change_home(self, new_home_address):
        self.home_address = new_home_address

    def change_pitstop(self, pitstop_address):
        self.directions_pitstop = pitstop_address
        self.load_google_maps()

    def change_goaddress(self, directions_to):
        self.directions_from = self.current_location()
        self.directions_pitstop = ""
        self.directions_to = directions_to
        self.load_google_maps()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget_gps = GPSWidget()
    widget_gps.resize(1000, 500)
    widget_gps.show()
    sys.exit(app.exec_())
