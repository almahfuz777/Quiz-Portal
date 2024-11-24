from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),  
    path('create/', views.create_blog, name='create_blog'),  
    path('<int:id>/', views.blog_detail, name='blog_detail'),  
]
