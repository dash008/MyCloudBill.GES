from django.db.models.signals import pre_migrate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission
from django.conf import settings
from django.dispatch import receiver


# custom user related permissions
@receiver(pre_migrate, sender=auth_models)
def add_user_permissions(sender, **kwargs):
	content_type = ContentType.objects.get_for_model(settings.AUTH_USER_MODEL)
	Permission.objects.get_or_create(codename='ver_registro_solicitud', name='Ver Registro Solicitud', content_type=content_type)
    	#Permission.objects.get_or_create(codename='cambiar_estado_solicitudes', name='Cambiar Estado Solicitud', content_type=content_type)