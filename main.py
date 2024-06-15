import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import time


def record_text_tr(recognizer):
    """kullanıcıdan gelen sesi tanımlayıp metin olarak returnlıyor"""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("dinleniyor...")
            audio = recognizer.listen(source)
            print("algılanıyor...")
            turkish_text = recognizer.recognize_google(audio, language="tr-TR")
            return turkish_text
    except sr.RequestError as e:
        print(f"could not request results from the speech recognition service; {e}")
    except sr.UnknownValueError:
        print("we could not understand audio")
    except Exception as e:
        print(f"an unexpected error occurred during recording: {e}")
    return None


def record_text_en(recognizer):
    """kullanıcıdan gelen sesi tanımlayıp metin olarak returnlıyor"""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("listening...")
            audio = recognizer.listen(source)
            print("recognizing...")
            english_text = recognizer.recognize_google(audio, language="en-EN")
            return english_text
    except sr.RequestError as e:
        print(f"could not request results from the speech recognition service; {e}")
    except sr.UnknownValueError:
        print("we could not understand audio")
    except Exception as e:
        print(f"an unexpected error occurred during recording: {e}")
    return None


def translate_text(text, user_choice):
    """türkçe olarak gelen metni ingilizceye çevirmek için"""
    try:
        translator = Translator()
        if user_choice == '1':
            result_text = translator.translate(text, src="en", dest="tr").text
        else:
            result_text = translator.translate(text, src="tr", dest="en").text
        return result_text
    except Exception as e:
        print(f"error occured while translating: {e}")
        return None


def text_to_audio(engine, text):
    """Convert the given text to speech using the provided TTS engine."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")


def main():
    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()

    try:
        while True:

            print("Press Enter to start recording or 'q' to quit:")
            user_input = input().strip().lower()
            if user_input == 'q':
                break
            print("Press Enter 1 for english to turkish or 2 for turkish to english")
            user_choice = input().strip().lower()

            if user_choice == '1':
                text = record_text_en(recognizer)
            else:
                text = record_text_tr(recognizer)

            if text:
                print(text)
                translated_text = translate_text(text, user_choice)
                if translated_text:
                    print(translated_text)
                    text_to_audio(tts_engine, translated_text)

            # Pause briefly to give user time to read the console
            time.sleep(1)

    except KeyboardInterrupt:
        print("Process interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
