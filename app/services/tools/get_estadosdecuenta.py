from langchain.agents import tool
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from services.models.model_openai import modelo
import os
#from langchain_openai import ChatOpenAI

model = modelo()

#os.environ["OPENAI_API_KEY"] = ""
#model = ChatOpenAI(model="gpt-4o", temperature=0.8)

carpeta = "app\data\estados_de_cuenta"

email = "plaplia1.09@gmail.com"
dni = "12345678"
mes = "agosto"
año = "2024"

def buscar_archivo(carpeta):
    carpeta_dni = os.path.join(carpeta, dni)
    nombre_archivo = f"{dni}_{mes}_{año}.pdf"
    ruta_archivo = os.path.join(carpeta_dni, nombre_archivo)
    
    if os.path.exists(ruta_archivo):
        return ruta_archivo
    else:
        return None
    
def enviar_correo(destinatario, asunto, cuerpo, archivo_adjunto):
    remitente = "c.huapayamanco09@gmail.com"
    contraseña = "ytkb grhu bhwx iszs"

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente 
    mensaje['To'] = destinatario 
    mensaje['Subject'] = asunto 

    mensaje.attach(MIMEText(cuerpo, 'plain'))

    with open(archivo_adjunto, "rb") as adjunto:
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(adjunto.read()) 

        encoders.encode_base64(parte) 

        parte.add_header(
            'Content-Disposition',
            f"attachment; filename= {os.path.basename(archivo_adjunto)}",  # Establece el nombre del archivo adjunto
        )
        mensaje.attach(parte) # Adjunta el archivo al mensaje

    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)
    texto = mensaje.as_string()
    servidor.sendmail(remitente, destinatario, texto)
    servidor.quit() # Cierra la conexión al servidor

def manejar_consulta(carpeta):

    archivo = buscar_archivo(carpeta)
    if archivo:
        asunto = "Tu Estado de Cuenta"
        cuerpo = f"Adjunto encontrarás tu estado de cuenta del mes de {mes} de {año}."
        enviar_correo(email, asunto, cuerpo, archivo)
        return "El estado de cuenta ha sido enviado a tu correo."
    else:
        return "No se encontró un estado de cuenta para esos datos."

@tool
def get_bank_statements(consulta) -> str:
    """Use this tool to send account statements by email"""
    
    archivo = manejar_consulta(carpeta)
    if archivo:
        # Si se encuentra el archivo, define el asunto y cuerpo del correo
        return "Se envió satisfactoriamente el estado de cuenta a su correo."
    else:
        # Si no se encuentra el archivo, retorna un mensaje de error
        return "No se encontró un estado de cuenta para esos datos."


#response = get_bank_statements.invoke("Enviame mi estado de cuenta")
#print(response)
