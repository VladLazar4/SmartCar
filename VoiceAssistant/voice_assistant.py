import threading
import keyboard
from time import sleep

import self as self
import speech_recognition as sr
import pyttsx3
from PyQt5.QtCore import QThread, pyqtSignal

r = sr.Recognizer()

# file_input = open(r"C:\Users\vlad.lazar\Desktop\SmartCar\voice_input.txt", 'w')
# file_output = open(r"C:\Users\vlad.lazar\Desktop\SmartCar\voice_output.txt", 'r')


file_input = open(r"D:\Vlad\SmartCar\voice_input.txt", 'w')
file_output = open(r"D:\Vlad\SmartCar\voice_output.txt", 'r')

waiting_time = 30
timer_active = False
def unlock_assistant():
    while True:
        if keyboard.is_pressed('ctrl'):
            break
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2)
            valid_text = False
            while valid_text == False:
                print("Listening..")
                audio2 = r.listen(source2)
                try:
                    my_text = r.recognize_google(audio2)
                    # my_text = input(">>")
                    my_text = my_text.lower()

                    if my_text == "hello":
                        speak_text_("How may I help you?")
                        valid_text = True
                    else:
                        sleep(0)
                except sr.UnknownValueError:
                    sleep(0)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    global timer_active
    thread_start_timer = threading.Thread(target=start_timer)
    thread_start_timer.start()
    timer_active = True

def write_text():
    global timer_active
    if timer_active==False:
        unlock_assistant()
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2)

            valid_text = False
            while valid_text == False and timer_active == True:
                global waiting_time
                if waiting_time:
                    audio2 = r.listen(source2)
                    try:
                        # my_text = input(">>")
                        my_text = r.recognize_google(audio2)
                        my_text = my_text.lower()

                        if my_text != "0":
                            print(f"Command: {my_text}")
                            file_input.seek(0)
                            file_input.write(my_text)
                            file_input.write('\0')
                            file_input.flush()
                            valid_text = True
                            waiting_time = 30
                        else:
                            sleep(0)
                    except sr.UnknownValueError:
                        sleep(0)
                else:
                    print("Time is up")

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))


def speak_text():
    engine = pyttsx3.init()
    file_output.seek(0)
    content = file_output.read()
    result = content.split('\0')
    command = result[0]
    print(f"Spoke: {command}")
    engine.say(command)
    engine.runAndWait()


def speak_text_(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def start_timer():
    v = VoiceAssistant()
    v.run()

class VoiceAssistant(QThread):
    show_mic_signal = pyqtSignal(int)
    hide_mic_signal = pyqtSignal(int)
    def run(self):
        global waiting_time, timer_active
        waiting_time = 30
        self.show_mic_signal.emit(1)
        while waiting_time:
            # print(waiting_time)
            sleep(1)
            waiting_time -= 1
        timer_active = False
        self.hide_mic_signal.emit(1)


if __name__ == '__main__':
    # start_timer()
    print(1)
