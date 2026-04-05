from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.posts_list, name='list'),
    path('new-post/', views.new_post, name='new-post'),
    path('<slug:slug>', views.post_page, name='page'),
    path('<slug:slug>/edit/', views.edit_post, name='edit'),
    path('<slug:slug>/delete/', views.delete_post, name='delete'),
    path('<slug:slug>/like/', views.like_post, name='like'),    
]