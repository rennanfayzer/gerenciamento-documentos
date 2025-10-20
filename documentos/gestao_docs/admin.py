from django.contrib import admin
from .models import LocalMobilizacao, Funcionario, Documento, GestorLocal, Perfil

admin.site.register(LocalMobilizacao)
admin.site.register(Funcionario)
admin.site.register(Documento)
admin.site.register(GestorLocal)
admin.site.register(Perfil)

