from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
#Metodo para exportar para excel
import csv
import datetime
from django.http import HttpResponse, HttpResponseForbidden
# Modelos e Formulários atualizados
from .models import InscricaoDesenvolvedor
from .forms import InscricaoDesenvolvedorForm, UsuarioForm


# Página inicial
def index(request):
    return render(request, 'figital/index.html')

# View para o novo formulário de inscrição de desenvolvedores
def inscricao_desenvolvedor(request):
    if request.method == "POST":
        form = InscricaoDesenvolvedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua inscrição foi realizada com sucesso!')
            # Limpa o formulário após o envio para permitir um novo cadastro
            return redirect('inscricao_desenvolvedores') # Redireciona para a mesma página, limpa
        else:
            messages.error(request, 'Erro ao enviar o formulário. Por favor, verifique os dados.')
    else:
        form = InscricaoDesenvolvedorForm()
    
    context = {
        'form': form
    }
    # Lembre-se de criar o template 'form_desenvolvedor.html'
    return render(request, 'figital/form_desenvolvedor.html', context)


# Tela de Login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Melhor usar .get() para evitar erros
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index_autenticado') 
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
    return render(request, 'figital/login.html')

# ===================================================================
#             VIEWS PROTEGIDAS (REQUEREM AUTENTICAÇÃO)
# ===================================================================

# Página inicial para usuários autenticados
@login_required  # Opcional: protege a rota para usuários logados
def index_autenticado(request):
    return render(request, 'figital/index_autenticado.html')

@login_required
def visualizar_inscricoes(request):
    if str(request.user) != 'AnonymousUser':
        # Verifica as permissões do usuário logado
        pertence_grupo_edicao = request.user.groups.filter(name="Grupo de Edição").exists()
        pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

        # Busca todos os registros do novo modelo
        registros = InscricaoDesenvolvedor.objects.all().order_by('-data_inscricao')

        context = {
            'registros': registros,
            'pertence_grupo_edicao': pertence_grupo_edicao,
            'pertence_grupo_exclusao': pertence_grupo_exclusao,
        }
        # Lembre-se de criar o template 'visualizar_inscricoes.html'
        return render(request, 'figital/visualizar_inscricoes.html', context)
    else:
        return redirect('index')


# View UNIFICADA para editar um registro (Padrão Original)
@login_required
def editar_inscricao(request, registro_id):
    registro = get_object_or_404(InscricaoDesenvolvedor, id=registro_id)

    # Verifica se o usuário pertence ao grupo "Grupo de Edição"
    pertence_grupo_edicao = request.user.groups.filter(name="Grupo de Edição").exists()

    if not pertence_grupo_edicao:
        return HttpResponseForbidden("Você não tem permissão para editar este registro.")

    if request.method == 'POST':
        form = InscricaoDesenvolvedorForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizado com sucesso.")
            return redirect('visualizar_inscricoes') # Redireciona para a lista
    else:
        # Carrega o formulário com os dados do registro existente
        # OBS: Corrigido de 'isinstance' para 'instance', que é o correto
        form = InscricaoDesenvolvedorForm(instance=registro)

    context = {
        'form': form, # Passa o formulário para o template
        'registro': registro,
        'pertence_grupo_edicao': pertence_grupo_edicao,
    }
    # Lembre-se de criar o template 'editar_inscricao.html'
    return render(request, 'figital/editar_inscricao.html', context)


# View UNIFICADA para excluir um registro (Padrão Original)
@login_required
def excluir_inscricao(request, registro_id):
    registro = get_object_or_404(InscricaoDesenvolvedor, id=registro_id)

    # Verifica se o usuário pertence ao grupo "Grupo de Exclusão"
    pertence_grupo_exclusao = request.user.groups.filter(name="Grupo de Exclusão").exists()

    if not pertence_grupo_exclusao:
        return HttpResponseForbidden("Você não tem permissão para excluir este registro.")

    if request.method == 'POST':
        registro.delete()
        messages.success(request, "Registro removido com sucesso.")
        # O 'next' aqui é opcional, mas mantive o padrão de redirecionar para a lista
        next_url = request.GET.get('next', 'visualizar_inscricoes')
        return redirect(next_url)
    
    context = {
        'registro': registro,
        'pertence_grupo_exclusao': pertence_grupo_exclusao,
    }
    # O ideal aqui seria renderizar uma página de confirmação de exclusão
    # Mas para manter o padrão, renderiza a index ou a página de visualização
    return render(request, 'figital/visualizar_inscricoes.html', context)


# View UNIFICADA para exportar para CSV (Padrão Original)
@login_required
def exportar_inscricoes_csv(request):
    # Configurando a resposta HTTP para um arquivo CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    filename = f'inscricoes_desenvolvedores_{datetime.date.today()}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(u'\ufeff'.encode('utf8')) # Garante a codificação correta

    writer = csv.writer(response, delimiter=';')
    
    # Escrevendo o cabeçalho com os novos campos
    writer.writerow([
        'ID', 'Data da Inscrição', 'Nome Completo', 'Telefone', 'E-mail',
        'Unidade/Secretaria', 'Chefia Imediata', 'Linguagem/Ferramenta', 'Principal Desafio'
    ])

    # Escrevendo os dados de cada registro
    registros = InscricaoDesenvolvedor.objects.all()
    for registro in registros:
        writer.writerow([
            registro.id,
            registro.data_inscricao.strftime("%d/%m/%Y %H:%M"),
            registro.nome,
            registro.telefone,
            registro.email,
            registro.unidade_secretaria,
            registro.chefia_imediata,
            registro.linguagem_ferramenta,
            registro.principal_desafio
        ])

    return response