from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Documento, Funcionario, LocalMobilizacao

def criar_grupos_permissoes():
    """Cria os grupos e permissões do sistema"""
    # Grupo Administrador
    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    
    # Grupo Gestor
    gestor_group, _ = Group.objects.get_or_create(name='Gestor')
    
    # Grupo Visualizador
    visualizador_group, _ = Group.objects.get_or_create(name='Visualizador')
    
    # Permissões para Documentos
    doc_content_type = ContentType.objects.get_for_model(Documento)
    doc_permissions = Permission.objects.filter(content_type=doc_content_type)
    
    # Permissões para Funcionários
    func_content_type = ContentType.objects.get_for_model(Funcionario)
    func_permissions = Permission.objects.filter(content_type=func_content_type)
    
    # Permissões para Locais
    local_content_type = ContentType.objects.get_for_model(LocalMobilizacao)
    local_permissions = Permission.objects.filter(content_type=local_content_type)
    
    # Atribuir permissões ao grupo Administrador
    admin_group.permissions.add(*doc_permissions)
    admin_group.permissions.add(*func_permissions)
    admin_group.permissions.add(*local_permissions)
    
    # Atribuir permissões ao grupo Gestor
    gestor_permissions = [
        'view_documento',
        'add_documento',
        'change_documento',
        'view_funcionario',
        'add_funcionario',
        'change_funcionario',
        'view_localmobilizacao',
    ]
    for perm in gestor_permissions:
        if perm.startswith('documento'):
            gestor_group.permissions.add(*doc_permissions.filter(codename=perm))
        elif perm.startswith('funcionario'):
            gestor_group.permissions.add(*func_permissions.filter(codename=perm))
        elif perm.startswith('localmobilizacao'):
            gestor_group.permissions.add(*local_permissions.filter(codename=perm))
    
    # Atribuir permissões ao grupo Visualizador
    visualizador_permissions = [
        'view_documento',
        'view_funcionario',
        'view_localmobilizacao',
    ]
    for perm in visualizador_permissions:
        if perm.startswith('documento'):
            visualizador_group.permissions.add(*doc_permissions.filter(codename=perm))
        elif perm.startswith('funcionario'):
            visualizador_group.permissions.add(*func_permissions.filter(codename=perm))
        elif perm.startswith('localmobilizacao'):
            visualizador_group.permissions.add(*local_permissions.filter(codename=perm))

def verificar_permissao(user, model, action):
    """Verifica se o usuário tem permissão para realizar uma ação"""
    if user.is_superuser:
        return True
    
    codename = f'{action}_{model.__name__.lower()}'
    return user.has_perm(f'gestao_docs.{codename}') 