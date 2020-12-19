from django.urls import path, include
from agenda import views

app_name = 'agenda'

urlpatterns = [
    path('', views.index, name='index'),
    path('autocadastro/', views.autocadastro, name='autocadastro'),
    path('minhas_vacinas/<int:paciente_pk>', views.minhas_vacinas, name='minhas_vacinas'),
    path(r'campanhas/', include([
        path('', views.campanhas, name='campanhas'),
        path('<int:pk>', views.detalhar_campanha, name='detalhar_campanha'),
        path('<int:pk>/editar/', views.editar_campanha, name='editar_campanha'),
        path('cadastrar/', views.cadastrar_campanha, name='cadastrar_campanha'),
    ])),
]
