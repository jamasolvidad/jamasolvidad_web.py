import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re

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

def send_email(subject, body, to_emails, is_html=False):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
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

def create_email_body(form_data, form_type):
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
                .header {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }}
                .steps {{ margin: 20px 0; }}
                .step {{ margin-bottom: 15px; padding-left: 15px; border-left: 3px solid #3498db; }}
                .important {{ font-weight: bold; color: #e74c3c; }}
                .details {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 25px 0; border: 1px solid #ddd; }}
                table {{ width: 100%; border-collapse: collapse; }}
                td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
                .footer {{ margin-top: 30px; font-size: 0.9em; color: #7f8c8d; text-align: center; }}
                h2 {{ color: #2c3e50; }}
                h3 {{ color: #3498db; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Gracias por elegir nuestro servicio</h2>
                <p>Para honrar la memoria de tu ser querido</p>
            </div>
            
            <p style="font-size: 16px;">Estamos comprometidos a ayudarte a preservar su legado de una manera única y emotiva.</p>
            
            <div class="steps">
                <h3>📋 Próximos pasos:</h3>
                <div class="step">
                    <strong>1. Recopilación de Contenido:</strong><br>
                    Envíanos las fotos, videos y textos que deseas incluir en el código QR.
                </div>
                <div class="step">
                    <strong>2. Diseño y Personalización:</strong><br>
                    Nos encargaremos de crear un espacio digital seguro y accesible.
                </div>
                <div class="step">
                    <strong>3. Instalación del Código QR:</strong><br>
                    Una vez listo, te contactaremos para coordinar la instalación en la lápida.
                </div>
            </div>
            
            <div>
                <h3>🔍 Datos Importantes:</h3>
                <ul style="padding-left: 20px;">
                    <li>El código QR es <span class="important">duradero y resistente</span> a las condiciones climáticas.</li>
                    <li>Te proporcionaremos un <span class="important">enlace de acceso privado</span> para gestionar los contenidos.</li>
                </ul>
            </div>
            
            <div class="details">
                <h3>📝 Datos del formulario ({'Funeraria' if form_type == 'Funeraria' else 'Cementerio'}):</h3>
                <table>
    """
    
    for key, value in form_data.items():
        html_content += f"""
                    <tr>
                        <td style="width: 40%;"><strong>{key}:</strong></td>
                        <td>{value}</td>
                    </tr>
        """
    
    html_content += """
                </table>
            </div>
            
            <div class="footer">
                <p>Si tienes alguna duda o necesitas asistencia, no dudes en contactarnos.</p>
                <p>Estamos aquí para ayudarte en cada paso.</p>
                <p style="margin-top: 15px;">Gracias por confiar en nosotros para mantener viva su memoria.</p>
                
                <div style="margin-top: 25px; padding: 15px; background-color: #f0f8ff; border-radius: 5px;">
                    <h4 style="margin-top: 0; color: #2980b9;">📬 Enviar material:</h4>
                    <p><strong>WhatsApp:</strong> 3053629015</p>
                    <p><strong>Correo electrónico:</strong> jamasolvidad@gmail.com</p>
                </div>
            </div>
        </body>
    </html>
    """
    return html_content

def validate_phone(phone):
    """Valida que el teléfono tenga exactamente 10 dígitos numéricos"""
    return re.match(r'^\d{10}$', phone) is not None

def validate_cedula(cedula):
    """Valida que la cédula contenga solo números"""
    return cedula.isdigit()

def validate_name(name):
    """Valida que el nombre contenga solo letras y espacios"""
    return all(c.isalpha() or c.isspace() for c in name)

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
        ano_nacimiento = st.number_input("Año de nacimiento", min_value=min_year, max_value=current_year, value=current_year-80, key="funeraria_nacimiento")
        ano_fallecimiento = st.number_input("Año de fallecimiento", min_value=ano_nacimiento, max_value=current_year, value=current_year, key="funeraria_fallecimiento")
        
        funeraria = st.selectbox("Funeraria", funerarias_cali, key="funeraria_funeraria")
        vendedor = st.text_input("Vendedor", max_chars=100, key="funeraria_vendedor")
        pago = st.selectbox("Forma de pago", formas_pago, key="funeraria_pago")
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            # Validaciones
            errors = []
            
            if not validate_cedula(cedula):
                errors.append("❌ La cédula debe contener solo números")
                
            if not validate_name(nombre):
                errors.append("❌ El nombre debe contener solo letras y espacios")
                
            if not validate_phone(telefono):
                errors.append("❌ El teléfono debe tener exactamente 10 dígitos numéricos")
                
            if not all([cedula, nombre, telefono, email, cliente, funeraria, vendedor, pago]):
                errors.append("❌ Por favor complete todos los campos obligatorios")
            
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
            
            html_body = create_email_body(form_data, "Funeraria")
            
            if send_email(f"Nuevo formulario Funeraria - {nombre}", html_body, [email, EMAIL_TO], is_html=True):
                st.session_state.show_form = False
                st.session_state.form_submitted = True
                st.session_state.form_type = "Funeraria"
                st.experimental_rerun()
            else:
                st.error("❌ Error al enviar el formulario. Por favor intente nuevamente.")

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
        ano_nacimiento = st.number_input("Año de nacimiento", min_value=min_year, max_value=current_year, value=current_year-80, key="cementerio_nacimiento")
        ano_fallecimiento = st.number_input("Año de fallecimiento", min_value=ano_nacimiento, max_value=current_year, value=current_year, key="cementerio_fallecimiento")
        
        cementerio = st.selectbox("Cementerio", cementerios_cali, key="cementerio_cementerio")
        vendedor = st.text_input("Vendedor", max_chars=100, key="cementerio_vendedor")
        pago = st.selectbox("Forma de pago", formas_pago, key="cementerio_pago")
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            # Validaciones
            errors = []
            
            if not validate_cedula(cedula):
                errors.append("❌ La cédula debe contener solo números")
                
            if not validate_name(nombre):
                errors.append("❌ El nombre debe contener solo letras y espacios")
                
            if not validate_phone(telefono):
                errors.append("❌ El teléfono debe tener exactamente 10 dígitos numéricos")
                
            if not all([cedula, nombre, telefono, email, cliente, cementerio, vendedor, pago]):
                errors.append("❌ Por favor complete todos los campos obligatorios")
            
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
            
            html_body = create_email_body(form_data, "Cementerio")
            
            if send_email(f"Nuevo formulario Cementerio - {nombre}", html_body, [email, EMAIL_TO], is_html=True):
                st.session_state.show_form = False
                st.session_state.form_submitted = True
                st.session_state.form_type = "Cementerio"
                st.experimental_rerun()
            else:
                st.error("❌ Error al enviar el formulario. Por favor intente nuevamente.")

def main():
    st.set_page_config(page_title="Jamasolvida", page_icon=":rose:", layout="centered")
    
    # Inicializar estado de sesión
    if 'show_form' not in st.session_state:
        st.session_state.show_form = True
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if 'form_type' not in st.session_state:
        st.session_state.form_type = ""
    
    # Mostrar encabezado con logo y miniatura clickable
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo_jamasolvidad.jpg", width=150)
    with col2:
        # Miniatura clickable con ícono de play
        thumbnail_html = f"""
        <div style="position: relative; display: inline-block; cursor: pointer;" onclick="window.open('{VIDEO_URL}', '_blank')">
            <img src="video_thumbnail.jpg" width="300" style="border-radius: 10px; border: 2px solid #3498db;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="#ffffff" style="filter: drop-shadow(2px 2px 4px #000000);">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
                </svg>
            </div>
        </div>
        """
        st.markdown(thumbnail_html, unsafe_allow_html=True)
    
    st.title("Bienvenido a Jamasolvida")
    st.write("Servicios conmemorativos para honrar la memoria de tus seres queridos")
    
    # Navegación
    if st.session_state.show_form:
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
    else:
        if st.session_state.form_submitted:
            st.success(f"✅ Formulario de {st.session_state.form_type} enviado correctamente. Recibirás un correo de confirmación.")
            st.balloons()
        
        if st.button("Volver al inicio"):
            st.session_state.show_form = True
            st.session_state.form_submitted = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()