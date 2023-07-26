import re
import json
from urllib.request import urlopen

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication

import openai

openai.api_key = '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'
messages = [{"role": "system", "content":
    "You are a intelligent assistant."}]


class OpenAI(QThread):
    turn_on_ac_signal = pyqtSignal(int)
    turn_off_ac_signal = pyqtSignal(int)
    turn_on_left_seat_heat_signal = pyqtSignal(int)
    turn_off_left_seat_heat_signal = pyqtSignal(int)
    turn_on_right_seat_heat_signal = pyqtSignal(int)
    turn_off_right_seat_heat_signal = pyqtSignal(int)
    change_ventilation_signal = pyqtSignal(int)
    change_temperature_signal = pyqtSignal(int)
    change_radio_signal = pyqtSignal(int)
    change_bt_signal = pyqtSignal(int)
    change_cd_signal = pyqtSignal(int)
    increase_frecv_signal = pyqtSignal(int)
    decrease_frecv_signal = pyqtSignal(int)
    change_volume_signal = pyqtSignal(int)
    change_gohome_signal = pyqtSignal(int)
    change_home_signal = pyqtSignal(str)
    change_goaddress_signal = pyqtSignal(str)
    change_pitstop_signal = pyqtSignal(str)

    speak_text_signal = pyqtSignal(str)
    write_text_signal = pyqtSignal(int)

    def run(self):
        message = "I want you to learn some responses that I expect from you when I ask some tasks. Linked to a climatronic: turn on/off the ac, turn on/off the heat for the left/right seat, or change ventilation to a specific intensity 0-10, or the temperature 17-27 degrees. Linked to media: change the source to radio/bluetooth/cd, set the radio/song/track between 1-10, change the volume 0-10. Linked to maps: go to…, go home, new home address is…(R: new home address is …), add pitstop…(R: pitstop added to…). For the following commands, your responses should be short, concise and respect exactly the pattern where it is specified that you have done the desired action. If you understood this task, just respond “OK”."
        self.first_run = True
        while True:
            # if message:
            # 	messages.append(
            # 		{"role": "user", "content": message},
            # 	)
            # 	chat = openai.ChatCompletion.create(
            # 		model="gpt-3.5-turbo", messages=messages
            # 	)
            # reply = chat.choices[0].message.content
            reply = message
            reply = reply.casefold()
            if self.first_run == False:
                self.speak_text_signal.emit(reply)
                if reply.find("track") != -1:
                    num = re.findall(r'\d+', reply)
                    self.change_cd_signal.emit(1)
                    if len(num) == 1:
                        self.increase_frecv_signal.emit(int(num[0]))
                elif reply.find("ac") != -1:
                    if reply.find("on") != -1:
                        self.turn_on_ac_signal.emit(1)
                    else:
                        self.turn_off_ac_signal.emit(1)
                elif reply.find("seat") != -1:
                    if reply.find("left") != -1:
                        if reply.find("on") != -1:
                            self.turn_on_left_seat_heat_signal.emit(1)
                        else:
                            self.turn_off_left_seat_heat_signal.emit(1)
                    else:
                        if reply.find("on") != -1:
                            self.turn_on_right_seat_heat_signal.emit(1)
                        else:
                            self.turn_off_right_seat_heat_signal.emit(1)
                elif reply.find("ventilation") != -1:
                    num = re.findall(r'\d+', reply)
                    if len(num) == 0:
                        if reply.find("max") != -1 or reply.find("high") != -1:
                            self.change_ventilation_signal.emit(10)
                        elif reply.find("min") != -1 or reply.find("off") != -1 or reply.find("low") != -1:
                            self.change_ventilation_signal.emit(0)
                    elif len(num) == 1:
                        self.change_ventilation_signal.emit(int(num[0]))
                elif reply.find("temperature") != -1:
                    num = re.findall(r'\d+', reply)
                    if len(num) == 0:
                        if reply.find("max") != -1 or reply.find("high") != -1:
                            self.change_temperature_signal.emit(27)
                        elif reply.find("min") != -1 or reply.find("low") != -1 or reply.find("off") != -1:
                            self.change_temperature_signal.emit(17)
                    if len(num) == 1:
                        self.change_temperature_signal.emit(int(num[0]))
                elif reply.find("radio") != -1:
                    num = re.findall(r'\d+', reply)
                    self.change_radio_signal.emit(1)
                    if len(num) == 1:
                        self.increase_frecv_signal.emit(int(num[0]))
                elif reply.find("bluetooth") != -1:
                    self.change_bt_signal.emit(1)
                elif reply.find("cd") != -1:
                    self.change_cd_signal.emit(1)
                elif reply.find("song") != -1:
                    num = re.findall(r'\d+', reply)
                    self.change_bt_signal.emit(1)
                    if len(num) == 1:
                        self.increase_frecv_signal.emit(int(num[0]))
                elif reply.find("volume") != -1:
                    num = re.findall(r'\d+', reply)
                    if len(num) == 0:
                        if reply.find("max") != -1:
                            self.change_volume_signal.emit(10)
                        elif reply.find("min") != -1:
                            self.change_volume_signal.emit(0)
                    if len(num) == 1:
                        self.change_volume_signal.emit(int(num[0]))
                elif reply.find("mute") != -1:
                    self.change_volume_signal.emit(0)
                elif reply.find("home") != -1:
                    if reply.find("new") != -1:
                        self.change_home_signal.emit(parse_address(reply, reply.find("is ") + 3))
                    else:
                        self.change_gohome_signal.emit(1)
                elif reply.find("going to") != -1 or reply.find("navigating to") != -1:
                    self.change_goaddress_signal.emit(parse_address(reply, reply.find("to ") + 3))
                elif reply.find("pitstop") != -1:
                    self.change_pitstop_signal.emit(parse_address(reply, reply.find("to ") + 3))
            else:
                self.first_run = False

            # messages.append({"role": "assistant", "content": reply})
            # message = self.write_text_signal.emit(1)
            message = input(">>")

def parse_address(string, from_p):
    new_string = string[from_p:]
    return new_string


if __name__ == '__main__':
    print(1)