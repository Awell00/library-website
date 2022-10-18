from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('livre/', views.livre, name='liste'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path('emprunts/', views.emprunts, name='emprunts'),
    path('retard/', views.retard, name='retard')
]
