from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from ..models import PrimeiroEscalao, RedeTransformacaoDigital

class ViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="teste@example.com", password="senha123", username="teste_user"
        )

        # Criando grupos e adicionando o usuário ao grupo correto
        self.admin_group = Group.objects.get_or_create(name="Grupo de Exclusão")[0]
        self.edit_group = Group.objects.get_or_create(name="Grupo de Edição")[0]
        self.user.groups.add(self.admin_group)
        self.user.groups.add(self.edit_group)

        self.client.login(email="teste@example.com", password="senha123")

        self.escalao = PrimeiroEscalao.objects.create(
            nome="Teste Nome", secretaria="Secretaria Teste", cargo="Cargo Teste",
            email="teste@example.com", telefone="123456789", problema_urgente="Problema crítico"
        )
        self.transformacao = RedeTransformacaoDigital.objects.create(
            nome="Teste Nome", secretaria="Secretaria Teste", cargo="Cargo Teste",
            email="teste@example.com", telefone="123456789",
            chefe_imediato="Chefe Teste", problema_urgente="Problema crítico"
        )

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_autenticado_view(self):
        response = self.client.get(reverse("index_autenticado"))
        self.assertEqual(response.status_code, 200)

    def test_primeiro_escalao_view(self):
        response = self.client.post(reverse("primeiro_escalao"), {
            "nome": "Novo Nome",
            "secretaria": "Nova Secretaria",
            "cargo": "Novo Cargo",
            "email": "novo@example.com",
            "telefone": "123456789",
            "problema_urgente": "Novo problema crítico"
        })
        self.assertContains(response, "Formulário enviado com sucesso!")

    def test_rede_transformacao_view(self):
        response = self.client.post(reverse("rede_transformacao"), {
            "nome": "Novo Nome",
            "secretaria": "Nova Secretaria",
            "cargo": "Novo Cargo",
            "email": "novo@example.com",
            "telefone": "123456789",
            "chefe_imediato": "Novo Chefe",
            "problema_urgente": "Novo problema crítico"
        })
        self.assertContains(response, "Formulário enviado com sucesso!")

    def test_login_view_success(self):
        response = self.client.post(reverse("login"), {
            "email": "teste@example.com",
            "password": "senha123"
        })
        self.assertRedirects(response, reverse("index_autenticado"))

    def test_login_view_failure(self):
        response = self.client.post(reverse("login"), {
            "email": "teste@example.com",
            "password": "senha_incorreta"
        })
        self.assertContains(response, "E-mail ou senha inválidos.")

    def test_visualizar_escalao_view(self):
        response = self.client.get(reverse("visualizar_escalao"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teste Nome")

    def test_visualizar_transformacao_view(self):
        response = self.client.get(reverse("visualizar_transformacao"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teste Nome")

    def test_excluir_registro_escalao(self):
        response = self.client.post(reverse("excluir_registro_escalao", args=[self.escalao.id]))
        self.assertRedirects(response, reverse("visualizar_escalao"))
        self.assertFalse(PrimeiroEscalao.objects.filter(id=self.escalao.id).exists())

    def test_excluir_registro_transformacao(self):
        response = self.client.post(reverse("excluir_registro_transformacao", args=[self.transformacao.id]))
        self.assertRedirects(response, reverse("visualizar_transformacao"))
        self.assertFalse(RedeTransformacaoDigital.objects.filter(id=self.transformacao.id).exists())

    def test_editar_registro_escalao(self):
        response = self.client.post(reverse("editar_registro_escalao", args=[self.escalao.id]), {
            "nome": "Nome Editado",
            "secretaria": "Secretaria Editada",
            "cargo": "Cargo Editado",
            "email": "editado@example.com",
            "telefone": "987654321",
            "problema_urgente": "Problema atualizado"
        })
        self.assertRedirects(response, reverse("visualizar_escalao"))
        self.escalao.refresh_from_db()
        self.assertEqual(self.escalao.nome, "Nome Editado")

    def test_editar_registro_transformacao(self):
        response = self.client.post(reverse("editar_registro_transformacao", args=[self.transformacao.id]), {
            "nome": "Nome Editado",
            "secretaria": "Secretaria Editada",
            "cargo": "Cargo Editado",
            "email": "editado@example.com",
            "telefone": "987654321",
            "chefe_imediato": "Novo Chefe",
            "problema_urgente": "Problema atualizado"
        })
        self.assertRedirects(response, reverse("visualizar_transformacao"))
        self.transformacao.refresh_from_db()
        self.assertEqual(self.transformacao.chefe_imediato, "Novo Chefe")

    def test_exportar_escalao_excel(self):
        response = self.client.get(reverse("exportar_escalao"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertContains(response, "Nome,Secretaria,Cargo,Email,Telefone,Problema Urgente")

    def test_exportar_transformacao_excel(self):
        response = self.client.get(reverse("exportar_transformacao"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertContains(response, "Nome,Secretaria,Cargo,Email,Telefone,Chefe Imediato,Problema Urgente")
