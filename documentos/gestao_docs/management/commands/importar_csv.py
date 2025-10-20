import pandas as pd
from django.core.management.base import BaseCommand
from gestao_docs.models import Funcionario, Documento, LocalMobilizacao
from datetime import datetime

class Command(BaseCommand):
    help = 'Importa dados dos CSVs corretamente ajustados'

    def handle(self, *args, **kwargs):
        # Locais de Mobilização
        df_locais = pd.read_csv('local_mobilizacao.csv')
        for _, row in df_locais.iterrows():
            LocalMobilizacao.objects.get_or_create(
                id=row['id'],
                defaults={'nome': row['nome'], 'emails': row.get('emails', '')}
            )

        # Funcionários
        df_funcionarios = pd.read_csv('funcionarios.csv')
        for _, row in df_funcionarios.iterrows():
            Funcionario.objects.get_or_create(
                id=row['id'],
                defaults={
                    'nome': row['nome'],
                    'matricula': row['matricula'],
                    'ativo': bool(row['ativo'])
                }
            )

        # Associar Funcionários aos Locais (ManyToMany)
        df_funcionario_locais = pd.read_csv('funcionario_locais.csv')
        for _, row in df_funcionario_locais.iterrows():
            funcionario = Funcionario.objects.filter(id=row['funcionario_id']).first()
            local = LocalMobilizacao.objects.filter(id=row['local_mobilizacao_id']).first()
            if funcionario and local:
                funcionario.local_mobilizacao.add(local)
                print(f"Associado {funcionario.nome} ao local {local.nome}")

        # Documentos
        df_documentos = pd.read_csv('documentos.csv')
        for _, row in df_documentos.iterrows():
            funcionario = Funcionario.objects.filter(id=row['usuario_id']).first()
            local = LocalMobilizacao.objects.filter(id=row['local_id']).first()

            if funcionario and local:
                try:
                    data_emissao = datetime.strptime(row['data_emissao'], '%d/%m/%Y').date()
                    data_validade = datetime.strptime(row['data_validade'], '%d/%m/%Y').date()
                except Exception as e:
                    print(f"Erro nas datas do documento {row['id']}: {e}")
                    continue

                Documento.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'funcionario': funcionario,
                        'local_mobilizacao': local,
                        'nome_documento': row['nome_documento'],
                        'tipo_documento': row['tipo_documento'],
                        'data_emissao': data_emissao,
                        'data_validade': data_validade,
                        'arquivo': row['caminho_pdf'].replace('\\', '/'),
                    }
                )
                print(f"Documento {row['nome_documento']} importado para {funcionario.nome} no local {local.nome}")

        self.stdout.write(self.style.SUCCESS('Migração finalizada com sucesso!'))
