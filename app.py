import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
import os

st.set_page_config(page_title="Voice Translator", layout="centered")
st.title("🎙️ Voice Translator (Hindi ↔ Tamil)")

language_choice = st.selectbox("Choose the language you will speak:", ["Hindi", "Tamil"])

# Button to trigger recording
if st.button("🎤 Click to Record from Microphone"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎧 Listening... Speak now")
        audio = recognizer.listen(source, timeout=5)
        st.success("✅ Audio captured!")

        try:
            lang_code = 'hi-IN' if language_choice.lower() == 'hindi' else 'ta-IN'
            src_lang = 'hi' if language_choice.lower() == 'hindi' else 'ta'
            dest_lang = 'ta' if src_lang == 'hi' else 'hi'

            recognized_text = recognizer.recognize_google(audio, language=lang_code)
            st.write(f"🗣 You said ({language_choice}):", recognized_text)

            # Translate
            translator = Translator()
            translated = translator.translate(recognized_text, src=src_lang, dest=dest_lang)
            st.write("🌐 Translated:", translated.text)

            # Generate speech with gTTS
            tts = gTTS(text=translated.text, lang=dest_lang)
            tts.save("translated.mp3")
            st.audio("translated.mp3", format="audio/mp3")

        except Exception as e:
            st.error(f"Error: {e}")
