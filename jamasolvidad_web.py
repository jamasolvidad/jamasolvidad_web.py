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
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <div style="text-align: center;">
                <img src="data:image/jpeg;base64,{logo_base64}" alt="Jamasolvidad" style="max-height: 100px; margin-bottom: 20px;"/>
            </div>
            <h2 style="color: #1a1a1a;">🌟 Gracias por tu solicitud - <span style="color: #5e60ce;">Jamasolvidad</span></h2>
            <p>Hola,</p>
            <p>Gracias por confiar en <strong>Jamasolvidad</strong> para rendir homenaje a tu ser querido. Estamos comprometidos a ayudarte a mantener viva su memoria de una forma emotiva y respetuosa.</p>
            
            <h3 style="color: #5e60ce;">🛠️ ¿Qué sigue?</h3>
            <ul>
                <li>✔️ <strong>Envíanos</strong> fotos, videos y textos para el homenaje.</li>
                <li>✔️ <strong>Diseñamos</strong> un espacio digital único y seguro.</li>
                <li>✔️ <strong>Instalamos</strong> el código QR en la lápida o recuerdo.</li>
            </ul>

            <p style="background-color: #f1f1f1; padding: 10px; border-radius: 6px;">
                <strong>📌 Importante:</strong><br>
                • El código QR es duradero y resistente al clima.<br>
                • Recibirás un enlace privado para gestionar el contenido.
            </p>

            <p>📲 Puedes enviar el material por <strong>WhatsApp</strong> al <a href="https://wa.me/573053629015">305 362 9015</a><br>
            o al correo: <strong>jamasolvidad@gmail.com</strong></p>

            <h3 style="color: #5e60ce;">📋 Información del formulario:</h3>
            <ul>
    """
    for campo, valor in datos.items():
        cuerpo += f"<li><strong>{campo}:</strong> {valor}</li>"

    cuerpo += """
            </ul>
            <p style="text-align:center; margin-top:30px;">💜 Gracias por permitirnos hacer parte de este homenaje.</p>
            <p style="text-align:center;">Equipo <strong>Jamasolvidad</strong></p>
        </div>
    </body>
    </html>
    """

    mensaje.add_alternative(cuerpo, subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMITENTE, CLAVE_APP)
        smtp.send_message(mensaje)

# Validar
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
            errores.append("El año de nacimiento debe estar entre hace 110 años y el actual.")
        if not (nacimiento <= fallecimiento <= anio_actual):
            errores.append("El año de fallecimiento debe ser mayor o igual al de nacimiento y no mayor al actual.")
    except ValueError:
        errores.append("Los años deben ser números válidos.")

    return errores

# Formulario genérico
def formulario(tipo):
    st.set_page_config(layout="centered")
    st.markdown(f"<h2 style='text-align:center;'>Formulario {tipo}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("← Volver al inicio"):
        st.session_state['pantalla'] = 'inicio'
        st.experimental_rerun()

    nombre = st.text_input("Nombre del fallecido")
    nacimiento = st.text_input("Año de nacimiento")
    fallecimiento = st.text_input("Año de fallecimiento")
    telefono = st.text_input("Teléfono")
    email = st.text_input("Email")

    if tipo == "Funeraria":
        opciones = ["Funeraria San Vicente", "Funeraria La Ermita", "Funeraria In Memoriam", "Otra"]
    else:
        opciones = ["Cementerio Metropolitano del Sur", "Cementerio Central", "Jardines de la Aurora", "Otra"]

    lugar = st.selectbox(f"{tipo} asociado", opciones)
    if lugar == "Otra":
        lugar = st.text_input(f"Escriba el nombre del {tipo.lower()}:")

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
            st.success("Gracias por tu solicitud. Pronto nos pondremos en contacto.")
            st.session_state['pantalla'] = 'inicio'
            st.experimental_rerun()

# Interfaz principal
if 'pantalla' not in st.session_state:
    st.session_state['pantalla'] = 'inicio'

if st.session_state['pantalla'] == 'inicio':
    st.set_page_config(layout="centered")
    st.markdown("<h1 style='text-align: center;'>Jamasolvidad</h1>", unsafe_allow_html=True)
    st.image("foto jamasolvidad.jpg", use_container_width=True)

    # Mostrar miniatura del video con overlay de botón play
    with open("video_thumbnail.jpg", "rb") as f:
        img_base64 = b64encode(f.read()).decode()

    st.markdown(f"""
    <div style="position: relative; display: inline-block; cursor: pointer;" onclick="window.open('https://drive.google.com/file/d/1HWSGTcwaczETPg3luz7rGzcDwtYAJmZw/view?usp=drive_link', '_blank')">
        <img src="data:image/jpeg;base64,{img_base64}" style="width: 100%; border-radius: 10px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/72/YouTube_play_button_icon_%282013-2017%29.svg" style="position: absolute; top: 50%; left: 50%; width: 60px; transform: translate(-50%, -50%); opacity: 0.8;">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Formulario Funeraria"):
        st.session_state['pantalla'] = "Funeraria"
        st.experimental_rerun()
    if st.button("Formulario Cementerio"):
        st.session_state['pantalla'] = "Cementerio"
        st.experimental_rerun()

    if st.button("Salir"):
        st.session_state['pantalla'] = 'salir'
        st.experimental_rerun()

elif st.session_state['pantalla'] in ["Funeraria", "Cementerio"]:
    formulario(st.session_state['pantalla'])

elif st.session_state['pantalla'] == 'salir':
    st.set_page_config(layout="centered")
    st.markdown("<h2 style='text-align:center;'>Gracias por visitarnos.</h2>", unsafe_allow_html=True)
    st.stop()
