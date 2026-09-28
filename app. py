import streamlit as st
import os
import sys
import tempfile
import subprocess

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(page_title="Bambara Video Dubber Pro", layout="wide", page_icon="🎙️")

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #FF6B35; text-align: center; }
    .stButton>button { background-color: #FF6B35; color: white; width: 100%; height: 3em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">Bamanankan Video Dubber Pro</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">Dub your videos to Bambara / Bamanankan</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ الإعدادات الاحترافية")
    st.markdown("**Author:** Bourama")
    quality = st.selectbox("جودة الإخراج", ["Medium", "High", "Fast"])
    st.info("✅ FFmpeg مثبت\n✅ التطبيق جاهز")

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except:
        return False

ffmpeg_ok = check_ffmpeg()
if not ffmpeg_ok:
    st.error("❌ FFmpeg غير مثبت")
else:
    st.success("✅ FFmpeg يعمل")

uploaded_file = st.file_uploader("📤 ارفع فيديو MP4", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    st.video(video_path)
    st.write(f"الحجم: {uploaded_file.size/1024/1024:.2f} MB")
    
    if st.button("🚀 بدء الدبلجة الاحترافية"):
        with st.spinner("جاري المعالجة..."):
            audio_path = video_path.replace(".mp4", ".wav")
            cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", audio_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if os.path.exists(audio_path):
                st.success("✅ تم استخراج الصوت")
                st.audio(audio_path)
            else:
                st.error(f"فشل: {result.stderr[:500]}")
else:
    st.info("👆 ارفع فيديو لبدء")
