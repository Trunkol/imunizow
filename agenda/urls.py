from django.urls import path, include
from agenda import views

app_name = 'agenda'

urlpatterns = [
    path('', views.index, name='index'),
    path('autocadastro/', views.autocadastro, name='autocadastro'),
]
