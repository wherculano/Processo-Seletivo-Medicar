# Model User
# Permission config
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class Especialidades(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    crm = models.IntegerField(null=False, blank=False)
    email = models.EmailField(max_length=50, null=True, blank=True)
    telefone = models.CharField(max_length=13, null=True, blank=True)
    especialidade = models.ForeignKey('Especialidades', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Consultas(models.Model):
    dia = models.DateField()
    horario = models.TimeField()
    data_agendamento = models.ForeignKey('Agendas', on_delete=models.CASCADE)
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dia)


class Agendas(models.Model):
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    dia = models.DateField(null=False, blank=False, unique=True)
    horarios = models.CharField(
        max_length=100, null=False, blank=False, help_text='HH:MM (Se houver mais de um horário, separar por vírgula)'
    )

    def set_horarios(self, horarios):
        self.horarios = horarios.replace(' ', '').split(',')

    def get_horarios(self):
        return self.horarios

    def __str__(self):
        return self.medico


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    """
    App api User class
    Email and password are required. Other fields are optional.
    """

    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_email(self):
        """
        Return the email.
        """
        email = '%s' % self.email
        return email.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_authtoken(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
