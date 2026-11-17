# Versão 3: views com as classes genéricas do Django.
from django.urls import reverse_lazy
from django.views import generic

from .forms import PostForm
from .models import Post


class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    ordering = ['-date']


class PostDetailView(generic.DetailView):
    # DetailView já responde com 404 se o post não existir.
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class PostCreateView(generic.CreateView):
    # Após salvar, redireciona para Post.get_absolute_url().
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update.html'
    context_object_name = 'post'


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:index')
