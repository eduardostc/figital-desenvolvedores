from django import forms
from .models import InscricaoDesenvolvedor, Usuario
from django.contrib.auth.forms import UserCreationForm

# Formulário de criação de usuários
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password1', 'password2']

# NOVO FORMULÁRIO PARA CADASTRO DE DESENVOLVEDORES
class InscricaoDesenvolvedorForm(forms.ModelForm):
    class Meta:
        model = InscricaoDesenvolvedor
        # Lista de todos os campos do modelo que aparecerão no formulário
        fields = [
            'nome',
            'telefone',
            'email',
            'unidade_secretaria',
            'chefia_imediata',
            'linguagem_ferramenta',
            'principal_desafio',
        ]
        
        # Personaliza os textos que aparecem acima de cada campo
        labels = {
            'nome': 'Nome Completo:',
            'telefone': 'Telefone (Whatsapp):',
            'email': 'E-mail:',
            'unidade_secretaria': 'Unidade ou Secretaria:',
            'chefia_imediata': 'Nome da sua Chefia Imediata:',
            'linguagem_ferramenta': 'Principal linguagem ou ferramenta que você utiliza:',
            'principal_desafio': 'Qual seu principal desafio técnico ou de gestão no trabalho?',
        }
        
        # Adiciona atributos HTML para melhorar a experiência do usuário
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite seu nome completo'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(81) 99999-9999',
            'class': 'mask-telefone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seu.email@recife.pe.gov.br'}),
            'unidade_secretaria': forms.TextInput(attrs={'placeholder': 'Ex: Emprel, Secretaria de Finanças'}),
            'chefia_imediata': forms.TextInput(attrs={'placeholder': 'Nome do gestor ou líder direto'}),
            'linguagem_ferramenta': forms.TextInput(attrs={'placeholder': 'Ex: Python, Django, Power BI, JavaScript...'}),
            'principal_desafio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva o maior desafio que você enfrenta em seus projetos ou no dia a dia.'
            }),
        }