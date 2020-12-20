from django.urls import path, include
from gestao import views

app_name = 'gestao'

urlpatterns = [
    path('sair/', views.sair, name='sair'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('municipio/<ibge>', views.busca_municipio),

    path(r'estabelecimentos/', include([
        path('', views.estabelecimentos, name='estabelecimentos'),
        path('<int:pk>', views.detalhar_estabelecimento, name='detalhar_estabelecimento'),
        path('<int:pk>/editar/', views.editar_estabelecimento, name='editar_estabelecimento'),
        path('cadastrar/', views.cadastrar_estabelecimento, name='cadastrar_estabelecimento'),
        path('<int:pk>/habilitar_prestador', views.habilitar_prestador, name='habilitar_prestador'),
        path('<int:pk>/adicionar_profissional/', views.adicionar_profissional, name='adicionar_profissional'),
        path('<int:estabelecimento_pk>/desabilitar_profissional/<int:profissional_pk>', views.desabilitar_profissional, name='desabilitar_profissional'),
        path('<int:estabelecimento_pk>/habilitar_profissional/<int:profissional_pk>', views.habilitar_profissional, name='habilitar_profissional'),
        path('<int:pk>/gestao_vacinas', views.gestao_vacinas, name='gestao_vacinas'),
        path('<int:estabelecimento_pk>/gestao_vacinas/cadastrar_estoque/<int:campanha_pk>/', views.cadastrar_estoque, name='cadastrar_estoque'),
        path('<int:pk>/agendamentos', views.agendamentos, name='agendamentos'),
        path('<int:estabelecimento_pk>/agendamentos/cadastrar/<int:campanha_pk>/', views.cadastrar_agendamentos, name='cadastrar_agendamentos'),
    ])),
    
    path(r'coordenadores_sus/', include([
        path('', views.coordenadores_sus, name='coordenadores_sus'),
        path('adicionar/', views.adicionar_coordenador_sus, name='adicionar_coordenador_sus'),
        path('desabilitar_coordenador/<int:coordenador_pk>', views.desabilitar_coordenador, name='desabilitar_coordenador'),
        path('habilitar_coordenador/<int:coordenador_pk>', views.habilitar_coordenador, name='habilitar_coordenador'),        

    ])),
]
