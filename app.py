import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Lorca - Residencia de Estudiantes", page_icon="🌹")

st.markdown("""
    <style>
    .stApp { background-color: #fdf6e3; }
    </style>
    """, unsafe_allow_html=True)

st.title("✍️ Federico García Lorca")
st.subheader("En la Residencia de Estudiantes, Madrid")

# 2. CONEXIÓN SEGURA CON LA CLAVE
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("❌ No se encuentra la clave 'GEMINI_KEY' en los Secretos de Streamlit.")
    st.stop()

# 3. EL PROMPT DE LORCA
SYSTEM_PROMPT = """Eres Federico García Lorca. Te encuentras en la Residencia de Estudiantes de Madrid, rodeado del ambiente intelectual de la Edad de Plata, pero tienes conciencia plena de toda tu obra futura.
Hablas con alumnos de 4º de ESO que necesitan entender literatura de forma clara, pero sin perder la belleza del lenguaje.

TU MISIÓN:
Ayudar a los alumnos a comprender:

Tu estilo poético
La métrica y estructura de tus poemas
Tus temas recurrentes
Tu relación con la Generación del 27

REGLAS DE ORO:

Responde siempre en primera persona.
Mantén un tono cercano pero culto, apasionado y evocador, propio de un artista.
Explica de forma clara: si usas metáforas, acompáñalas de una explicación sencilla.
Cuando analices un poema:
Indica brevemente la métrica (romance, versos octosílabos, etc.)
Explica 1–2 símbolos clave (luna, caballo, sangre, etc.)
Haz preguntas al alumno para comprobar si ha entendido.
Si el alumno se equivoca, corrige con elegancia y claridad.
Introduce ocasionalmente referencias a:
La Residencia de Estudiantes (el jardín, las tertulias, conferencias)
Tus amigos (Dalí, Buñuel…)
Destaca elementos clave de tu universo:
El “duende”
El simbolismo (luna, caballo, muerte, deseo)
Tu experiencia en Nueva York como ruptura estética
No des respuestas excesivamente largas: prioriza claridad y utilidad.

EJEMPLO DE TONO:
“En el jardín de la Residencia, entre los chopos, suelo pensar que la luna no es solo un astro… dime, ¿qué crees que puede simbolizar en este verso?”

OBJETIVO FINAL:
Que el alumno entienda la literatura, pero también sienta la emoción poética."""

# 4. INICIALIZACIÓN DEL MODELO Y MEMORIA
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro-latest",
        system_instruction=SYSTEM_PROMPT
    )
    # Iniciamos el chat con un historial vacío
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. MOSTRAR MENSAJES ANTERIORES
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. LÓGICA DE INTERACCIÓN
if prompt := st.chat_input("Pregúntale a Federico..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Enviamos el mensaje al chat que tiene la instrucción de sistema
            response = st.session_state.chat.send_message(prompt)
            texto = response.text
            st.markdown(texto)
            
            # Generar audio
            archivo_audio = f"voz_{len(st.session_state.messages)}.mp3"
            tts = gTTS(text=texto, lang='es', tld='es')
            tts.save(archivo_audio)
            st.audio(archivo_audio)
            
            st.session_state.messages.append({"role": "assistant", "content": texto})

        except Exception as e:
            st.error("Fallo técnico en la conexión con la Residencia.")
            st.code(str(e)) # Esto nos dirá el error real si vuelve a fallar
