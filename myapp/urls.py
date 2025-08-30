from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Головна сторінка
    path('rooms/', views.room_list, name='room_list'),
    path('book/', views.book_room, name='book_room'),
    path('success/', views.success, name='success'),
]