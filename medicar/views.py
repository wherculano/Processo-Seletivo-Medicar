# Models Especialidades, Medico, Consultas, Agendas
from datetime import datetime

from rest_framework.decorators import api_view, permission_classes  # , authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from django.utils.timezone import now
from .serializers import (EspecialidadesSerializer, MedicoSerializer, ConsultasSerializer,
                          AgendasSerializer, CadastroSerializer)
from medicar.models import Especialidades, Medico, Consultas, Agendas


# Especialidade
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_especialidades(request):
    especialidades = Especialidades.objects.all()
    serializer = EspecialidadesSerializer(especialidades, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_especialidades(request):
    serializer = EspecialidadesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_especialidades(request, pk):
    especialidades = Especialidades.objects.get(id=pk)
    serializer = EspecialidadesSerializer(especialidades, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_especialidades(request, pk):
    especialidades = Especialidades.objects.get(id=pk)
    especialidades.delete()
    message = {'message': f'Especialidade {especialidades} excluída!'}
    return Response(message)


# Medico
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medico(request):
    medico = Medico.objects.all()
    serializer = MedicoSerializer(medico, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_medico(request):
    serializer = MedicoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_medico(request, pk):
    medico = Medico.objects.get(id=pk)
    serializer = MedicoSerializer(medico, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medico(request, pk):
    medico = Medico.objects.get(id=pk)
    medico.delete()
    message = {"message": f"Medico {medico} excluído!"}
    return Response(message)


# Cosultas
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_consultas(request):
    consultas = Consultas.objects.all().filter(dia__gte=now().date())
    serializer = ConsultasSerializer(consultas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_consultas(request):
    serializer = ConsultasSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_consultas(request, pk):
    consultas = Consultas.objects.get(id=pk)
    serializer = ConsultasSerializer(consultas, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['DELTE'])
@permission_classes([IsAuthenticated])
def delete_consultas(request, pk):
    consultas = Consultas.objects.get(id=pk)
    consultas.delete()
    message = {"message": f"Consulta {consultas} excluida!"}
    return Response(message)


# Agendas
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_agendas(request):
    agendas = Agendas.objects.all()
    serializer = AgendasSerializer(agendas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_agendas(request):
    if datetime.strptime(request.data['dia'], '%Y-%m-%d').date() < now().date():
        return Response({"erro": "Data anterior ao dia atual!"})

    serializer = AgendasSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_agendas(request, pk):
    agendas = Agendas.objects.get(id=pk)
    serializer = AgendasSerializer(agendas, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['DELTE'])
@permission_classes([IsAuthenticated])
def delete_agendas(request, pk):
    agendas = Agendas.objects.get(id=pk)
    agendas.delete()
    message = {"message": f"Agenda {agendas} excluída!"}
    return Response(message)


# Cadastro
@api_view(['POST'])
def cadastro(request):
    if request.method == 'POST':
        serializer = CadastroSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Cadastro efetuado com sucesso!'
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


# ListViews
class EspecialidadesListView(ListAPIView):
    queryset = Especialidades.objects.all()
    serializer_class = EspecialidadesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nome',)


class MedicoListView(ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('nome', 'especialidade')

#
# class ConsultasListView(ListAPIView):
#     queryset = Consultas.objects.all()
#     serializer_class = ConsultasSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     filter_backends = ('dia', 'horario')
#     ordering_fields = ['dia', 'horario']
#
#
# class AgendasListView(ListAPIView):
#     queryset = Agendas.objects.all()
#     serializer_class = AgendasSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     filter_backends = ('dia', 'horario', 'medico', 'especialidade')
#     ordering_fields = ['dia']
