from django.utils import timezone
from datetime import timedelta
from .models import Documento
from .notifications import verificar_documentos_vencendo, verificar_documentos_vencidos
from .backup_utils import criar_backup
from .cache_utils import limpar_cache

def gerar_relatorio_semanal():
    """Gera um relatório semanal dos documentos"""
    hoje = timezone.now().date()
    semana_passada = hoje - timedelta(days=7)
    
    documentos_vencidos = Documento.objects.filter(
        data_vencimento__lt=hoje
    ).count()
    
    documentos_criticos = Documento.objects.filter(
        data_vencimento__lte=hoje + timedelta(days=7),
        data_vencimento__gt=hoje
    ).count()
    
    documentos_em_dia = Documento.objects.filter(
        data_vencimento__gt=hoje + timedelta(days=7)
    ).count()
    
    return {
        'vencidos': documentos_vencidos,
        'criticos': documentos_criticos,
        'em_dia': documentos_em_dia,
        'total': documentos_vencidos + documentos_criticos + documentos_em_dia
    }

def executar_tarefas_agendadas():
    """Executa todas as tarefas agendadas"""
    # Verificar documentos vencendo
    verificar_documentos_vencendo()
    
    # Verificar documentos vencidos
    verificar_documentos_vencidos()
    
    # Gerar relatório semanal
    relatorio = gerar_relatorio_semanal()
    
    return relatorio

def executar_tarefas_diarias():
    """Executa tarefas diárias do sistema"""
    # Verificar documentos vencendo
    verificar_documentos_vencendo()
    
    # Verificar documentos vencidos
    verificar_documentos_vencidos()
    
    # Limpar cache antigo
    limpar_cache()
    
    return True

def executar_tarefas_semanais():
    """Executa tarefas semanais do sistema"""
    # Criar backup
    criar_backup()
    
    return True

def executar_tarefas_mensais():
    """Executa tarefas mensais do sistema"""
    # Limpar logs antigos
    from .log_utils import limpar_logs_antigos
    limpar_logs_antigos(dias=90)
    
    return True 