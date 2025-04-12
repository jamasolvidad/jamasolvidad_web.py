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

    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #2c3e50;">Gracias por tu solicitud - Jamasolvidad</h2>
        <p>Gracias por elegir nuestro servicio para honrar la memoria de tu ser querido. Estamos comprometidos a ayudarte a preservar su legado de una manera única y emotiva.</p>
        <h3>Paso a paso:</h3>
        <ol>
            <li><strong>Recopilación de Contenido:</strong> Envíanos las fotos, videos y textos que deseas incluir en el código QR.</li>
            <li><strong>Diseño y Personalización:</strong> Nos encargaremos de crear un espacio digital seguro y accesible.</li>
            <li><strong>Instalación del Código QR:</strong> Una vez listo, te contactaremos para coordinar la instalación en la lápida.</li>
        </ol>
        <p><strong>Información importante:</strong><br>
        • El código QR es duradero y resistente a las condiciones climáticas.<br>
        • Te proporcionaremos un enlace de acceso privado para que gestiones los contenidos.</p>

        <p><strong>Enviar material para el video al WhatsApp:</strong> 3053629015<br>
        <strong>O al correo:</strong> jamasolvidad@gmail.com</p>

        <h3>Datos del formulario:</h3>
        <ul>
    """
    for campo, valor in datos.items():
        cuerpo += f"<li><strong>{campo}:</strong> {valor}</li>"

    cuerpo += """
        </ul>
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

    # Imagen con botón de reproducción dibujado
    img = Image.open("Gemini_Generated_Image_62yjfv62yjfv62yj (1).jpg").copy()
    draw = ImageDraw.Draw(img)
    x, y, r = img.width // 2, img.height // 2, 30
    draw.polygon([(x - r, y - r), (x - r, y + r), (x + r, y)], fill="red")

    st.image(img, use_container_width=True)
    st.markdown("""
    <script>
    const imgs = window.parent.document.querySelectorAll('img');
    imgs.forEach(img => {
        if(img.src.includes("Gemini_Generated")) {
            img.style.cursor = 'pointer';
            img.onclick = () => window.open("https://drive.google.com/file/d/1HWSGTcwaczETPg3luz7rGzcDwtYAJmZw/view?usp=drive_link", "_blank");
        }
    });
    </script>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Formulario Funeraria"):
            st.session_state['pantalla'] = "Funeraria"
            st.experimental_rerun()
    with col2:
        if st.button("Formulario Cementerio"):
            st.session_state['pantalla'] = "Cementerio"
            st.experimental_rerun()

    if st.button("Salir"):
        st.write("Gracias por visitarnos.")
        st.stop()

elif st.session_state['pantalla'] in ["Funeraria", "Cementerio"]:
    formulario(st.session_state['pantalla'])
