import streamlit as st
from st_audiorec import st_audiorec
import speech_recognition as sr
from googletrans import Translator
import tempfile


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

    # Use st_audiorec to record audio
    st.write("Record your audio below:")
    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        # Save the recorded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
            temp_audio_file.write(wav_audio_data)
            audio_file_path = temp_audio_file.name

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
