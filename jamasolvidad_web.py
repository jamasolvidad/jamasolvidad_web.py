import streamlit as st
import openpyxl
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import re
from PIL import Image, ImageDraw

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

    cuerpo = """Gracias por elegir nuestro servicio para honrar la memoria de tu ser querido.  
Estamos comprometidos a ayudarte a preservar su legado de una manera única y emotiva. A continuación, te explicamos los siguientes pasos:

1. Recopilación de Contenido: Envíanos las fotos, videos y textos que deseas incluir en el código QR.
2. Diseño y Personalización: Nos encargaremos de crear un espacio digital seguro y accesible.
3. Instalación del Código QR: Una vez listo, te contactaremos para coordinar la instalación en la lápida.

Datos Importantes:
• El código QR es duradero y resistente a las condiciones climáticas.
• Te proporcionaremos un enlace de acceso privado para que gestiones los contenidos.

Si tienes alguna duda o necesitas asistencia, no dudes en contactarnos. Estamos aquí para ayudarte en cada paso.

Enviar material para el video al WhatsApp 3053629015 o al correo jamasolvidad@gmail.com

Datos del formulario:
"""
    for campo, valor in datos.items():
        cuerpo += f"{campo}: {valor}\n"

    mensaje.set_content(cuerpo)

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
            errores.append("El año de nacimiento debe estar entre hace 110 años y el actual.")
        if not (nacimiento <= fallecimiento <= anio_actual):
            errores.append("El año de fallecimiento debe ser mayor o igual al de nacimiento y no mayor al actual.")
    except ValueError:
        errores.append("Los años deben ser números válidos.")

    return errores

# Formulario
def formulario(tipo):
    st.subheader(f"Formulario {tipo}")
    with st.form(f"{tipo}_formulario"):
        campos = {}
        campos["Cédula"] = st.text_input("Cédula")
        campos["Nombre y Apellido"] = st.text_input("Nombre y Apellido")
        campos["Teléfono"] = st.text_input("Teléfono")
        campos["Email"] = st.text_input("Email")
        campos["Cliente (Fallecido)"] = st.text_input("Cliente (Fallecido)")
        campos["Año de nacimiento"] = st.text_input("Año de nacimiento")
        campos["Año de fallecimiento"] = st.text_input("Año de fallecimiento")

        if tipo == "Funeraria":
            opciones = ["Los Olivos", "Capillas de La Fe", "Inmemorial", "Recordar", "Funerales La Esperanza", "Campos de Paz", "Plenitud Protección S.A.", "Casa de Funerales La Ermita", "Funerales García", "Otro"]
        else:
            opciones = ["Cementerio Central", "Cementerio Metropolitano del Norte", "Jardines del Recuerdo", "Cementerio San Joaquín", "Cementerio Hebreo de Cali", "Parque Cementerio Jardines de La Aurora", "Cementerio - Carabineros", "Otro"]

        seleccion = st.selectbox("Selecciona " + tipo, opciones)
        if seleccion == "Otro":
            campos[tipo] = st.text_input(f"Otro {tipo}")
        else:
            campos[tipo] = seleccion

        campos["Vendedor"] = st.text_input("Vendedor")
        campos["Forma de pago"] = st.selectbox("Forma de pago", ["Bancolombia 74900017557", "Nequi 3184666194", "Daviplata 3184666194", "Efectivo"])

        submitted = st.form_submit_button("Enviar formulario")
        if submitted:
            errores = validar(campos)
            if errores:
                st.error("\n".join(errores))
            else:
                guardar_en_excel("registros_web.xlsx", campos)
                enviar_correo(campos["Email"], campos)
                enviar_correo("jamasolvidad@gmail.com", campos)
                st.success("Formulario enviado. Revisa tu correo.")

# Interfaz
st.title("Jamasolvidad")
st.image("foto jamasolvidad.jpg", width=250)

# Imagen de video con play
img = Image.open("Gemini_Generated_Image_62yjfv62yjfv62yj (1).jpg").copy()
draw = ImageDraw.Draw(img)
x, y, r = img.width // 2, img.height // 2, 30
draw.polygon([(x - r, y - r), (x - r, y + r), (x + r, y)], fill="red")
if st.image(img, use_column_width=True):
    st.markdown("[Haz clic aquí para ver el video](https://drive.google.com/file/d/1HWSGTcwaczETPg3luz7rGzcDwtYAJmZw/view?usp=drive_link)")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("Formulario Funeraria"):
        st.session_state["formulario_tipo"] = "Funeraria"
with col2:
    if st.button("Formulario Cementerio"):
        st.session_state["formulario_tipo"] = "Cementerio"

# Mostrar formulario si está definido
if "formulario_tipo" in st.session_state:
    formulario(st.session_state["formulario_tipo"])

# Botón de salida
if st.button("Salir"):
    st.success("Gracias por visitarnos.")
    st.stop()
