import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import sounddevice as sd
import wavio
import tempfile


def record_audio(duration=5, fs=44100):
    """Record audio from the microphone and save it as a temporary WAV file."""
    try:
        st.info(f"Recording for {duration} seconds... Please speak into the microphone.")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until the recording is finished
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
            audio_file_path = temp_audio_file.name
            wavio.write(audio_file_path, recording, fs, sampwidth=2)
        st.success("Recording finished!")
        return audio_file_path
    except Exception as e:
        st.error(f"An unexpected error occurred during recording: {e}")
        return None


def recognize_speech_from_audio(audio_file_path, language):
    """Recognize speech from an audio file and convert it to text."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.RequestError as e:
        st.error(f"Could not request results from the speech recognition service: {e}")
    except sr.UnknownValueError:
        st.error("Could not understand the audio")
    except Exception as e:
        st.error(f"An unexpected error occurred during speech recognition: {e}")
    return None


def translate_text(text, src_lang, dest_lang):
    """Translate text from one language to another."""
    try:
        translator = Translator()
        translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
        return translated_text
    except Exception as e:
        st.error(f"An error occurred while translating: {e}")
        return None


def main():
    st.title("Türkçe ve İngilizce Çeviri Uygulaması")

    st.write("Sesinizi kaydedin ve Türkçe ile İngilizce arasında çeviri yapın.")
    st.write("Please record your speech for translation between Turkish and English.")

    language_choice = st.radio("Choose translation direction / Çeviri yönünü seçin:", ["TR to ENG", "ENG to TR"])

    audio_file_path = None

    if st.button("Record Audio"):
        audio_file_path = record_audio()
        if audio_file_path:
            st.audio(audio_file_path)

    if audio_file_path:
        if language_choice == "TR to ENG":
            text = recognize_speech_from_audio(audio_file_path, "tr-TR")
            if text:
                st.write("Recognized Text (Turkish):")
                st.write(text)
                translated_text = translate_text(text, "tr", "en")
                if translated_text:
                    st.write("Translated Text (English):")
                    st.write(translated_text)
        elif language_choice == "ENG to TR":
            text = recognize_speech_from_audio(audio_file_path, "en-US")
            if text:
                st.write("Recognized Text (English):")
                st.write(text)
                translated_text = translate_text(text, "en", "tr")
                if translated_text:
                    st.write("Translated Text (Turkish):")
                    st.write(translated_text)


if __name__ == "__main__":
    main()
