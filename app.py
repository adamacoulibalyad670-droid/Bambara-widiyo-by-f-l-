import streamlit as st
import tempfile, os

st.set_page_config(page_title="Bambara Dubber", page_icon="🎙️")
st.title("🎙️ Bamanankan Dubber - V2")

@st.cache_resource
def load_whisper():
    import whisper
    return whisper.load_model("small") # small ka fisa ni tiny ye

@st.cache_resource
def get_ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

uploaded = st.file_uploader("Video upload", type=["mp4","mp3","wav","m4a"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        input_path = tmp.name
    st.video(input_path)
    
    if st.button("A transcrire 🚀"):
        with st.spinner("A bɛ baara la..."):
            ffmpeg_exe = get_ffmpeg()
            audio_path = input_path + ".wav"
            os.system(f'"{ffmpeg_exe}" -y -i "{input_path}" -ar 16000 -ac 1 "{audio_path}"')
            
            model = load_whisper()
            result = model.transcribe(audio_path) # auto langue - Bambara be se ka sɔrɔ
            st.success("Ban!")
            st.write(result["text"])
            st.audio(audio_path)
