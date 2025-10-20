from django.test import TestCase
from ..forms import UsuarioForm, PrimeiroEscalaoForm, RedeTransformacaoDigitalForm
from ..models import Usuario, PrimeiroEscalao, RedeTransformacaoDigital

class UsuarioFormTests(TestCase):

    def test_usuario_form_valid(self):
        form_data = {
            'email': 'teste@example.com',
            'username': 'usuario_teste',
            'password1': 'TestSenha123!',
            'password2': 'TestSenha123!',
        }
        form = UsuarioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_usuario_form_invalid(self):
        form_data = {
            'email': 'teste@example.com',
            'username': 'usuario_teste',
            'password1': 'TestSenha123!',
            'password2': 'SenhaDiferente123!',
        }
        form = UsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class PrimeiroEscalaoFormTests(TestCase):

    def test_primeiro_escalao_form_valid(self):
        form_data = {
            'nome': 'João da Silva',
            'secretaria': 'Secretaria de Tecnologia',
            'cargo': 'Gerente',
            'email': 'joao@example.com',
            'telefone': '(81) 99999-9999',
            'problema_urgente': 'Falta de equipamentos na unidade.',
        }
        form = PrimeiroEscalaoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_primeiro_escalao_form_invalid(self):
        form_data = {
            'nome': '',
            'secretaria': 'Secretaria de Tecnologia',
            'cargo': 'Gerente',
            'email': 'email_invalido',
            'telefone': '(81) 99999-9999',
            'problema_urgente': '',
        }
        form = PrimeiroEscalaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('problema_urgente', form.errors)


class RedeTransformacaoDigitalFormTests(TestCase):

    def test_rede_transformacao_digital_form_valid(self):
        form_data = {
            'nome': 'Maria Oliveira',
            'secretaria': 'Secretaria de Desenvolvimento',
            'cargo': 'Coordenadora',
            'email': 'maria@example.com',
            'telefone': '(81) 98888-8888',
            'chefe_imediato': 'Carlos Souza, Diretor, (81) 97777-7777, carlos@example.com',
            'problema_urgente': 'Processos burocráticos atrasando as entregas.',
        }
        form = RedeTransformacaoDigitalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rede_transformacao_digital_form_invalid(self):
        form_data = {
            'nome': 'Maria Oliveira',
            'secretaria': 'Secretaria de Desenvolvimento',
            'cargo': 'Coordenadora',
            'email': 'email_invalido',
            'telefone': '(81) 98888-8888',
            'chefe_imediato': '',
            'problema_urgente': '',
        }
        form = RedeTransformacaoDigitalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('chefe_imediato', form.errors)
        self.assertIn('problema_urgente', form.errors)
