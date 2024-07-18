import streamlit as st
from googletrans import Translator
import fitz  # PyMuPDF
from io import BytesIO

# Function to translate text using Google Translate
def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text, translation.src

# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to convert text to a downloadable file
def text_to_downloadable_file(text, filename="translated_text.txt"):
    return BytesIO(text.encode())

# Language options
languages = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian',
    'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian',
    'bg': 'Bulgarian', 'ca': 'Catalan', 'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish',
    'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish',
    'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek',
    'gu': 'Gujarati', 'ht': 'Haitian Creole', 'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'hi': 'Hindi',
    'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish',
    'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer',
    'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
    'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam',
    'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali',
    'no': 'Norwegian', 'or': 'Odia', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese',
    'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian',
    'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian',
    'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik',
    'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek',
    'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
}

# Set page layout to wide
st.set_page_config(layout="wide")

# Streamlit App
st.title("PDF/Text Translator")

# Create columns for layout
col1, col2 = st.columns([1, 3])

# Upload PDF file
with col1:
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Input text
with col2:
    input_text = st.text_area("Or enter text to translate")

# Source and destination languages
src_lang = st.selectbox("Select source language", options=languages.keys(), format_func=lambda x: languages[x])
dest_lang = st.selectbox("Select destination language", options=languages.keys(), format_func=lambda x: languages[x])

if st.button("Detect Language"):
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        _, detected_lang = translate_text(text, 'auto', dest_lang)
        st.write(f"Detected Language: {languages[detected_lang]}")
    elif input_text:
        _, detected_lang = translate_text(input_text, 'auto', dest_lang)
        st.write(f"Detected Language: {languages[detected_lang]}")
    else:
        st.write("Please upload a PDF file or enter text to detect the language.")

if st.button("Translate"):
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        translated_text, detected_lang = translate_text(text, src_lang, dest_lang)
        st.write(f"Detected Language: {languages[detected_lang]}")
        st.write(translated_text)
        download_file = text_to_downloadable_file(translated_text)
        st.download_button("Download Translated Text", data=download_file, file_name="translated_text.txt")
    elif input_text:
        translated_text, detected_lang = translate_text(input_text, src_lang, dest_lang)
        st.write(f"Detected Language: {languages[detected_lang]}")
        st.write(translated_text)
        download_file = text_to_downloadable_file(translated_text)
        st.download_button("Download Translated Text", data=download_file, file_name="translated_text.txt")
    else:
        st.write("Please upload a PDF file or enter text to translate.")
