from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from datetime import timedelta
from .models import Documento, Funcionario, LocalMobilizacao
from .serializers import (
    DocumentoSerializer,
    FuncionarioSerializer,
    LocalMobilizacaoSerializer
)

class DocumentoFilter(filters.FilterSet):
    """Filtros para documentos"""
    data_inicio = filters.DateFilter(field_name='data_validade', lookup_expr='gte')
    data_fim = filters.DateFilter(field_name='data_validade', lookup_expr='lte')
    tipo = filters.CharFilter(field_name='tipo_documento')
    status = filters.CharFilter(method='filter_status')
    
    class Meta:
        model = Documento
        fields = ['data_inicio', 'data_fim', 'tipo', 'status']
    
    def filter_status(self, queryset, name, value):
        from django.utils import timezone
        hoje = timezone.now().date()
        
        if value == 'vencidos':
            return queryset.filter(data_validade__lt=hoje)
        elif value == 'criticos':
            return queryset.filter(
                data_validade__lte=hoje + timedelta(days=7),
                data_validade__gt=hoje
            )
        elif value == 'vencendo':
            return queryset.filter(
                data_validade__lte=hoje + timedelta(days=30),
                data_validade__gt=hoje + timedelta(days=7)
            )
        elif value == 'em_dia':
            return queryset.filter(data_validade__gt=hoje + timedelta(days=30))
        return queryset

class DocumentoViewSet(viewsets.ModelViewSet):
    """API para documentos"""
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = DocumentoFilter
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos documentos"""
        from .cache_utils import cache_documentos_por_status, cache_documentos_por_tipo
        
        return Response({
            'por_status': cache_documentos_por_status(),
            'por_tipo': cache_documentos_por_tipo()
        })

class FuncionarioViewSet(viewsets.ModelViewSet):
    """API para funcionários"""
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['local_mobilizacao', 'status']
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos funcionários"""
        from .cache_utils import cache_funcionarios_por_local
        
        return Response({
            'por_local': cache_funcionarios_por_local()
        })

class LocalMobilizacaoViewSet(viewsets.ModelViewSet):
    """API para locais de mobilização"""
    queryset = LocalMobilizacao.objects.all()
    serializer_class = LocalMobilizacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status'] 