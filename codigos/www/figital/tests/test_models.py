from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import BaseFormulario, PrimeiroEscalao, RedeTransformacaoDigital
from model_mommy import mommy

class UsuarioManagerTests(TestCase):
    
    def setUp(self):
        self.email = "usuario@example.com"
        self.password = "testpassword123"
        self.username = "usuario_teste"
    
    def test_create_user(self):
        user = get_user_model().objects.create_user(email=self.email, password=self.password, username=self.username)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(self.password))
    
    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(email=self.email, password=self.password, username=self.username)
        self.assertEqual(superuser.email, self.email)
        self.assertEqual(superuser.username, self.username)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.check_password(self.password))

    def test_str_usuario(self):
        user = get_user_model().objects.create_user(email=self.email, password=self.password)
        self.assertEqual(str(user), self.email)


class BaseFormularioTests(TestCase):
    
    def test_str_primeiro_escalao(self):
        form = PrimeiroEscalao.objects.create(
            nome="Teste Nome",
            secretaria="Secretaria Teste",
            cargo="Cargo Teste",
            email="teste@example.com",
            telefone="123456789",
            problema_urgente="Teste de urgência"
        )
        self.assertEqual(str(form), f"1º Escalão - {form.nome}")

    def test_str_rede_transformacao_digital(self):
        form = RedeTransformacaoDigital.objects.create(
            nome="Teste Nome",
            secretaria="Secretaria Teste",
            cargo="Cargo Teste",
            email="teste@example.com",
            telefone="123456789",
            problema_urgente="Teste de urgência",
            chefe_imediato="Chefe Teste"
        )
        self.assertEqual(str(form), f"Rede de Transformação Digital - {form.nome}")


# class BaseFormularioTestCase(TestCase):
#     def setUp(self):
#         self.nome = mommy.make('nome')
#     def test_str(self):
#         self.assertEqual(str(self.nome), self.nome.nome)


class TestFormulario(BaseFormulario):
    class Meta:
        abstract = False  # Permite que Django crie a tabela

def test_str_base_formulario(self):
    form = mommy.make(TestFormulario, nome="Teste Nome")
    self.assertEqual(str(form), form.nome)
