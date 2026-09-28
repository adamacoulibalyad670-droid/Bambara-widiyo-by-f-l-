import streamlit as st
import tempfile, subprocess, os

st.set_page_config(page_title="Bambara Dubber", page_icon="🎙️", layout="centered")
st.title("🎙️ Bamanankan Dubber Pro")
st.markdown("**a ka fisa - Video to Bambara** | Author: Bourama")

@st.cache_resource
def load_whisper():
    import whisper
    return whisper.load_model("tiny")

uploaded = st.file_uploader("📤 ارفع فيديو (فرنسي/انجليزي)", type=["mp4","mov","mkv","avi"])

if uploaded:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded.read())
    st.video(tfile.name)

    if st.button("🚀 ابدأ الدبلجة للبامبارا"):
        # 1. استخراج الصوت
        audio_path = tfile.name.replace(".mp4",".wav")
        subprocess.run(["ffmpeg","-y","-i",tfile.name,"-vn","-ac","1","-ar","16000",audio_path], check=True)
        st.success("✅ 1/3 تم استخراج الصوت")

        # 2. تفريغ النص
        with st.spinner("2/3 جاري الاستماع..."):
            model = load_whisper()
            result = model.transcribe(audio_path, language="fr")
            text = result["text"]
            st.text_area("النص الأصلي", text, height=100)

        # 3. ترجمة للبامبارا
        with st.spinner("3/3 ترجمة للبامبارا..."):
            from transformers import pipeline
            translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", src_lang="fra_Latn", tgt_lang="bam_Latn", max_length=400)
            bambara = translator(text)[0]['translation_text']
            st.success("✅ الترجمة اكتملت!")
            st.text_area("النص بالبامبارا - Bamanankan", bambara, height=150)
            st.balloons()
else:
    st.info("👆 ارفع فيديو للبدء")

st.markdown("---")
st.caption("v2.0 - NLLB + Whisper | packages.txt must contain ffmpeg")
