from rest_framework import serializers
from .models import Documento, Funcionario, LocalMobilizacao

class LocalMobilizacaoSerializer(serializers.ModelSerializer):
    """Serializer para LocalMobilizacao"""
    class Meta:
        model = LocalMobilizacao
        fields = '__all__'

class FuncionarioSerializer(serializers.ModelSerializer):
    """Serializer para Funcionario"""
    # Para um relacionamento ManyToMany, definimos many=True
    local_mobilizacao = LocalMobilizacaoSerializer(read_only=True, many=True)
    local_mobilizacao_id = serializers.PrimaryKeyRelatedField(
        queryset=LocalMobilizacao.objects.all(),
        source='local_mobilizacao',
        write_only=True,
        many=True
    )
    
    class Meta:
        model = Funcionario
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    """Serializer para Documento"""
    funcionario = FuncionarioSerializer(read_only=True)
    funcionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.all(),
        source='funcionario',
        write_only=True
    )
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Documento
        fields = '__all__'
    
    def get_status(self, obj):
        """Retorna o status do documento"""
        from django.utils import timezone
        hoje = timezone.now().date()
        dias_restantes = (obj.data_validade - hoje).days
        
        if dias_restantes < 0:
            return 'Vencido'
        elif dias_restantes <= 7:
            return 'Crítico'
        elif dias_restantes <= 30:
            return 'Vencendo'
        else:
            return 'Em Dia' 