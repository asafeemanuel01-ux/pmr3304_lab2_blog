# Blog de Mecatrônica — Segunda entrega de laboratório (PMR3304)

Aplicação CRUD em Django 5.2: posts (criação, edição e remoção na própria
aplicação), comentários e categorias. Banco SQLite.

## Estrutura

```
config/                  configurações do projeto (settings, urls, wsgi)
templates/base.html      template base (pasta /templates)
blog/models.py           Post, Comment, Category
blog/views.py            views (versão final: classes genéricas)
blog/forms.py            PostForm, CommentForm
blog/urls.py             rotas com nomes (app_name = 'blog')
blog/templates/blog/     templates das páginas
blog/management/commands/popular_banco.py   dados da parte 4
sql/consultas.sql        queries da parte 4
build.sh                 script de build do Render
```

## Histórico Git

```
main ── v1 (views funcionais, sem forms) ── v2 (views funcionais + Django form)
     ── v3 (views genéricas) ── merge comments ── merge categories
             └── comments: modelo Comment + views
                              └── categories: modelo Category + views
```

Para ver: `git log --oneline --graph --all`

## Rodar localmente (Windows / PowerShell)

Requer Python 3.10 ou mais novo.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py popular_banco
python manage.py runserver
```

No Linux/macOS, ative com `source .venv/bin/activate`.

Acesse http://127.0.0.1:8000/ (blog) e http://127.0.0.1:8000/admin/ (administrador).

O `popular_banco` cria os usuários `ana`, `bruno` e `carla` (senha `pmr3304-blog`),
3 categorias, 3 posts e 5 comentários. Se precisar voltar o banco a esse estado,
rode `python manage.py popular_banco --reset`.

## URLs

| URL | View | Nome |
|---|---|---|
| `/` | listagem de posts | `blog:index` |
| `/<id>/` | post individual (404 se não existir) | `blog:detail` |
| `/create/` | criação de post | `blog:create` |
| `/update/<id>/` | edição de post | `blog:update` |
| `/delete/<id>/` | confirmação de remoção | `blog:delete` |
| `/<id>/comment/` | criação de comentário | `blog:comment` |
| `/categories/` | listagem de categorias | `blog:categories` |
| `/categories/<id>/` | categoria individual (404 se não existir) | `blog:category` |

## Deploy no Render

1. Suba o repositório no GitHub (com as três branches):
   ```
   git remote add origin https://github.com/<seu-usuario>/<repo>.git
   git push -u origin main comments categories
   ```
2. No Render: **New → Web Service**, conecte o repositório e preencha:
   - Runtime: `Python 3`
   - Build Command: `bash build.sh`
   - Start Command: `gunicorn config.wsgi:application`
   - Instance type: `Free`
3. Em **Environment**, adicione:
   - `SECRET_KEY` = (qualquer texto longo e aleatório)
   - `DEBUG` = `False`
   - `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`
4. Crie o serviço. O build roda as migrações, popula o banco e cria o superusuário.

Observação: no plano gratuito o disco do Render não é persistente; o que for
criado pela aplicação depois do deploy some quando o serviço reinicia, mas os
dados do `popular_banco` voltam a cada build.
