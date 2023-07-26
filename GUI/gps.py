import sys
from time import sleep

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

from selenium import webdriver
from selenium.webdriver.common.by import By

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

        self.home_address = "cluj napoca, centru"

        self.navigation_state = False
        self.route_active = False
        self.pitstop_active = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.addStretch()

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

    def change_gohome(self):
        if not self.navigation_state:
            self.open_navigation()
        self.new_route(self.home_address)

    def change_home(self, new_home_address):
        self.home_address = new_home_address

    def change_pitstop(self, pitstop_address):
        if not self.navigation_state:
            self.open_navigation()
        self.add_pitstop(pitstop_address)

    def change_goaddress(self, directions_to):
        if not self.navigation_state:
            self.open_navigation()
        self.new_route(directions_to)

    def new_route(self, to_p):
        if self.route_active == True:
            if self.pitstop_active == True:
                try:
                    cancel_pitstop = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[3]/div[2]/button[2]')
                    cancel_pitstop.click()
                except Exception:
                    sleep(0)
                pass
                self.pitstop_active = False
            try:
                place = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input')
                place.clear()
                place.send_keys(to_p)

                submit = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/button[1]')
                submit.click()
            except Exception:
                sleep(0)
            pass
        else:
            try:
                self.route_active = True
                place = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div/div[2]/form/input[1]')
                place.send_keys(to_p)

                submit = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div/div[2]/div[2]/button/div')
                submit.click()
                sleep(2)

                indicatii = self.driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input')
                indicatii.click()

                #seteaza ca punct de plecare locatia curenta
                start_point = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[4]/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[1]')
                start_point.click()
            except Exception:
                sleep(0)
            pass

    def add_pitstop(self, pitstop_p):
        self.pitstop_active = True
        if not self.navigation_state:
            self.open_navigation()
        if not self.route_active:
            print(f"Navigating to {pitstop_p}")
            self.new_route(pitstop_p)
        else:
            sleep(2)
            add_pitstop = self.driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/button/div[1]/div')
            add_pitstop.click()
            sleep(2)

            textbox_pitstop = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[3]/div[2]/div[1]/div/input')
            textbox_pitstop.send_keys(pitstop_p)
            sleep(2)

            enter_pitstop = self.driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[3]/div[2]/button[1]')
            enter_pitstop.click()
    def open_navigation(self):
        self.navigation_state = True
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.driver.get("https://www.google.com/maps/@46.7826949,23.6179692,14z?entry=ttu")
        sleep(2)

        accept = self.driver.find_element(By.XPATH,'/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
        accept.click()
        self.driver.fullscreen_window()
        sleep(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget_gps = GPSWidget()
    widget_gps.resize(1000, 500)
    widget_gps.show()
    widget_gps.change_goaddress("Targu Mures")
    widget_gps.add_pitstop("Brasov")
    sys.exit(app.exec_())