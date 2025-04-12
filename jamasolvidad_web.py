import streamlit as st
import openpyxl
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import re
from PIL import Image
from base64 import b64encode

# Configuración de la aplicación
st.set_page_config(layout="centered")

# Variables de correo
EMAIL_REMITENTE = "jamasolvidad@gmail.com"
CLAVE_APP = "upvucofjunwdstid"

# Función para guardar datos en Excel
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

# Función para enviar correo
def enviar_correo(destinatario, datos):
    mensaje = EmailMessage()
    mensaje["Subject"] = "Gracias por tu solicitud - Jamasolvidad"
    mensaje["From"] = EMAIL_REMITENTE
    mensaje["To"] = destinatario

    cuerpo = f"""
    Hola,

    Gracias por confiar en Jamasolvidad para rendir homenaje a tu ser querido. Estamos comprometidos a ayudarte a mantener viva su memoria de una forma emotiva y respetuosa.

    Información del formulario:
    """
    for campo, valor in datos.items():
        cuerpo += f"\n{campo}: {valor}"

    cuerpo += "\n\nGracias por permitirnos hacer parte de este homenaje.\nEquipo Jamasolvidad"

    mensaje.set_content(cuerpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMITENTE, CLAVE_APP)
        smtp.send_message(mensaje)

# Función para validar campos
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

# Mostrar logo
if os.path.exists("logo_jamasolvidad.jpg"):
    with open("logo_jamasolvidad.jpg", "rb") as f:
        logo_base64 = b64encode(f.read()).decode()
    st.markdown(f"""
        <div style="text-align:center;">
            <img src="data:image/jpeg;base64,{logo_base64}" style="height: 100px;">
        </div>
    """, unsafe_allow_html=True)

st.title("Bienvenido a Jamasolvidad")

# Botones de navegación
opcion = st.radio("Seleccione una opción:", ["Inicio", "Formulario", "Salir"])

if opcion == "Inicio":
    st.write("Gracias por visitar Jamasolvidad. Por favor, seleccione una opción del menú.")

elif opcion == "Formulario":
    st.header("Formulario de Solicitud")

    nombre = st.text_input("Nombre del fallecido")
    nacimiento = st.text_input("Año de nacimiento")
    fallecimiento = st.text_input("Año de fallecimiento")
    telefono = st.text_input("Teléfono")
    email = st.text_input("Email")

    if st.button("Enviar solicitud"):
        campos = {
            "Nombre": nombre,
            "Año de nacimiento": nacimiento,
            "Año de fallecimiento": fallecimiento,
            "Teléfono": telefono,
            "Email": email
        }
        errores = validar(campos)
        if errores:
            st.error("\n".join(errores))
        else:
            guardar_en_excel("datos_jamasolvidad.xlsx", campos)
            enviar_correo(email, campos)
            st.success("✅ ¡Tu solicitud fue enviada exitosamente! Gracias por confiar en nosotros. Pronto nos pondremos en contacto contigo.")

elif opcion == "Salir":
    st.write("Gracias por utilizar Jamasolvidad. ¡Hasta pronto!")
