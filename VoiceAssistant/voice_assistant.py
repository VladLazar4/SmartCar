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

                print("I am listening...")
                audio2 = r.listen(source2)
                print(audio2)

                my_text = r.recognize_google(audio2)
                my_text = my_text.lower()

                return my_text

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return "ERROR"

        except sr.UnknownValueError:
            print("unknown error occurred")
            return "ERROR"
