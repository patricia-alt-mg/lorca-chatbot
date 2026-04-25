import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# Configuración visual de la página
st.set_page_config(page_title="Lorca - Residencia de Estudiantes", page_icon="🌹")

# Estilo para que se vea más literario (papel antiguo)
st.markdown("""
    <style>
    .stApp { background-color: #fdf6e3; }
    </style>
    """, unsafe_allow_html=True)

st.title("✍️ Federico García Lorca")
st.subheader("En la Residencia de Estudiantes, Madrid")

# 1. Configurar la API Key desde los secretos de Streamlit
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Falta la configuración de la API Key en los secretos.")
    st.stop()

# 2. Tu Prompt (La personalidad de Federico)
SYSTEM_PROMPT = """
Eres Federico García Lorca. Te encuentras en la Residencia de Estudiantes de Madrid, rodeado del ambiente intelectual de la Edad de Plata, pero tienes conciencia plena de toda tu obra futura.
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
Que el alumno entienda la literatura, pero también sienta la emoción poética.)
"""

# 3. Inicializar el modelo (Versión robusta para evitar el error NotFound)
# Busca este bloque en tu app.py y asegúrate de que esté así:
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # O el que te haya funcionado (1.0-pro)
        system_instruction=SYSTEM_PROMPT  # <--- ESTO ES LO QUE LE DA LA PERSONALIDAD
    )
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Mostrar historial de la conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Interacción con el alumno
if prompt := st.chat_input("Pregúntale a Federico..."):
    # Guardar y mostrar mensaje del alumno
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Enviar mensaje a la IA
            response = st.session_state.chat.send_message(prompt)
            texto_respuesta = response.text
            st.markdown(texto_respuesta)
            
            # Generar audio gratuito
            # Usamos un nombre de archivo dinámico para evitar bloqueos del sistema
            archivo_audio = f"voz_{len(st.session_state.messages)}.mp3"
            tts = gTTS(text=texto_respuesta, lang='es', tld='es')
            tts.save(archivo_audio)
            st.audio(archivo_audio)
            
            # Guardar respuesta en el historial
            st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
            
        except Exception as e:
            st.error("¡Ay! Mis duendes se han quedado mudos por un momento...")
            st.info("Intenta refrescar la página o comprueba tu conexión.")
