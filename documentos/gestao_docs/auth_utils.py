import pyotp
import qrcode
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def gerar_chave_secreta():
    """Gera uma chave secreta para autenticação em dois fatores"""
    return pyotp.random_base32()

def gerar_qr_code(chave_secreta, email):
    """Gera um QR code para autenticação em dois fatores"""
    totp = pyotp.TOTP(chave_secreta)
    provisioning_uri = totp.provisioning_uri(email, issuer_name="Sistema de Gestão de Documentos")
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()

def verificar_codigo(chave_secreta, codigo):
    """Verifica se o código 2FA está correto"""
    totp = pyotp.TOTP(chave_secreta)
    return totp.verify(codigo)

def enviar_codigo_email(user, codigo):
    """Envia o código 2FA por email"""
    try:
        send_mail(
            'Código de Autenticação',
            f'Seu código de autenticação é: {codigo}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar código por email: {e}")
        return False

def gerar_codigo_email():
    """Gera um código numérico para autenticação por email"""
    return pyotp.random_base32()[:6].upper()

def verificar_codigo_email(codigo_gerado, codigo_digitado):
    """Verifica se o código de email está correto"""
    return codigo_gerado == codigo_digitado 