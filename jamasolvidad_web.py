import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re
from PIL import Image
import io
import base64

# Configuración
CLAVE_APP = "upvucofjunwdstid"
EMAIL_FROM = "jamasolvidad@gmail.com"
EMAIL_TO = "jamasolvidad@gmail.com"
VIDEO_URL = "https://drive.google.com/file/d/1HWSGTcwaczETPg3luz7rGzcDwtYAJmZw/view?usp=drive_link"

# Datos para dropdowns
funerarias_cali = [
    "Funeraria Los Olivos",
    "Funeraria La Piedad",
    "Funeraria San Fernando",
    "Funeraria La Merced",
    "Funeraria San Vicente",
    "Funeraria La Esperanza",
    "Funeraria Jardines del Recuerdo",
    "Funeraria San Judas Tadeo",
    "Funeraria La Sagrada Familia",
    "Funeraria La Ascensión",
    "Otro"
]

cementerios_cali = [
    "Cementerio Jardines del Recuerdo",
    "Cementerio Los Cedros",
    "Cementerio San Fernando",
    "Cementerio Metropolitano del Sur",
    "Cementerio Parque del Recuerdo",
    "Cementerio Municipal de Cali",
    "Cementerio La Piedad",
    "Cementerio La Merced",
    "Cementerio San Antonio",
    "Cementerio San Vicente",
    "Otro"
]

formas_pago = [
    "Bancolombia 74900017557",
    "Nequi 3184666194",
    "Daviplata 3184666194",
    "Efectivo"
]

def send_email(subject, body, to_emails):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, CLAVE_APP)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, to_emails, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error al enviar el correo: {e}")
        return False

def create_email_content(form_data, form_type):
    email_content = f"""Gracias por elegir nuestro servicio para honrar la memoria de tu ser querido.  
Estamos comprometidos a ayudarte a preservar su legado de una manera única y emotiva. A continuación, te explicamos los siguientes pasos:
1. Recopilación de Contenido: Envíanos las fotos, videos y textos que deseas incluir en el código QR.
2. Diseño y Personalización: Nos encargaremos de crear un espacio digital seguro y accesible.
3. Instalación del Código QR: Una vez listo, te contactaremos para coordinar la instalación en la lápida.

Datos Importantes:
• El código QR es duradero y resistente a las condiciones climáticas.
• Te proporcionaremos un enlace de acceso privado para que gestiones los contenidos.

Si tienes alguna duda o necesitas asistencia, no dudes en contactarnos. Estamos aquí para ayudarte en cada paso.
Gracias por confiar en nosotros para mantener viva su memoria. 

Enviar material para el video al WhatsApp 3053629015 o al correo jamasolvidad@gmail.com

Datos del formulario {form_type}:
"""
    for key, value in form_data.items():
        email_content += f"{key}: {value}\n"
    
    return email_content

def validate_phone(phone):
    return re.match(r'^\d{10}$', phone) is not None

def validate_cedula(cedula):
    return cedula.isdigit()

def validate_name(name):
    return all(c.isalpha() or c.isspace() for c in name)

def create_thumbnail_with_play_button():
    """Crea una miniatura con botón play superpuesto"""
    try:
        # Cargar la miniatura original
        img = Image.open("video_thumbnail.jpg")
        img = img.resize((300, 170))  # Ajustar tamaño
        
        # Convertir a base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # HTML con el botón play
        thumbnail_html = f"""
        <div style="position:relative;display:inline-block;cursor:pointer" 
             onclick="window.open('{VIDEO_URL}','_blank')">
            <img src="data:image/jpeg;base64,{img_str}" 
                 style="border-radius:8px;width:300px;border:2px solid #ff0000">
            <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" 
                     viewBox="0 0 24 24" fill="#ff0000" style="filter:drop-shadow(2px 2px 4px #000000);opacity:0.8">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
                </svg>
            </div>
        </div>
        """
        return thumbnail_html
    except Exception as e:
        st.error(f"Error al cargar la miniatura: {e}")
        return ""

def funeraria_form():
    st.header("Formulario Funeraria")
    
    with st.form("funeraria_form"):
        cedula = st.text_input("Cédula (solo números)", max_chars=20, key="funeraria_cedula")
        nombre = st.text_input("Nombre y Apellido", max_chars=100, key="funeraria_nombre")
        telefono = st.text_input("Teléfono (10 dígitos)", max_chars=10, key="funeraria_telefono")
        email = st.text_input("Email", max_chars=100, key="funeraria_email")
        cliente = st.text_input("Cliente (Fallecido)", max_chars=100, key="funeraria_cliente")
        
        current_year = datetime.now().year
        min_year = current_year - 110
        ano_nacimiento = st.number_input("Año de nacimiento", min_value=min_year, 
                                       max_value=current_year, value=current_year-80, 
                                       key="funeraria_nacimiento")
        ano_fallecimiento = st.number_input("Año de fallecimiento", min_value=ano_nacimiento, 
                                          max_value=current_year, value=current_year,
                                          key="funeraria_fallecimiento")
        
        funeraria = st.selectbox("Funeraria", funerarias_cali, key="funeraria_funeraria")
        vendedor = st.text_input("Vendedor", max_chars=100, key="funeraria_vendedor")
        pago = st.selectbox("Forma de pago", formas_pago, key="funeraria_pago")
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            errors = []
            if not validate_cedula(cedula):
                errors.append("❌ La cédula debe contener solo números")
            if not validate_name(nombre):
                errors.append("❌ El nombre debe contener solo letras y espacios")
            if not validate_phone(telefono):
                errors.append("❌ El teléfono debe tener 10 dígitos numéricos")
            if not all([cedula, nombre, telefono, email, cliente, funeraria, vendedor, pago]):
                errors.append("❌ Complete todos los campos obligatorios")
            
            if errors:
                for error in errors:
                    st.error(error)
                return
                
            form_data = {
                "Cédula": cedula,
                "Nombre y Apellido": nombre,
                "Teléfono": telefono,
                "Email": email,
                "Cliente (Fallecido)": cliente,
                "Año de nacimiento": ano_nacimiento,
                "Año de fallecimiento": ano_fallecimiento,
                "Funeraria": funeraria,
                "Vendedor": vendedor,
                "Forma de pago": pago
            }
            
            email_body = create_email_content(form_data, "Funeraria")
            
            if send_email(f"Formulario Funeraria - {nombre}", email_body, [email, EMAIL_TO]):
                st.success("✅ Formulario enviado correctamente")
                st.session_state.show_form = False
                st.experimental_rerun()
            else:
                st.error("❌ Error al enviar el formulario")

