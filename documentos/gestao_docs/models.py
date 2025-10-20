from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class LocalMobilizacao(models.Model):
    nome = models.CharField(max_length=100)
    emails = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.nome

class GestorLocal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locais = models.ManyToManyField(LocalMobilizacao, related_name='gestores')

    def __str__(self):
        return f"{self.user.username} - {', '.join([l.nome for l in self.locais.all()])}"

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.IntegerField(unique=True)
    ativo = models.BooleanField(default=True)
    local_mobilizacao = models.ManyToManyField(
        LocalMobilizacao, 
        blank=True, 
        related_name='funcionarios'
    )
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='funcionarios_criados')
    atualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='funcionarios_atualizados')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Documento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    local_mobilizacao = models.ForeignKey(LocalMobilizacao, on_delete=models.CASCADE)
    nome_documento = models.CharField(max_length=200)
    tipo_documento = models.CharField(max_length=100)
    data_emissao = models.DateField()
    data_validade = models.DateField()
    arquivo = models.FileField(upload_to='upload_documentos/', blank=True, null=True)
    ultimo_email_enviado = models.DateField(blank=True, null=True)

    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_criados')
    atualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_atualizados')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_documento} - {self.funcionario.nome} ({self.local_mobilizacao.nome})"

class LogAtividade(models.Model):
    """Modelo para registrar atividades do sistema"""
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    objeto_id = models.IntegerField()
    detalhes = models.TextField(blank=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Log de Atividade'
        verbose_name_plural = 'Logs de Atividades'
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.usuario} - {self.acao} - {self.modelo} - {self.data_hora}"

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='perfil_fotos/', blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

