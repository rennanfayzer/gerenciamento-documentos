import os
import json
from datetime import datetime
from django.conf import settings
from django.core import serializers
from .models import Documento, Funcionario, LocalMobilizacao, LogAtividade

def criar_backup():
    """Cria um backup dos dados do sistema"""
    try:
        # Criar diretório de backup se não existir
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Nome do arquivo de backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
        
        # Dados para backup
        backup_data = {
            'documentos': serializers.serialize('json', Documento.objects.all()),
            'funcionarios': serializers.serialize('json', Funcionario.objects.all()),
            'locais': serializers.serialize('json', LocalMobilizacao.objects.all()),
            'logs': serializers.serialize('json', LogAtividade.objects.all()),
            'timestamp': timestamp
        }
        
        # Salvar backup
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f)
        
        return True, backup_file
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
        return False, str(e)

def restaurar_backup(backup_file):
    """Restaura um backup do sistema"""
    try:
        # Ler arquivo de backup
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        # Restaurar dados
        for model_data in backup_data['documentos']:
            obj = serializers.deserialize('json', json.dumps([model_data]))
            for item in obj:
                item.save()
        
        for model_data in backup_data['funcionarios']:
            obj = serializers.deserialize('json', json.dumps([model_data]))
            for item in obj:
                item.save()
        
        for model_data in backup_data['locais']:
            obj = serializers.deserialize('json', json.dumps([model_data]))
            for item in obj:
                item.save()
        
        for model_data in backup_data['logs']:
            obj = serializers.deserialize('json', json.dumps([model_data]))
            for item in obj:
                item.save()
        
        return True
    except Exception as e:
        print(f"Erro ao restaurar backup: {e}")
        return False

def listar_backups():
    """Lista todos os backups disponíveis"""
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    if not os.path.exists(backup_dir):
        return []
    
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith('backup_') and file.endswith('.json'):
            file_path = os.path.join(backup_dir, file)
            backups.append({
                'nome': file,
                'caminho': file_path,
                'data': datetime.fromtimestamp(os.path.getctime(file_path))
            })
    
    return sorted(backups, key=lambda x: x['data'], reverse=True) 