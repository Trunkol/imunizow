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
    path(r'agendar_vacinacao/', include([
        path('<int:campanha_pk>/', views.agendar_vacinacao_estabelecimento, name='agendar_vacinacao_estabelecimento'),
        path('<int:campanha_pk>/<int:estabelecimento_pk>/', views.agendar_vacinacao_data, name='agendar_vacinacao_data'),
    ])),
    
    path(r'acompanhar_vacinacao/', include([
        path('<int:agendamento_pk>/fila/', views.fila, name='fila'),
    ])),
    
    path('<int:agendamento_pk>/confirmar_vacinacao/', views.confirmar_vacinacao, name='confirmar_vacinacao'),
    path('cadastrar_vacina_privada/', views.cadastrar_vacina_privada, name='cadastrar_vacina_privada')

]
