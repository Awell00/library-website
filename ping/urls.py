from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path('emprunts/', views.emprunts, name='emprunts'),
    path('retard/', views.retard, name='retard')
]
