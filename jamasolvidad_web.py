import streamlit as st
import openpyxl
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import re
from PIL import Image
from base64 import b64encode

EMAIL_REMITENTE = "jamasolvidad@gmail.com"
CLAVE_APP = "upvucofjunwdstid"

# Guardar en Excel
def guardar_en_excel(nombre_archivo, datos):
    if not os.path.exists(nombre_archivo):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(list(datos.keys()))
    else:
        wb = openpyxl.load_workbook(nombre_archivo)
        ws = wb.active
    ws.append(list(datos.values()))
    wb.save(nombre_archivo)

# Enviar correo
def enviar_correo(destinatario, datos):
    mensaje = EmailMessage()
    mensaje["Subject"] = "Gracias por tu solicitud - Jamasolvidad"
    mensaje["From"] = EMAIL_REMITENTE
    mensaje["To"] = destinatario

    with open("logo_jamasolvidad.jpg", "rb") as f:
        logo_base64 = b64encode(f.read()).decode()

    cuerpo = f"""
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; background: #fff; padding: 20px;">
            <div style="text-align: center;">
                <img src="data:image/jpeg;base64,{logo_base64}" style="max-height: 100px;">
            </div>
            <h2>Gracias por tu solicitud - Jamasolvidad</h2>
            <p>Gracias por confiar en nosotros. Aquí están los datos que recibimos:</p>
            <ul>
    """
    for campo, valor in datos.items():
        cuerpo += f"<li><strong>{campo}:</strong> {valor}</li>"

    cuerpo += """
            </ul>
            <p>Nos pondremos en contacto contigo pronto.</p>
        </div>
    </body>
    </html>
    """
    mensaje.add_alternative(cuerpo, subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMITENTE, CLAVE_APP)
        smtp.send_message(mensaje)

# Validación
def validar(campos):
    errores = []
    anio_actual = datetime.now().year

    if not re.fullmatch(r"3\d{9}", campos["Teléfono"]):
        errores.append("El teléfono debe tener 10 dígitos y comenzar con 3.")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+", campos["Email"]):
        errores.append("El correo electrónico no es válido.")

    try:
        nacimiento = int(campos["Año de nacimiento"])
        fallecimiento = int(campos["Año de fallecimiento"])
        if not (anio_actual - 110 <= nacimiento <= anio_actual):
            errores.append("Año de nacimiento no válido.")
        if not (nacimiento <= fallecimiento <= anio_actual):
            errores.append("Año de fallecimiento no válido.")
    except ValueError:
        errores.append("Los años deben ser números.")

    return errores

# Estado inicial
if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = False
if "tipo_formulario" not in st.session_state:
    st.session_state.tipo_formulario = "Funeraria"

# Logo
with open("logo_jamasolvidad.jpg", "rb") as f:
    logo_base64 = b64encode(f.read()).decode()
st.markdown(f"""
    <div style="text-align:center;">
        <img src="data:image/jpeg;base64,{logo_base64}" style="height: 100px;">
    </div>
""", unsafe_allow_html=True)

# Miniatura de video
with open("video_thumbnail.jpg", "rb") as f:
    img_base64 = b64encode(f.read()).decode()
st.markdown(f"""
<div style="text-align:center;">
    <a href="https://drive.google.com/file/d/1HWSGTcwaczETPg3luz7rGzcDwtYAJmZw/view?usp=sharing" target="_blank" style="position: relative; display: inline-block;">
        <img src="data:image/jpeg;base64,{img_base64}" style="width: 100%; max-width: 400px; border-radius: 12px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/72/YouTube_play_button_icon_%282013-2017%29.svg" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 64px; opacity: 0.8;">
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Botón para mostrar formulario
formulario_elegido = st.radio("Selecciona el formulario:", ("Funeraria", "Cementerio"))
if st.button("Abrir formulario"):
    st.session_state.mostrar_formulario = True
    st.session_state.tipo_formulario = formulario_elegido

# Mostrar formulario
if st.session_state.mostrar_formulario:
    tipo = st.session_state.tipo_formulario
    st.markdown("---")
    st.header(f"Formulario {tipo}")

    nombre = st.text_input("Nombre del fallecido")
    nacimiento = st.text_input("Año de nacimiento")
    fallecimiento = st.text_input("Año de fallecimiento")
    telefono = st.text_input("Teléfono")
    email = st.text_input("Email")

    if tipo == "Funeraria":
        opciones = ["Funeraria San Vicente", "Funeraria La Ermita", "Funeraria In Memoriam", "Otra"]
    else:
        opciones = ["Cementerio Metropolitano del Sur", "Cementerio Central", "Jardines de la Aurora", "Otra"]

    lugar_opcion = st.selectbox(f"{tipo} asociado", opciones)
    if lugar_opcion == "Otra":
        lugar = st.text_input(f"Escriba el nombre del {tipo.lower()}:")
    else:
        lugar = lugar_opcion

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enviar solicitud"):
            campos = {
                "Nombre": nombre,
                "Año de nacimiento": nacimiento,
                "Año de fallecimiento": fallecimiento,
                "Teléfono": telefono,
                "Email": email,
                f"{tipo} asociado": lugar
            }
            errores = validar(campos)
            if errores:
                st.error("\n".join(errores))
            else:
                guardar_en_excel("datos_jamasolvidad.xlsx", campos)
                enviar_correo(email, campos)
                st.success("✅ ¡Tu solicitud fue enviada exitosamente!")
                st.session_state.mostrar_formulario = False
    with col2:
        if st.button("❌ Cancelar"):
            st.session_state.mostrar_formulario = False
