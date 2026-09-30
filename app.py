import streamlit as st
import whisper
import tempfile
import os
import json
import time

st.set_page_config(page_title="Bamanankan Dubber PRO", layout="centered")
st.title("Bamanankan Dubber PRO - 3 en 1")

# --- 1. DICTIONNAIRE CORRECTION ---
CORRECTIONS_BASE = {
    "hello": "I ni ce",
    "thank you": "I ni ce kosɔbɛ",
    "how are you": "I ka kɛnɛ?",
    "i am fine": "N ka kɛnɛ",
    "president": "perésidan",
    "america": "Ameriki",
    "people": "mɔgɔw",
    "water": "ji",
    "food": "dumuni",
}

# Charge corrections apprises
if os.path.exists("corrections.json"):
    with open("corrections.json", "r") as f:
        CORRECTIONS_APP = json.load(f)
else:
    CORRECTIONS_APP = {}

def corriger_texte(bambara_text):
    for mauvais, bon in CORRECTIONS_BASE.items():
        bambara_text = bambara_text.replace(mauvais, bon)
    for mauvais, bon in CORRECTIONS_APP.items():
        bambara_text = bambara_text.replace(mauvais, bon)
    return bambara_text

# --- UI ---
uploaded = st.file_uploader("Video upload", type=["mp4","mov","mp3","wav"])

if uploaded:
    st.video(uploaded)
    if st.button("Traduire 🚀"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        with st.spinner("Transcription..."):
            model = whisper.load_model("tiny")
            result = model.transcribe(tmp_path)
            english_text = result["text"]
            st.info(f"Angilɛ: {english_text}")

        bambara_final = ""
        with st.spinner("Traduction NLLB (Meilleur que Google)..."):
            try:
                # 2. NLLB - Meilleur pour Bambara
                from transformers import pipeline
                translator = pipeline("translation", model="facebook/nllb-200-distilled-600M",
                                    src_lang="eng_Latn", tgt_lang="bam_Latn")
                short = english_text[:400]
                out = translator(short, max_length=400)
                bambara_final = out[0]['translation_text']
                st.success(f"NLLB: {bambara_final}")
            except Exception as e:
                st.warning(f"NLLB lourd, fallback Google... ({e})")
                try:
                    from deep_translator import GoogleTranslator
                    time.sleep(1)
                    short = english_text[:480]
                    bambara_final = GoogleTranslator(source='en', target='bm').translate(short)
                    st.success(f"Google: {bambara_final}")
                except Exception as e2:
                    st.error(f"Google bloqué: {e2}")
                    bambara_final = english_text

        # 1. Applique corrections
        bambara_corrige = corriger_texte(bambara_final)
        st.markdown("### ✅ Bamanankan Final Corrigé:")
        st.markdown(f"**{bambara_corrige}**")

        # 3. APPRENTISSAGE - Tu corriges!
        st.markdown("---")
        st.markdown("### 3. I bɛ a ɲɛ ka app kalan?")
        user_correction = st.text_input("Ni fili bɛ yen, Bamanankan ɲuman sɛbɛn yan:")
        if st.button("Sauvegarder correction"):
            if user_correction:
                CORRECTIONS_APP[bambara_final[:50]] = user_correction
                with open("corrections.json", "w") as f:
                    json.dump(CORRECTIONS_APP, f)
                st.balloons()
                st.success("I ni ce! App ye i ka correction mara!")

        os.unlink(tmp_path)
