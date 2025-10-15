from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Gerenciador de usuário personalizado
class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        username = extra_fields.get('username', email)  
        extra_fields.setdefault('username', username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser precisa ter is_superuser=True')
        
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser precisa ter is_staff=True')
        
        return self._create_user(email, password, **extra_fields)

# Modelo de usuário personalizado
class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    nome_completo = models.CharField(max_length=255, blank=True, null=True)  # Nome completo
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Telefone opcional
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class InscricaoDesenvolvedor(models.Model):
    nome = models.CharField(verbose_name="Nome Completo", max_length=200)
    telefone = models.CharField(verbose_name="Telefone", max_length=20)
    email = models.EmailField(verbose_name="E-mail")
    unidade_secretaria = models.CharField(verbose_name="Unidade/Secretaria", max_length=200)
    chefia_imediata = models.CharField(verbose_name="Chefia Imediata", max_length=200)
    linguagem_ferramenta = models.CharField(verbose_name="Linguagem ou ferramenta que trabalha", max_length=255)
    principal_desafio = models.TextField(verbose_name="Principal desafio enfrentado nos projetos/trabalho")
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Inscrição de Desenvolvedor"
        verbose_name_plural = "Inscrições de Desenvolvedores"