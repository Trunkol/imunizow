from django.urls import path, include
from gestao import views

app_name = 'agenda'

urlpatterns = [
    path('/', views.index, name='index'),
]
