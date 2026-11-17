from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.list_posts, name='index'),
    path('<int:pk>/', views.detail_post, name='detail'),
    path('create/', views.create_post, name='create'),
    path('update/<int:pk>/', views.update_post, name='update'),
    path('delete/<int:pk>/', views.delete_post, name='delete'),
]
