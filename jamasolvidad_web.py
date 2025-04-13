import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration
CLAVE_APP = "upvucofjunwdstid"
EMAIL_FROM = "jamasolvidad@gmail.com"
EMAIL_TO = "jamasolvidad@gmail.com"

# Sample data for dropdowns
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

def funeraria_form():
    st.header("Formulario Funeraria")
    
    with st.form("funeraria_form"):
        cedula = st.text_input("Cédula", max_chars=20)
        nombre = st.text_input("Nombre y Apellido", max_chars=100)
        telefono = st.text_input("Teléfono", max_chars=20)
        email = st.text_input("Email", max_chars=100)
        cliente = st.text_input("Cliente (Fallecido)", max_chars=100)
        
        current_year = datetime.now().year
        min_year = current_year - 110
        ano_nacimiento = st.number_input("Año de nacimiento", min_value=min_year, max_value=current_year, value=current_year-80)
        ano_fallecimiento = st.number_input("Año de fallecimiento", min_value=ano_nacimiento, max_value=current_year, value=current_year)
        
        funeraria = st.selectbox("Funeraria", funerarias_cali)
        vendedor = st.text_input("Vendedor", max_chars=100)
        pago = st.selectbox("Forma de pago", formas_pago)
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            # Validate required fields
            if not all([cedula, nombre, telefono, email, cliente, funeraria, vendedor, pago]):
                st.error("Por favor complete todos los campos obligatorios")
                return
                
            # Prepare email content
            subject = f"Nuevo formulario Funeraria - {nombre}"
            body = f"""Gracias por elegir nuestro servicio para honrar la memoria de tu ser querido.  
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

Datos del formulario:
Cédula: {cedula}
Nombre y Apellido: {nombre}
Teléfono: {telefono}
Email: {email}
Cliente (Fallecido): {cliente}
Año de nacimiento: {ano_nacimiento}
Año de fallecimiento: {ano_fallecimiento}
Funeraria: {funeraria}
Vendedor: {vendedor}
Forma de pago: {pago}
"""
            
            # Send email
            if send_email(subject, body, [email, EMAIL_TO]):
                st.success("Formulario enviado correctamente. Recibirás un correo de confirmación.")
            else:
                st.error("Error al enviar el formulario. Por favor intente nuevamente.")

def cementerio_form():
    st.header("Formulario Cementerio")
    
    with st.form("cementerio_form"):
        cedula = st.text_input("Cédula", max_chars=20)
        nombre = st.text_input("Nombre y Apellido", max_chars=100)
        telefono = st.text_input("Teléfono", max_chars=20)
        email = st.text_input("Email", max_chars=100)
        cliente = st.text_input("Cliente (Fallecido)", max_chars=100)
        
        current_year = datetime.now().year
        min_year = current_year - 110
        ano_nacimiento = st.number_input("Año de nacimiento", min_value=min_year, max_value=current_year, value=current_year-80)
        ano_fallecimiento = st.number_input("Año de fallecimiento", min_value=ano_nacimiento, max_value=current_year, value=current_year)
        
        cementerio = st.selectbox("Cementerio", cementerios_cali)
        vendedor = st.text_input("Vendedor", max_chars=100)
        pago = st.selectbox("Forma de pago", formas_pago)
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            # Validate required fields
            if not all([cedula, nombre, telefono, email, cliente, cementerio, vendedor, pago]):
                st.error("Por favor complete todos los campos obligatorios")
                return
                
            # Prepare email content
            subject = f"Nuevo formulario Cementerio - {nombre}"
            body = f"""Gracias por elegir nuestro servicio para honrar la memoria de tu ser querido.  
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

Datos del formulario:
Cédula: {cedula}
Nombre y Apellido: {nombre}
Teléfono: {telefono}
Email: {email}
Cliente (Fallecido): {cliente}
Año de nacimiento: {ano_nacimiento}
Año de fallecimiento: {ano_fallecimiento}
Cementerio: {cementerio}
Vendedor: {vendedor}
Forma de pago: {pago}
"""
            
            # Send email
            if send_email(subject, body, [email, EMAIL_TO]):
                st.success("Formulario enviado correctamente. Recibirás un correo de confirmación.")
            else:
                st.error("Error al enviar el formulario. Por favor intente nuevamente.")

def main():
    # Page configuration
    st.set_page_config(page_title="Jamasolvida", page_icon=":rose:", layout="centered")
    
    # Header with logo and thumbnail
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo_jamasolvidad.jpg", width=150)
    with col2:
        st.image("video_thumbnail.jpg", width=300)
    
    st.title("Bienvenido a Jamasolvida")
    st.write("Servicios conmemorativos para honrar la memoria de tus seres queridos")
    
    # Navigation buttons
    option = st.radio("Seleccione una opción:", 
                      ["Inicio", "Formulario Funeraria", "Formulario Cementerio", "Salir"],
                      horizontal=True)
    
    if option == "Inicio":
        st.write("Por favor seleccione uno de los formularios para continuar.")
    elif option == "Formulario Funeraria":
        funeraria_form()
    elif option == "Formulario Cementerio":
        cementerio_form()
    elif option == "Salir":
        st.stop()

if __name__ == "__main__":
    main()