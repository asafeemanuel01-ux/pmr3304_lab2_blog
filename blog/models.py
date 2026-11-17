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
