from django.urls import path, include
from gestao import views

app_name = 'gestao'

urlpatterns = [
    path(r'estabelecimentos/', include([
        path('', views.estabelecimentos, name='estabelecimentos'),
        path('<int:pk>', views.detalhar_estabelecimento, name='detalhar_estabelecimento'),
        path('<int:pk>/editar/', views.editar_estabelecimento, name='editar_estabelecimento'),
    ])),

    
]
