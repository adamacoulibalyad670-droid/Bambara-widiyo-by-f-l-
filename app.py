import streamlit as st
import whisper
import tempfile
import os
from deep_translator import MyMemoryTranslator

st.set_page_config(page_title="Bamanankan Dubber", layout="centered")
st.title("Bamanankan Dubber V3 - Fixed")

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

        with st.spinner("Traduction..."):
            try:
                # 1 SEUL request, pas de boucle = pas de blocage Google
                short = english_text[:480]
                bambara = MyMemoryTranslator(source='en-US', target='bm').translate(short)
                st.success(f"Bamanankan na: {bambara}")
            except Exception as e:
                st.error(f"Error: {e}")
                # Fallback: affiche au moins transcription
                st.write(f"Transcription réussie: {english_text}")
                st.write("Traduction Bamanankan: Réessaie dans 1 minute, Google bɛ repos.")

        os.unlink(tmp_path)
