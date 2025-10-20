from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Documento

def enviar_notificacao_email(assunto, mensagem, destinatario):
    """Envia um email de notificação"""
    try:
        send_mail(
            assunto,
            mensagem,
            settings.EMAIL_HOST_USER,
            [destinatario],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def verificar_documentos_vencendo():
    """Verifica documentos próximos do vencimento e envia notificações"""
    hoje = timezone.now().date()
    documentos_criticos = Documento.objects.filter(
        data_vencimento__lte=hoje + timedelta(days=7),
        data_vencimento__gt=hoje
    )
    
    for doc in documentos_criticos:
        mensagem = f"""
        Alerta: O documento {doc.nome} está próximo do vencimento!
        Data de vencimento: {doc.data_vencimento}
        Funcionário: {doc.funcionario.nome}
        Tipo: {doc.tipo}
        """
        enviar_notificacao_email(
            "Alerta de Documento Próximo do Vencimento",
            mensagem,
            doc.funcionario.email
        )

def verificar_documentos_vencidos():
    """Verifica documentos vencidos e envia notificações"""
    hoje = timezone.now().date()
    documentos_vencidos = Documento.objects.filter(
        data_vencimento__lt=hoje
    )
    
    for doc in documentos_vencidos:
        mensagem = f"""
        Urgente: O documento {doc.nome} está vencido!
        Data de vencimento: {doc.data_vencimento}
        Funcionário: {doc.funcionario.nome}
        Tipo: {doc.tipo}
        """
        enviar_notificacao_email(
            "Alerta de Documento Vencido",
            mensagem,
            doc.funcionario.email
        ) 