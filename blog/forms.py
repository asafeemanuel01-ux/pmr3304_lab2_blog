from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': 'Título',
            'content': 'Conteúdo (HTML)',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 12}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        labels = {
            'author': 'Autor',
            'text': 'Comentário',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }
