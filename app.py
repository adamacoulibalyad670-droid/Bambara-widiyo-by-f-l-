import streamlit as st
import whisper
import tempfile
import os
from deep_translator import MyMemoryTranslator, GoogleTranslator
import time

st.set_page_config(page_title="Bamanankan Dubber V3 Light", layout="centered")
st.title("Bamanankan Dubber - V3 Light")

uploaded = st.file_uploader("Video kelen upload", type=["mp4","mov","mp3","wav"])

if uploaded:
    st.video(uploaded)
    if st.button("Traduire en Bambara 🚀"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        with st.spinner("Transcription..."):
            model = whisper.load_model("tiny")
            result = model.transcribe(tmp_path)
            english_text = result["text"]
            st.info(f"Angilɛ: {english_text}")

        # Traduction avec protection anti-blocage
        with st.spinner("Traduction en Bambara..."):
            text_short = english_text[:500]  # Limite pour éviter blocage
            
            bambara = ""
            try:
                # Essaie MyMemory d'abord (gratuit, pas de limite)
                bambara = MyMemoryTranslator(source='en-US', target='bm').translate(text_short)
                st.success(f"Bamanankan na: {bambara}")
            except Exception as e:
                st.warning(f"MyMemory echoué, essaie Google par morceaux... {e}")
                try:
                    words = text_short.split()
                    parts = []
                    for i in range(0, len(words), 15):
                        chunk = " ".join(words[i:i+15])
                        if chunk.strip():
                            p = GoogleTranslator(source='en', target='bm').translate(chunk)
                            parts.append(p)
                            time.sleep(1.2)  # Pause pour Google
                    bambara = " ".join(parts)
                    st.success(f"Bamanankan na: {bambara}")
                except Exception as e2:
                    st.error(f"Traduction error: {e2}")
                    st.write(f"Mais transcription bɛ yen! Angilɛ: {text_short}")

        os.unlink(tmp_path)
