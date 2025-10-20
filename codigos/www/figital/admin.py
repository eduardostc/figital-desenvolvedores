from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, InscricaoDesenvolvedor # IMPORTAÇÃO CORRIGIDA

# Configuração do modelo de usuário personalizado no Admin (Mantido)
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['nome_completo', 'email', 'username', 'telefone', 'is_staff', 'is_active']
    search_fields = ['nome_completo', 'email', 'username', 'telefone']
    ordering = ['nome_completo']
    fieldsets = (
        (None, {'fields': ('nome_completo', 'email', 'username', 'telefone', 'password')}),  
        ('Permissões', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome_completo', 'email', 'username', 'telefone', 'password', 'is_staff', 'is_superuser'),
        }),
    )

# Nova configuração para exibir o modelo de Inscrição de Desenvolvedor no Admin
@admin.register(InscricaoDesenvolvedor)
class InscricaoDesenvolvedorAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 
        'unidade_secretaria', 
        'linguagem_ferramenta', 
        'email', 
        'telefone', 
        'data_inscricao'
    ]
    search_fields = ['nome', 'unidade_secretaria', 'linguagem_ferramenta', 'email']
    list_filter = ['unidade_secretaria', 'data_inscricao']
    ordering = ['-data_inscricao']