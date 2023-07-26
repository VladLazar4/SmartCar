from time import sleep

import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
class VoiceAssistant():
    def speak_text(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def write_text(self):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)

                valid_text=False
                while valid_text==False:
                    audio2 = r.listen(source2)
                    try:
                        my_text = r.recognize_google(audio2)
                        my_text = my_text.lower()

                        if my_text.strip():
                            print(f"Command: {my_text}")
                            file = open("./../file.txt", 'w')
                            file.write(my_text)
                            return my_text
                        else:
                            sleep(0)

                    except sr.UnknownValueError:
                        sleep(0)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return "ERROR"

if __name__ == '__main__':
    v = VoiceAssistant()
    v.write_text()
