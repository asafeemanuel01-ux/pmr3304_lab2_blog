from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField('título', max_length=200)
    # O conteúdo é guardado como código HTML e renderizado com o filtro "safe".
    content = models.TextField('conteúdo (HTML)')
    date = models.DateTimeField('data de postagem', default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=(self.id,))


class Comment(models.Model):
    # O autor referencia o modelo de usuário do Django (settings.AUTH_USER_MODEL).
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='autor',
    )
    text = models.TextField('texto')
    date = models.DateTimeField('data de postagem', default=timezone.now)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='post',
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.author} em "{self.post}": {self.text[:40]}'


class Category(models.Model):
    name = models.CharField('nome', max_length=100)
    description = models.TextField('descrição', blank=True)
    # Um post pode estar em várias categorias e uma categoria tem vários posts.
    # O related_name permite acessar post.categories.all().
    posts = models.ManyToManyField(
        Post,
        related_name='categories',
        blank=True,
        verbose_name='posts',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', args=(self.id,))
