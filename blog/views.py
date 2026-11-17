# Versão 1: views funcionais, sem Django forms e sem validação de dados.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Post


def list_posts(request):
    post_list = Post.objects.order_by('-date')
    return render(request, 'blog/index.html', {'post_list': post_list})


def detail_post(request, pk):
    # Responde com 404 se o post não existir.
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})


def create_post(request):
    if request.method == 'POST':
        post = Post(
            title=request.POST['title'],
            content=request.POST['content'],
            date=timezone.now(),
        )
        post.save()
        return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))
    return render(request, 'blog/create.html', {})


def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))
    return render(request, 'blog/update.html', {'post': post})


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return HttpResponseRedirect(reverse('blog:index'))
    return render(request, 'blog/delete.html', {'post': post})
