from time import sleep

import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

file_input = open(r"C:\Users\vlad.lazar\Desktop\SmartCar\voice_input.txt", 'w')
file_output = open(r"C:\Users\vlad.lazar\Desktop\SmartCar\voice_output.txt", 'r')
# file_input = open(r"D:\Vlad\SmartCar\voice_input.txt", 'w')
# file_output = open(r"D:\Vlad\SmartCar\voice_output.txt", 'r')
def write_text():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2)

            valid_text = False
            while valid_text == False:
                print("Listening..")
                # audio2 = r.listen(source2)
                try:
                    my_text = input(">>")
                    # my_text = r.recognize_google(audio2)
                    # my_text = my_text.lower()

                    # if my_text.strip():
                    if my_text != "0":
                        print(f"Command: {my_text}")
                        file_input.seek(0)
                        file_input.write(my_text)
                        file_input.write('\0')
                        file_input.flush()
                        valid_text = True
                    else:
                        sleep(0)

                except sr.UnknownValueError:
                    sleep(0)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

def speak_text():
    engine = pyttsx3.init()
    content = file_output.read()
    result = content.split('\0')
    command = result[0]
    engine.say(command)
    engine.runAndWait()



if __name__ == '__main__':
    # v = VoiceAssistant()
    # v.speak_text("hello")
    print(1)