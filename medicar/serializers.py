from rest_framework import serializers

from .models import Especialidades, Medico, Consultas, Agendas, User


class EspecialidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidades
        fields = ['id', 'nome']


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'nome', 'crm', 'email', 'telefone', 'especialidade']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['especialidade'] = EspecialidadesSerializer(instance.especialidade).data
        return rep


class ConsultasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultas
        fields = ['id', 'dia', 'horario', 'data_agendamento', 'medico']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['medico'] = MedicoSerializer(instance.medico).data
        return rep


class AgendasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendas
        fields = ['id', 'medico', 'dia', 'horarios']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['medico'] = MedicoSerializer(instance.medico).data
        return rep


class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
