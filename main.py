import speech_recognition as sr
from googletrans import Translator
import pyttsx3

r = sr.Recognizer()


def record_text():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            print("Listening...")
            audio = r.listen(source)
            print("Recognizing...")
            turkish_text = r.recognize_google(audio, language="tr-TR")
            return turkish_text
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.UnknownValueError:
        print("Unknown error occurred")
    return None


def output_text(text):
    try:
        with open("output_file.txt", "w", encoding="utf-8") as ff:
            ff.write(text)
    except IOError as e:
        print(f"File error: {e}")


def translate_text(text):
    try:
        translator = Translator()
        english_text = translator.translate(text, src="tr", dest="en").text
        return english_text
    except Exception as e:
        print(f"Translation error: {e}")
        return None


def text_to_audio(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")


def main():
    try:
        while True:
            text = record_text()
            if text:
                print(f"Turkish Text: {text}")
                output_text(text)
                translated_text = translate_text(text)
                if translated_text:
                    print(f"English Translation: {translated_text}")
                    text_to_audio(translated_text)
    except KeyboardInterrupt:
        print("Process interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