def cementerio_form():
    st.header("Formulario Cementerio")
    
    with st.form("cementerio_form"):
        cedula = st.text_input("Cédula (solo números)", max_chars=20, key="cementerio_cedula")
        nombre = st.text_input("Nombre y Apellido", max_chars=100, key="cementerio_nombre")
        telefono = st.text_input("Teléfono (10 dígitos)", max_chars=10, key="cementerio_telefono")
        email = st.text_input("Email", max_chars=100, key="cementerio_email")
        cliente = st.text_input("Cliente (Fallecido)", max_chars=100, key="cementerio_cliente")
        
        current_year = datetime.now().year
        min_year = current_year - 110
        ano_nacimiento = st.number_input("Año de nacimiento", min_value=min_year, 
                                       max_value=current_year, value=current_year-80,
                                       key="cementerio_nacimiento")
        ano_fallecimiento = st.number_input("Año de fallecimiento", min_value=ano_nacimiento, 
                                          max_value=current_year, value=current_year,
                                          key="cementerio_fallecimiento")
        
        cementerio = st.selectbox("Cementerio", cementerios_cali, key="cementerio_cementerio")
        vendedor = st.text_input("Vendedor", max_chars=100, key="cementerio_vendedor")
        pago = st.selectbox("Forma de pago", formas_pago, key="cementerio_pago")
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            errors = []
            if not validate_cedula(cedula):
                errors.append("❌ La cédula debe contener solo números")
            if not validate_name(nombre):
                errors.append("❌ El nombre debe contener solo letras y espacios")
            if not validate_phone(telefono):
                errors.append("❌ El teléfono debe tener 10 dígitos numéricos")
            if not all([cedula, nombre, telefono, email, cliente, cementerio, vendedor, pago]):
                errors.append("❌ Complete todos los campos obligatorios")
            
            if errors:
                for error in errors:
                    st.error(error)
                return
                
            form_data = {
                "Cédula": cedula,
                "Nombre y Apellido": nombre,
                "Teléfono": telefono,
                "Email": email,
                "Cliente (Fallecido)": cliente,
                "Año de nacimiento": ano_nacimiento,
                "Año de fallecimiento": ano_fallecimiento,
                "Cementerio": cementerio,
                "Vendedor": vendedor,
                "Forma de pago": pago
            }
            
            email_body = create_email_content(form_data, "Cementerio")
            
            if send_email(f"Formulario Cementerio - {nombre}", email_body, [email, EMAIL_TO]):
                st.success("✅ Formulario enviado correctamente")
                st.session_state.show_form = False
                st.experimental_rerun()
            else:
                st.error("❌ Error al enviar el formulario")

def main():
    st.set_page_config(page_title="Jamasolvida", page_icon=":rose:", layout="centered")
    
    # Inicializar estado
    if 'show_form' not in st.session_state:
        st.session_state.show_form = True
    
    # Header con logo y miniatura
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo_jamasolvidad.jpg", width=150)
    with col2:
        thumbnail_html = create_thumbnail_with_play_button()
        if thumbnail_html:
            st.markdown(thumbnail_html, unsafe_allow_html=True)
        else:
            st.image("video_thumbnail.jpg", width=300)
            st.markdown(f"[Ver video]({VIDEO_URL})")
    
    st.title("Bienvenido a Jamasolvidad@")
    st.write("Servicios conmemorativos para honrar la memoria de tus seres queridos")
    
    if st.session_state.show_form:
        option = st.radio("Seleccione una opción:", 
                         ["Inicio", "Formulario Funeraria", "Formulario Cementerio", "Salir"],
                         horizontal=True, key="nav_options")
        
        if option == "Inicio":
            st.write("Por favor seleccione uno de los formularios para continuar.")
        elif option == "Formulario Funeraria":
            funeraria_form()
        elif option == "Formulario Cementerio":
            cementerio_form()
        elif option == "Salir":
            st.stop()
    else:
        st.success("¡Formulario enviado con éxito! ¿Qué deseas hacer ahora?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Volver al inicio", key="volver_inicio"):
                st.session_state.show_form = True
                st.experimental_rerun()
        with col2:
            if st.button("Salir", key="salir_app"):
                st.stop()

if __name__ == "__main__":
    main()