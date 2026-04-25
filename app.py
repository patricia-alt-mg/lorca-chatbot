import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# Configuración de página
st.set_page_config(page_title="Lorca Chatbot", page_icon="🌹")

# Estilo papel antiguo
st.markdown("""
    <style>
    .stApp { background-color: #fdf6e3; }
    </style>
    """, unsafe_allow_html=True)

st.title("✍️ Federico García Lorca")
st.subheader("En la Residencia de Estudiantes, Madrid")

# 1. Configuración de API
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Falta la GEMINI_KEY en Secrets.")
    st.stop()

# 2. PROMPT CON COMILLAS TRIPLES (Para evitar el SyntaxError)
LORCA_PROMPT = """
Eres Federico García Lorca. Te encuentras en la Residencia de Estudiantes de Madrid, rodeado del ambiente intelectual de la Edad de Plata, pero tienes conciencia plena de toda tu obra futura.
Hablas con alumnos de 4º de ESO que necesitan entender literatura de forma clara, pero sin perder la belleza del lenguaje.
Responde siempre en primera persona, explica tus símbolos (luna, caballo, sangre) y mantén un tono poético y cercano.
"""

# 3. Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Interacción
if prompt := st.chat_input("Pregúntale a Federico..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Usamos el nombre del modelo que ya sabemos que la versión 0.8.3 acepta
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            full_query = f"{LORCA_PROMPT}\n\nAlumno dice: {prompt}"
            response = model.generate_content(full_query)
            texto = response.text
            
            st.markdown(texto)
            
            # Audio
            audio_file = f"voz_{len(st.session_state.messages)}.mp3"
            tts = gTTS(text=texto, lang='es', tld='es')
            tts.save(archivo_audio := audio_file)
            st.audio(archivo_audio)
            
            st.session_state.messages.append({"role": "assistant", "content": texto})

        except Exception as e:
            st.error("Error de conexión")
            st.code(str(e))
