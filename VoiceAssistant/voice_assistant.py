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

                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print("Did you say: ", MyText)
                self.speak_text(MyText)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")
