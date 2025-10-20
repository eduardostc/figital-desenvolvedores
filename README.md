Dependências
============
* Python version ^3.11.5
* Django version ^4.2.16

Requisitos
============
* Database: Banco de dados MySQL ou PostgreSQL (configurar .env)

Estrategia Figital
=============================

Desenvolvimento: [estrategia-figital.dev.app.emprel.gov.br][1]

Homologação: [estrategia-figital.homolog.app.emprel.gov.br][2]

Produção: [estrategia-figital.recife.pe.gov.br][3]

Configuração Ambiente Desenvolvimento
--------------

Para configurar o projeto em desenvolvimento, executar os comandos à baixo:

```bash
$ cd codigos\www\
```

```bash
$ pip install --no-cache-dir -r requirements.txt
```

```bash
$ python manage.py makemigrations figital
```

```bash
$ python manage.py migrate
```

```bash
$ python manage.py runserver
```

[1]:  https://estrategia-figital.dev.app.emprel.gov.br
[2]:  https://estrategia-figital.homolog.app.emprel.gov.br
[3]:  https://estrategia-figital.recife.pe.gov.br
