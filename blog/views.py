from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import CommentForm, PostForm
from .models import Post


# ---------------------------------------------------------------- Posts ---

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Comentários do post, do mais recente para o mais antigo.
        context['comments'] = self.object.comments.order_by('-date')
        context['comment_form'] = CommentForm(initial=self._initial_author())
        return context

    def _initial_author(self):
        user = self.request.user
        return {'author': user.pk} if user.is_authenticated else {}


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


# ---------------------------------------------------------- Comentários ---

def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog:detail', args=(post.id,)))
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['author'] = request.user.pk
        form = CommentForm(initial=initial)
    return render(request, 'blog/comment.html', {'form': form, 'post': post})
