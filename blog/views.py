# Versão 2: views funcionais utilizando um Django form (com validação).
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import PostForm
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
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/update.html', {'post': post, 'form': form})


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return HttpResponseRedirect(reverse('blog:index'))
    return render(request, 'blog/delete.html', {'post': post})
