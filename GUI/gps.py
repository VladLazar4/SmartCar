import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class GPSWidget(QWidget):
    def __init__(self):
        super().__init__()

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
        self.load_google_maps()

        self.update()

    def load_google_maps(self):
        self.webview = QWebEngineView(self)
        self.webview.loadFinished.connect(self.on_load_finished)
        self.webview.setMinimumSize(400, 360)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.addWidget(self.webview)
        layout.addStretch()
        self.setLayout(layout)

        self.directions_from="Cluj-Napoca"
        self.directions_to="Cluj-Napoca"

        map_url = f"https://www.waze.com/ro/live-map/directions/{self.directions_from}?to={self.directions_to}"
        #map_url = f"https://www.google.com/maps/dir/{self.directions_from}/{self.directions_to}"
        self.webview.setUrl(QUrl(map_url))
        #print(self.webview.url())

    def on_load_finished(self):
        self.webview.page().runJavaScript("""
            function clickStartButton() {
                var startButton = document.getElementsByClassName("section-directions-action-icon")[0];
                if (startButton) {
                    startButton.click();
                } else {
                    setTimeout(clickStartButton, 500);
                }
            }
            clickStartButton();
        """)

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
        self.webview.reload()
        self.directions_from = "zorilor"
        self.directions_to = "centru"
        self.load_google_maps()
        self.update()

    def change_goaddress(self, directions_from, directions_to):
        self.webview.reload()
        self.directions_from = directions_from
        self.directions_to = directions_to
        self.load_google_maps()
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget_gps = GPSWidget()
    widget_gps.resize(1000, 500)
    widget_gps.show()
    sys.exit(app.exec_())