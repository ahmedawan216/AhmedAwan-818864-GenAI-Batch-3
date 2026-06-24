import speech_recognition as sr
import pyttsx3
import webbrowser
import time

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Optional: adjust speaking speed
engine.setProperty('rate', 170)

def speak(text):
    print("Chatbot:", text)
    engine.say(text)
    engine.runAndWait()   # ensures speech completes

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You:", command)
        return command
    except:
        return ""

def chatbot():
    speak("Hello! Say YouTube, LinkedIn, GitHub, or Google. Say bye to exit.")

    while True:
        user_input = listen()

        if "youtube" in user_input:
            speak("Opening YouTube")
            time.sleep(1)   # 🔥 important fix
            webbrowser.open("https://www.youtube.com")

        elif "linkedin" in user_input:
            speak("Opening LinkedIn")
            time.sleep(1)
            webbrowser.open("https://www.linkedin.com")

        elif "github" in user_input:
            speak("Opening GitHub")
            time.sleep(1)
            webbrowser.open("https://github.com")

        elif "google" in user_input:
            speak("Opening Google")
            time.sleep(1)
            webbrowser.open("https://www.google.com")

        elif "bye" in user_input:
            speak("Goodbye!")
            break

        else:
            speak("I did not understand that")

chatbot()