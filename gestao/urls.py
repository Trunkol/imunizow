from django.urls import path, include
from gestao import views

app_name = 'gestao'

urlpatterns = [
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
    ])),

    
]
