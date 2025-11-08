from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('book/', views.book_room, name='book_room'),
    path('success/', views.success, name='success'),
    path('failed/', views.failed, name='failed'),
    path('contacts/', views.contacts, name='contacts'),
]
