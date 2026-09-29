import streamlit as st
import tempfile, subprocess

st.set_page_config(page_title="Bambara Dubber", page_icon="🎙️", layout="centered")
st.title("🎙️ Bamanankan Dubber Pro")
st.markdown("**a ka fisa - Video to Bambara**")

@st.cache_resource
def load_whisper():
    import whisper
    return whisper.load_model("tiny")

@st.cache_resource
def load_translator():
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    name = "facebook/nllb-200-distilled-600M"
    tok = AutoTokenizer.from_pretrained(name)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(name)
    return tok, mdl

uploaded = st.file_uploader("ارفع فيديو", type=["mp4","mov","mkv","avi"])

if uploaded:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded.read())
    st.video(tfile.name)

    if st.button("🚀 ابدأ الدبلجة للبامبارا"):
        audio_path = tfile.name.replace(".mp4",".wav")
        subprocess.run(["ffmpeg","-y","-i",tfile.name,"-vn","-ac","1","-ar","16000",audio_path], check=True)
        st.success("1/3 الصوت ✅")

        with st.spinner("2/3 استماع..."):
            model = load_whisper()
            result = model.transcribe(audio_path, language="fr")
            text = result["text"]
            st.text_area("الأصلي (FR)", text, height=100)

        with st.spinner("3/3 ترجمة بامبارا..."):
            tokenizer, trans_model = load_translator()
            tokenizer.src_lang = "fra_Latn"
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=400)
            translated = trans_model.generate(**inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids("bam_Latn"), max_length=400)
            bam = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
            st.success("انتهى! 🎉")
            st.text_area("Bamanankan", bam, height=180)
            st.balloons()
else:
    st.info("👆 ارفع فيديو قصير (10 ثواني) للبدء")
