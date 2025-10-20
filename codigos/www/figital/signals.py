from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

import requests
from django.db.models.signals import post_migrate, post_save
from .models import InscricaoDesenvolvedor

@receiver(post_migrate)
def criar_superusuarios(sender, **kwargs):
    """Cria os grupos necessários e os superusuários automaticamente após migrações."""
    User = get_user_model()

    try:
        # Criar ou obter grupos
        grupo_exclusao, _ = Group.objects.get_or_create(name="Grupo de Exclusão")
        grupo_edicao, _ = Group.objects.get_or_create(name="Grupo de Edição")

        # Criar superusuário 'admin' se não existir
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'carlos.rodrigues@recife.pe.gov.br',
                'nome_completo': 'Carlos Eduardo',
                'telefone': '(81) 98717-2274',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('@Admin123')  # Define a senha corretamente
            admin_user.save()  # Salva as alterações
            admin_user.groups.add(grupo_exclusao, grupo_edicao)
            print("✅ Superusuário 'admin' criado e adicionado aos grupos!")

        # Criar superusuário 'joao' se não existir
        joao_user, created = User.objects.get_or_create(
            username='joao',  # Corrigido para evitar erro de duplicação
            defaults={
                'email': 'joaocarloscosta@recife.pe.gov.br',
                'nome_completo': 'João Carlos Costa',
                'telefone': '(81) 98765-0747',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            joao_user.set_password('112358')  # Define a senha corretamente
            joao_user.save()  # Salva as alterações
            joao_user.groups.add(grupo_exclusao, grupo_edicao)
            print("✅ Superusuário 'joao' criado e adicionado aos grupos!")

    except Exception as e:
        print(f"⚠️ Erro ao criar superusuários: {e}")



# ===================================================================
# SINAL PARA ENVIAR WEBHOOK AO N8N QUANDO UM NOVO REGISTRO É CRIADO
# ===================================================================
@receiver(post_save, sender=InscricaoDesenvolvedor)
def enviar_webhook_n8n(sender, instance, created, **kwargs):
    """
    Este sinal é acionado sempre que uma nova inscrição é salva.
    """
    # O webhook só será enviado se um NOVO registro for criado.
    if created:
        # **COLOQUE O LINK DO SEU WEBHOOK DO N8N AQUI**
        webhook_url = "https://webhook-n8n-dev-conectarecife.recife.pe.gov.br/webhook/figitaldesenvolvedor"

        # Prepara os dados para enviar (em formato JSON)
        payload = {
            'id': instance.id, 
            'nome': instance.nome,
            'telefone': instance.telefone,
            'email': instance.email,
            'unidade_secretaria': instance.unidade_secretaria,
            'chefia_imediata': instance.chefia_imediata,
            'linguagem_ferramenta': instance.linguagem_ferramenta,
            'principal_desafio': instance.principal_desafio,
            'data_inscricao': instance.data_inscricao.isoformat()
        }

        try:
            # Envia a requisição POST para o n8n
            response = requests.post(webhook_url, json=payload, timeout=10)
            # Verifica se a requisição foi bem-sucedida (código 2xx)
            response.raise_for_status() 
            print(f"✅ Webhook enviado com sucesso para o n8n para a inscrição: {instance.nome}")
        except requests.exceptions.RequestException as e:
            # Em caso de erro, imprime no console do servidor
            print(f"⚠️ ERRO ao enviar webhook para o n8n: {e}")