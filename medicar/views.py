from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from .serializers import (EspecialidadesSerializer, MedicoSerializer, ConsultasSerializer,
                          AgendasSerializer, CadastroSerializer)
from medicar.models import Especialidades, Medico, Consultas, Agendas, User


# Especialidade
class EspecialidadesViewSet(ModelViewSet):
    queryset = Especialidades.objects.all()
    serializer_class = EspecialidadesSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nome',)


# Medico
class MedicoViewSet(ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nome',)


# Cosultas
class ConsultasViewSet(ModelViewSet):
    queryset = Consultas.objects.all()
    serializer_class = ConsultasSerializer
    permission_classes = (IsAuthenticated, )


# Agendas
class AgendasViewSet(ModelViewSet):
    queryset = Agendas.objects.all()
    serializer_class = AgendasSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nome',)


# Cadastro
class CadastroViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CadastroSerializer
    http_method_names = ['post']

