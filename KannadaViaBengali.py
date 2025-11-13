import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process as aksharamukha_process
from gtts import gTTS
from io import BytesIO
import pandas as pd

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="Bengali → Kannada Learning",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ HIDE STREAMLIT UI ------------------ #
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------ AUDIO GENERATOR ------------------ #
def make_audio(text, lang="kn"):
    fp = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# ------------------ PAGE TITLE ------------------ #
st.title("📝 Learn Kannada using Bengali Script")
st.subheader("বাংলা লিপি ব্যবহার করে কান্নড় শিখুন")

text = st.text_area("Enter Bengali text here:", height=120)

if st.button("Translate"):
    if text.strip():
        try:
            # ---------------- FULL SENTENCE PROCESSING ---------------- #

            # Bengali → Kannada sentence translation
            kannada = GoogleTranslator(source="bn", target="kn").translate(text)

            # Kannada → Bengali script (transliteration)
            kannada_in_bengali = aksharamukha_process("Kannada", "Bengali", kannada)

            # Kannada → English phonetics
            kannada_english = transliterate(kannada, sanscript.KANNADA, sanscript.ITRANS)

            # Kannada audio (sentence)
            audio_sentence = make_audio(kannada)

            # ---------------- OUTPUT ---------------- #
            st.markdown("## 🔹 Translation Results")

            st.markdown(f"**Bengali Input:**  \n:blue[{text}]")
            st.markdown(f"**Kannada Translation:**  \n:green[{kannada}]")
            st.markdown(f"**Kannada in Bengali Script:**  \n:orange[{kannada_in_bengali}]")
            st.markdown(f"**English Phonetics:**  \n`{kannada_english}`")

            st.markdown("### 🔊 Kannada Audio (Sentence)")
            st.audio(audio_sentence, format="audio/mp3")
            st.download_button("Download Sentence Audio", audio_sentence, "sentence.mp3")

            # ---------------- WORD-BY-WORD FLASHCARDS ---------------- #

            st.markdown("---")
            st.markdown("## 🃏 Flashcards (Word-by-Word)")

            bengali_words = text.split()
            kan_words = kannada.split()

            # Handle mismatch carefully
            limit = min(len(bengali_words), len(kan_words))

            for i in range(limit):
                bw = bengali_words[i]
                kw = kan_words[i]

                # Kannada → Bengali script (word)
                kw_bn = aksharamukha_process("Kannada", "Bengali", kw)

                # Phonetic (word)
                kw_ph = transliterate(kw, sanscript.KANNADA, sanscript.ITRANS)

                # Audio (word)
                kw_audio = make_audio(kw)

                with st.expander(f"Word {i+1}: {bw}", expanded=False):
                    st.write("**Bengali word:**", bw)
                    st.write("**Kannada word:**", kw)
                    st.write("**Kannada in Bengali script:**", kw_bn)
                    st.write("**Phonetics:**", kw_ph)

                    st.audio(kw_audio, format="audio/mp3")
                    st.download_button(
                        f"Download Audio (Word {i+1})",
                        kw_audio,
                        f"word_{i+1}.mp3"
                    )

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please enter Bengali text.")
