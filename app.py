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

# 1. Configuración de API - Simplificada al máximo
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Falta la GEMINI_KEY en los secretos de Streamlit.")
    st.stop()

# 2. Instrucciones de Lorca
LORCA_PROMPT = """Eres Federico García Lorca. Te encuentras en la Residencia de Estudiantes de Madrid. 
Hablas con alumnos de 4º de ESO. Mantén un tono poético y cercano. 
Explica símbolos como la luna, el caballo o la sangre. Responde siempre en primera persona."""

# 3. Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Interacción principal
if prompt := st.chat_input("Pregúntale a Federico..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # USAMOS EL NOMBRE TÉCNICO QUE NO DA 404
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            
            # Unimos el prompt y la pregunta en un solo envío
            respuesta = model.generate_content(f"{LORCA_PROMPT}\n\nPregunta: {prompt}")
            texto = respuesta.text
            
            st.markdown(texto)
            
            # Audio
            archivo_audio = f"voz_{len(st.session_state.messages)}.mp3"
            tts = gTTS(text=texto, lang='es', tld='es')
            tts.save(archivo_audio)
            st.audio(archivo_audio)
            
            st.session_state.messages.append({"role": "assistant", "content": texto})

        except Exception as e:
            st.error("Ha ocurrido un error en la conexión.")
            st.code(str(e))
