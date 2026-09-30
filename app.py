import streamlit as st
import tempfile, os

st.set_page_config(page_title="Bambara Dubber V3 Light")
st.title("🎙️ Bamanankan Dubber - V3 Light")
st.markdown("Angilɛ → Bamanankan")

@st.cache_resource
def load_whisper():
    import whisper
    return whisper.load_model("small")

@st.cache_resource
def get_ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

uploaded = st.file_uploader("Video (English)", type=["mp4","mp3","wav","m4a"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        input_path = tmp.name
    st.video(input_path)

    if st.button("Traduire en Bambara 🚀"):
        with st.spinner("A bɛ baara la..."):
            ffmpeg_exe = get_ffmpeg()
            audio_path = input_path + ".wav"
            os.system(f'"{ffmpeg_exe}" -y -i "{input_path}" -ar 16000 -ac 1 "{audio_path}"')

            model = load_whisper()
            result = model.transcribe(audio_path, language="en")
            english_text = result["text"]
            
            st.info(f"**Angilɛ:** {english_text}")

            try:
                from deep_translator import GoogleTranslator
                bambara = GoogleTranslator(source='en', target='bm').translate(english_text)
                st.success("**Bamanankan na:**")
                st.markdown(f"### {bambara}")
            except Exception as e:
                st.warning(f"Traduction error: {e}")
                st.write("Mais transcription bɛ yen!")
