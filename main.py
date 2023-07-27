import sys
import time

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

from GUI import measure_distance
from GUI.climatronic import ClimatronicWidget
from GUI.media import MediaWidget
from GUI.gps import GPSWidget
from GUI.parking_sensors import ParkingSensorsWidget
from VoiceAssistant.openai import OpenAI
from VoiceAssistant.voice_assistant import VoiceAssistant


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.raise_()

        self.climatronic = ClimatronicWidget()
        self.media = MediaWidget()
        self.gps = GPSWidget()
        self.parking_sensors = ParkingSensorsWidget()
        self.openai = OpenAI()
        self.voice_assistant = VoiceAssistant()

        self.openai.turn_on_ac_signal.connect(self.climatronic.turn_on_ac)
        self.openai.turn_off_ac_signal.connect(self.climatronic.turn_off_ac)
        self.openai.turn_on_left_seat_heat_signal.connect(self.climatronic.turn_on_left_seat_heat)
        self.openai.turn_off_left_seat_heat_signal.connect(self.climatronic.turn_off_left_seat_heat)
        self.openai.turn_on_right_seat_heat_signal.connect(self.climatronic.turn_on_right_seat_heat)
        self.openai.turn_off_right_seat_heat_signal.connect(self.climatronic.turn_off_right_seat_heat)
        self.openai.change_ventilation_signal.connect(self.climatronic.change_ventilation)
        self.openai.change_temperature_signal.connect(self.climatronic.change_temperature)
        self.openai.change_radio_signal.connect(self.media.change_radio)
        self.openai.change_cd_signal.connect(self.media.change_cd)
        self.openai.change_bt_signal.connect(self.media.change_bt)
        self.openai.increase_frecv_signal.connect(self.media.increase_frecv)
        self.openai.decrease_frecv_signal.connect(self.media.decrease_frecv)
        self.openai.change_gohome_signal.connect(self.gps.change_gohome)
        self.openai.change_home_signal.connect(self.gps.change_home)
        self.openai.change_goaddress_signal.connect(self.gps.change_goaddress)
        self.openai.change_pitstop_signal.connect(self.gps.change_pitstop)
        self.openai.exit_navigation_signal.connect(self.gps.exit_navigation)
        self.openai.change_volume_signal.connect(self.media.change_volume)
        self.openai.speak_text_signal.connect(self.voice_assistant.speak_text)
        # self.openai.write_text_signal.connect(self.voice_assistant.write_text)
        self.openai.start()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.gps.setFixedHeight(500)

        layout.addWidget(self.climatronic, 0, 0)
        layout.addWidget(self.media, 1, 0)
        layout.addWidget(self.gps, 0, 1)
        layout.addWidget(self.parking_sensors, 1, 1)

        self.setLayout(layout)

        self.setWindowTitle("Smart car")
        self.setGeometry(300, 300, 250, 150)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.showMaximized()
    widget.show()
    window_ret = app.exec_()
    # measure_distance.kill_th()
    sys.exit(window_ret)


#pip install pyqt5
#pip install pyqtwebengine
#pip install openai
#pip install speechrecognition
#pip install pyttsx3
#pip install selenium
#pip install pyaudio
#pip install opencv-python