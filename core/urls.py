from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Homepage URL
    path('dashboard/',views.dashboard,name='dashboard'),
    path('signup/',views.signup,name = 'signup'), # signup url
    path('verify/<uuid:token>/', views.verify, name='verify'),
    path('login/',views.user_login, name = 'login'),
    path('logout/',views.user_logout,name='logout')
]
