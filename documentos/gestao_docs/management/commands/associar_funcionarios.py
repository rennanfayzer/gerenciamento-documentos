from gestao_docs.models import Documento

for doc in Documento.objects.all():
    funcionario = doc.funcionario
    local = doc.local_mobilizacao

    if not funcionario.local_mobilizacao.filter(id=local.id).exists():
        funcionario.local_mobilizacao.add(local)
        print(f"Associado automaticamente: {funcionario.nome} ao local {local.nome}")
    else:
        print(f"{funcionario.nome} já está associado ao local {local.nome}")
