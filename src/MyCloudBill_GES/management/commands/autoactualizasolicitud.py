# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from MyCloudBill_GES.models import Solicitud
from time import sleep

class Command(BaseCommand):
    help = 'Cambiar el estado de los registros de acuerdo al tiempo especificado'
    def add_arguments(self, parser):
        # Argumento posicional
        parser.add_argument('tiempo',type=int)
        parser.add_argument('idsolicitud',type=int)


    def handle(self, *args, **options):
        tiempo = options['tiempo']
        id_sol = options['idsolicitud']
        solicitud = Solicitud.objects.get(pk=id_sol)
        if tiempo == 4:
            sleep(10)
            setattr(solicitud,"estado","EnUso")
            solicitud.save()
        elif tiempo == 6 and solicitud.estado == "EnUso":
            sleep(2628000)
            sleep(2628000)
            sleep(2628000)
            sleep(2628000)
            sleep(2628000)
            sleep(2628000)
            setattr(solicitud, "estado", "Liberado")
            solicitud.save()
        elif tiempo == 4 and solicitud.estado == "Liberado":
            sleep(14400)
            setattr(solicitud, "estado", "Contabilizado")
            solicitud.save()
        else:
            sleep(2628000)
            self.stdout.write("Error en la ejecucion del comando")
        self.stdout.write('¡Registros actualizados!')