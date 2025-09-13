from django.urls import path
from . import views

urlpatterns = [
    path('', views.info, name='info'),           # стартовая страница
    path('rooms/', views.home, name='home'),     # список номеров
    path('book/', views.book_room, name='book_room'),
    path('success/', views.success, name='success'),
    path('failed/', views.failed, name='failed'),
    path('contacts/', views.contacts, name='contacts'),  # контакты
]
