## Medicar

Para rodar este projeto será necessário instalar primeiro o *pipenv* com o comando:    
```
$ pip install pipenv
```
Após feito isso, basta instalar as dependências do projeto com o comando:    
```
$ pipenv install
```
Concluída a instalação das dependências, é necessário criar as *"migrations"*:
```
$ pipenv run python manage.py makemigrations
```
Agora é necessário "popular" o banco de dados com estas *"migrações"*:
```
$ pipenv run python manage.py migrate
```
Com as tabelas do banco de dados criada, basta "subir" o servidor com:
```
$ pipenv run python manage.py runserver
```

Os seguintes endpoints foram criados:    
* */admin/*
* */especialidades/*
* */especialidades/post/*
* */especialidades/put/id*
* */especialidades/delete/id*


* */medicos/*
**/medicos/post/*
* */medicos/put/id*
* */medicos/delete/id*


* */consultas/*
* */consultas/post/*
* */consultas/put/id*
* */consultas/delete/id*


* */agendas/*
* */agendas/post/*
* */agendas/put/id*
* */agendas/delete/id*


* */login/*
* */cadastro/*