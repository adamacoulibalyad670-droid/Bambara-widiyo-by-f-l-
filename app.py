import streamlit as st
import tempfile, subprocess

st.set_page_config(page_title="Bambara Dubber", page_icon="🎙️", layout="centered")
st.title("🎙️ Bamanankan Dubber Pro")
st.markdown("**a ka fisa - Video to Bambara**")

def load_whisper():
    import whisper
    return whisper.load_model("tiny")

uploaded = st.file_uploader("📤 ارفع فيديو", type=["mp4","mov","mkv","avi"])

if uploaded:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded.read())
    st.video(tfile.name)

    if st.button("🚀 ابدأ الدبلجة للبامبارا"):
        audio_path = tfile.name.replace(".mp4",".wav")
        subprocess.run(["ffmpeg","-y","-i",tfile.name,"-vn","-ac","1","-ar","16000",audio_path], check=True)
        st.success("✅ 1/3 تم استخراج الصوت")

        with st.spinner("2/3 جاري الاستماع..."):
            model = load_whisper()
            result = model.transcribe(audio_path, language="fr")
            text = result["text"]
            st.text_area("النص الأصلي", text, height=100)

        with st.spinner("3/3 ترجمة للبامبارا..."):
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            tok = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
            trans_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
            inputs = tok(text, return_tensors="pt", truncation=True, max_length=400)
            translated_tokens = trans_model.generate(**inputs, forced_bos_token_id=tok.lang_code_to_id["bam_Latn"], max_length=400)
            bambara = tok.batch_decode(translated_tokens, skip_special_tokens=True)[0]
            st.success("✅ اكتملت الترجمة للبامبارا!")
            st.text_area("Bamanankan", bambara, height=180)
            st.balloons()
else:
    st.info("👆 ارفع فيديو للبدء")
