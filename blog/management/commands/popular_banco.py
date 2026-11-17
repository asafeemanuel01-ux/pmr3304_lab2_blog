"""
Popula o banco com os dados mínimos pedidos na parte 4 do enunciado:

* 3 posts, sendo 1 sem comentários e 2 em múltiplas categorias;
* cada post comentado com 2 a 3 comentários;
* 3 categorias, com cada post em pelo menos uma.

Uso:
    python manage.py popular_banco           # só popula se ainda não houver posts
    python manage.py popular_banco --reset   # apaga posts/comentários/categorias e recria
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from blog.models import Category, Comment, Post

TZ = ZoneInfo('America/Sao_Paulo')


def quando(dia, hora, minuto=0):
    return datetime(2026, 11, dia, hora, minuto, tzinfo=TZ)


SENHA_USUARIOS = 'pmr3304-blog'

USUARIOS = [
    ('ana', 'Ana', 'Souza'),
    ('bruno', 'Bruno', 'Lima'),
    ('carla', 'Carla', 'Mendes'),
]

CATEGORIAS = [
    ('Programação', 'Desenvolvimento de software, frameworks e boas práticas.'),
    ('Automação', 'Controle, CLPs e modelagem de sistemas a eventos discretos.'),
    ('Manufatura', 'Processos de fabricação e máquinas-ferramenta.'),
]

POSTS = [
    {
        'title': 'Primeiros passos com Django',
        'date': quando(3, 10, 0),
        'categorias': ['Programação'],
        'content': (
            '<p>O <strong>Django</strong> é um framework web em Python que segue o padrão '
            '<em>Model-View-Template</em>. Com ele, boa parte do trabalho repetitivo de uma '
            'aplicação web (rotas, acesso ao banco, formulários e administração) já vem pronta.</p>'
            '<h3>Criando o projeto</h3>'
            '<pre><code>python -m venv .venv\n'
            'pip install django\n'
            'django-admin startproject config .\n'
            'python manage.py startapp blog</code></pre>'
            '<p>Depois disso basta definir os modelos, rodar <code>makemigrations</code> e '
            '<code>migrate</code>, e o administrador do Django já permite cadastrar dados.</p>'
        ),
        'comentarios': [
            ('ana', 'Ótimo resumo! O admin pronto economiza muito tempo.', quando(4, 9, 15)),
            ('bruno', 'Vale lembrar de ativar o ambiente virtual antes do pip install.', quando(5, 18, 40)),
            ('carla', 'Quais as diferenças entre views funcionais e genéricas?', quando(7, 21, 5)),
        ],
    },
    {
        'title': 'Redes de Petri na automação industrial',
        'date': quando(9, 14, 30),
        'categorias': ['Automação', 'Programação'],
        'content': (
            '<p>As <strong>redes de Petri</strong> são uma ferramenta gráfica e matemática para '
            'modelar sistemas a eventos discretos, como linhas de montagem e células de manufatura.</p>'
            '<ul>'
            '<li><strong>Lugares</strong> representam estados ou condições;</li>'
            '<li><strong>Transições</strong> representam eventos;</li>'
            '<li><strong>Fichas</strong> (marcas) indicam o estado atual do sistema.</li>'
            '</ul>'
            '<p>A partir do modelo é possível verificar propriedades como vivacidade e '
            'limitação antes de escrever o programa do CLP.</p>'
        ),
        'comentarios': [
            ('bruno', 'Usei isso para modelar uma estação de teste no CoDeSys, ajudou muito.', quando(10, 11, 0)),
            ('ana', 'Seria legal um post sobre a conversão da rede para Ladder.', quando(11, 16, 20)),
        ],
    },
    {
        'title': 'Do G-code à peça: como funciona um torno CNC',
        'date': quando(14, 9, 15),
        'categorias': ['Manufatura', 'Automação'],
        'content': (
            '<p>Um <strong>torno CNC</strong> transforma um programa em <em>G-code</em> em '
            'movimentos coordenados dos eixos da máquina.</p>'
            '<p>Comandos como <code>G00</code> (posicionamento rápido) e <code>G01</code> '
            '(interpolação linear) definem a trajetória da ferramenta, enquanto '
            '<code>M03</code> liga o eixo-árvore no sentido horário.</p>'
            '<p>O controlador lê o programa, calcula as trajetórias e envia os comandos aos '
            'acionamentos dos motores de passo ou servomotores.</p>'
        ),
        'comentarios': [],
    },
]


class Command(BaseCommand):
    help = 'Popula o banco com posts, comentários e categorias de exemplo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Apaga todos os posts, comentários e categorias antes de popular.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            Comment.objects.all().delete()
            Category.objects.all().delete()
            Post.objects.all().delete()
            self.stdout.write('Posts, comentários e categorias apagados.')
        elif Post.objects.exists():
            self.stdout.write(
                'O banco já tem posts; nada foi feito. Use --reset para recriar os dados.'
            )
            return

        User = get_user_model()
        usuarios = {}
        for username, nome, sobrenome in USUARIOS:
            user, criado = User.objects.get_or_create(
                username=username,
                defaults={'first_name': nome, 'last_name': sobrenome},
            )
            if criado:
                user.set_password(SENHA_USUARIOS)
                user.save()
            usuarios[username] = user

        categorias = {
            nome: Category.objects.create(name=nome, description=descricao)
            for nome, descricao in CATEGORIAS
        }

        for dados in POSTS:
            post = Post.objects.create(
                title=dados['title'],
                content=dados['content'],
                date=dados['date'],
            )
            for nome in dados['categorias']:
                categorias[nome].posts.add(post)
            for username, texto, data in dados['comentarios']:
                Comment.objects.create(
                    post=post, author=usuarios[username], text=texto, date=data
                )

        self.stdout.write(self.style.SUCCESS(
            f'Banco populado: {Post.objects.count()} posts, '
            f'{Comment.objects.count()} comentários, '
            f'{Category.objects.count()} categorias.'
        ))
