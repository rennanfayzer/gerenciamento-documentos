from .models import LogAtividade
from django.utils import timezone

def registrar_atividade(usuario, acao, modelo, objeto_id, detalhes='', ip_address=None):
    """Registra uma atividade no sistema"""
    try:
        LogAtividade.objects.create(
            usuario=usuario,
            acao=acao,
            modelo=modelo,
            objeto_id=objeto_id,
            detalhes=detalhes,
            ip_address=ip_address
        )
        return True
    except Exception as e:
        print(f"Erro ao registrar atividade: {e}")
        return False

def obter_logs_por_usuario(usuario, dias=30):
    """Obtém os logs de um usuário nos últimos dias"""
    data_limite = timezone.now() - timezone.timedelta(days=dias)
    return LogAtividade.objects.filter(
        usuario=usuario,
        data_hora__gte=data_limite
    ).order_by('-data_hora')

def obter_logs_por_modelo(modelo, dias=30):
    """Obtém os logs de um modelo nos últimos dias"""
    data_limite = timezone.now() - timezone.timedelta(days=dias)
    return LogAtividade.objects.filter(
        modelo=modelo,
        data_hora__gte=data_limite
    ).order_by('-data_hora')

def obter_logs_por_acao(acao, dias=30):
    """Obtém os logs de uma ação nos últimos dias"""
    data_limite = timezone.now() - timezone.timedelta(days=dias)
    return LogAtividade.objects.filter(
        acao=acao,
        data_hora__gte=data_limite
    ).order_by('-data_hora')

def limpar_logs_antigos(dias=90):
    """Remove logs mais antigos que o número de dias especificado"""
    data_limite = timezone.now() - timezone.timedelta(days=dias)
    LogAtividade.objects.filter(data_hora__lt=data_limite).delete() 