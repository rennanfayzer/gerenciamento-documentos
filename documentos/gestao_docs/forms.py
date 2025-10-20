from django import forms
from .models import LocalMobilizacao, Funcionario, Documento, GestorLocal, Perfil
from django.contrib.auth.forms import AuthenticationForm


class LocalMobilizacaoForm(forms.ModelForm):
    class Meta:
        model = LocalMobilizacao
        fields = ['nome', 'emails']



class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'matricula', 'ativo', 'local_mobilizacao']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # <-- recebe o usuário
        super().__init__(*args, **kwargs)

        # ✅ Adiciona classes Bootstrap e Select2
        self.fields['local_mobilizacao'].widget.attrs.update({
            'class': 'form-select select2',
            'multiple': 'multiple'
        })

        # ✅ Restringe opções se não for superuser
        if user and not user.is_superuser:
            from .models import GestorLocal
            # Obtém o gestor vinculado ao usuário
            gestor = GestorLocal.objects.filter(user=user).first()
            if gestor:
                # Ajuste: GestorLocal possui relação ManyToMany com LocalMobilizacao através de 'locais'.
                # Portanto, restringe o queryset aos locais associados ao gestor.
                self.fields['local_mobilizacao'].queryset = gestor.locais.all()

class DocumentoForm(forms.ModelForm):
    data_emissao = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        input_formats=['%Y-%m-%d'],
    )
    data_validade = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Documento
        fields = [
            'local_mobilizacao',
            'nome_documento',
            'tipo_documento',
            'data_emissao',
            'data_validade',
            'arquivo'
        ]

class GestorLocalForm(forms.ModelForm):
    class Meta:
        model = GestorLocal
        fields = ['user', 'locais']
        widgets = {
            'locais': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Usuário'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })

class SearchForm(forms.Form):
    nome = forms.CharField(
        label='Nome do Documento',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    nome_funcionario = forms.CharField(
        label='Nome do Funcionário',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    cargo = forms.CharField(
        label='Cargo',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    local = forms.CharField(
        label='Local',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil']
