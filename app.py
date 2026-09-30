import streamlit as st
import tempfile, os

st.set_page_config(page_title="Bambara Dubber V3", page_icon="🎙️")
st.title("🎙️ Bamanankan Dubber - V3")
st.markdown("Angilɛ → Bamanankan 🔄")

@st.cache_resource
def load_models():
    import whisper
    from transformers import pipeline
    whisper_model = whisper.load_model("small")
    # NLLB ye Bambara dɔn!
    translator = pipeline("translation", model="facebook/nllb-200-distilled-600M",
                          src_lang="eng_Latn", tgt_lang="bam_Latn")
    return whisper_model, translator

@st.cache_resource
def get_ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

uploaded = st.file_uploader("Video (English)", type=["mp4","mp3","wav"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        input_path = tmp.name
    st.video(input_path)

    if st.button("Traduire en Bambara 🚀"):
        with st.spinner("Transcription + Traduction..."):
            ffmpeg_exe = get_ffmpeg()
            audio_path = input_path + ".wav"
            os.system(f'"{ffmpeg_exe}" -y -i "{input_path}" -ar 16000 -ac 1 "{audio_path}"')

            whisper_model, translator = load_models()
            result = whisper_model.transcribe(audio_path, language="en")
            english_text = result["text"]

            st.markdown("**Angilɛkan:**")
            st.write(english_text)

            bambara_text = translator(english_text, max_length=500)[0]['translation_text']

            st.success("**Bamanankan na:**")
            st.write(f"### {bambara_text}")
