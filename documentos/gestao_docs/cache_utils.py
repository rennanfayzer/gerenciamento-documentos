from django.core.cache import cache
from django.conf import settings
from datetime import timedelta

def cache_documentos_por_status():
    """Cache dos documentos por status"""
    cache_key = 'documentos_por_status'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        from .models import Documento
        from django.utils import timezone
        
        hoje = timezone.now().date()
        
        data = {
            'vencidos': Documento.objects.filter(data_validade__lt=hoje).count(),
            'criticos': Documento.objects.filter(
                data_validade__lte=hoje + timedelta(days=7),
                data_validade__gt=hoje
            ).count(),
            'em_dia': Documento.objects.filter(data_validade__gt=hoje + timedelta(days=7)).count()
        }
        
        cache.set(cache_key, data, timeout=3600)  # Cache por 1 hora
        return data
    
    return cached_data

def cache_documentos_por_tipo():
    """Cache dos documentos por tipo"""
    cache_key = 'documentos_por_tipo'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        from .models import Documento
        
        tipos = Documento.objects.values_list('tipo_documento', flat=True).distinct()
        data = {}
        
        for tipo in tipos:
            data[tipo] = Documento.objects.filter(tipo_documento=tipo).count()
        
        cache.set(cache_key, data, timeout=3600)  # Cache por 1 hora
        return data
    
    return cached_data

def cache_funcionarios_por_local():
    """Cache dos funcionários por local"""
    cache_key = 'funcionarios_por_local'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        from .models import Funcionario, LocalMobilizacao
        
        locais = LocalMobilizacao.objects.all()
        data = {}
        
        for local in locais:
            data[local.nome] = Funcionario.objects.filter(local_mobilizacao=local).count()
        
        cache.set(cache_key, data, timeout=3600)  # Cache por 1 hora
        return data
    
    return cached_data

def limpar_cache():
    """Limpa todo o cache do sistema"""
    cache.clear()

def invalidar_cache_documentos():
    """Invalida o cache relacionado a documentos"""
    cache.delete('documentos_por_status')
    cache.delete('documentos_por_tipo')

def invalidar_cache_funcionarios():
    """Invalida o cache relacionado a funcionários"""
    cache.delete('funcionarios_por_local') 