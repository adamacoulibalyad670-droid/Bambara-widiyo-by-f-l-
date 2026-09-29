import streamlit as st
import tempfile, subprocess

st.set_page_config(page_title="Bambara Dubber", page_icon="🎙️")
st.title("🎙️ Bamanankan Dubber")
st.markdown("**a ka fisa - Video to Bambara** - خفيف وسريع ⚡")

@st.cache_resource
def load_whisper():
    import whisper
    return whisper.load_model("tiny")

uploaded = st.file_uploader("ارفع فيديو", type=["mp4","mov","mkv","avi","mp3","wav"])

if uploaded:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded.read())
    st.video(tfile.name)

    if st.button("🚀 ابدأ الدبلجة للبامبارا"):
        audio_path = tfile.name.replace(".mp4",".wav")
        subprocess.run(["ffmpeg","-y","-i",tfile.name,"-vn","-ac","1","-ar","16000",audio_path], check=True)
        
        with st.spinner("جاري الاستماع..."):
            model = load_whisper()
            result = model.transcribe(audio_path, language="fr")
            text = result["text"]
            st.text_area("النص الأصلي FR", text, height=100)

        with st.spinner("ترجمة للبامبارا..."):
            try:
                from deep_translator import GoogleTranslator
                bam = GoogleTranslator(source='fr', target='bm').translate(text)
            except:
                bam = text  # اذا فشل، اعرض الأصلي
            
            st.success("تم! 🎉")
            st.text_area("Bamanankan (Bambara)", bam, height=180)
            st.balloons()
else:
    st.info("👆 ارفع فيديو 10 ثواني للبدء - الآن سريع وخفيف!")
