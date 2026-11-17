from django.contrib import admin

from .models import Category, Comment, Post


class CategoryInline(admin.TabularInline):
    """Permite escolher as categorias na própria tela de edição do post."""
    model = Category.posts.through
    extra = 1
    verbose_name = 'categoria'
    verbose_name_plural = 'categorias'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title', 'content')
    inlines = [CategoryInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date')
    list_filter = ('post',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('posts',)
