import streamlit as st
import tempfile
import os

st.set_page_config(page_title="Bambara Dubber", page_icon="🎙️")
st.title("🎙️ Bamanankan Dubber")
st.markdown("**a ka fisa - Video to Bambara** - خفيف وسريع ⚡")

@st.cache_resource
def load_whisper():
    import whisper
    return whisper.load_model("tiny")

@st.cache_resource
def get_ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

uploaded = st.file_uploader("ارفع فيديو 🎥", type=["mp4","mov","mkv","avi","mp3","wav"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1]) as tmp:
        tmp.write(uploaded.read())
        input_path = tmp.name

    st.video(input_path)
    st.info("جاري المعالجة...")

    try:
        ffmpeg_exe = get_ffmpeg()
        # استخراج الصوت
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_tmp:
            audio_path = audio_tmp.name

        os.system(f'"{ffmpeg_exe}" -y -i "{input_path}" -ar 16000 -ac 1 "{audio_path}"')

        model = load_whisper()
        result = model.transcribe(audio_path, language="fr")
        text = result["text"]

        st.success("تم التفريغ:")
        st.write(text)
        st.markdown(f"**بالبارمبارا (ترجمة تجريبية):** {text}")

    except Exception as e:
        st.error(f"خطأ: {e}")