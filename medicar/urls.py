from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

from .views import MedicoListView

urlpatterns = [
    path('especialidades/', views.get_especialidades, name='get_especialidades'),
    path('especialidades/post/', views.post_especialidades, name='post_especialidades'),
    path('especialidades/put/<str:pk>', views.put_especialidades, name='put_especialidades'),
    path('especialidades/delete/<str:pk>', views.delete_especialidades, name='delete_especialidades'),

    path('medicos/', views.get_medico, name='get_medicos'),
    path('medicos/post/', views.post_medico, name='post_medicos'),
    path('medicos/put/<str:pk>', views.put_medico, name='put_medicos'),
    path('medicos/delete/<str:pk>', views.delete_medico, name='delete_medicos'),

    path('consultas/', views.get_consultas, name='get_cosultas'),
    path('consultas/post/', views.post_consultas, name='post_cosultas'),
    path('consultas/put/<str:pk>', views.put_consultas, name='put_cosultas'),
    path('consultas/delete/<str:pk>', views.delete_consultas, name='delete_cosultas'),

    path('agendas/', views.get_agendas, name='get_agendas'),
    path('agendas/post/', views.post_agendas, name='post_agendas'),
    path('agendas/put/<str:pk>', views.put_agendas, name='put_agendas'),
    path('agendas/delete/<str:pk>', views.delete_agendas, name='delete_agendas'),

    path('medicos/', MedicoListView.as_view(), name="medicos"),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('login/', obtain_auth_token, name="login"),
]
