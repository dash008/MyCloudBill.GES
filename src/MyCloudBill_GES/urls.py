from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin



urlpatterns = [
    # Examples:
    url(r'^$', 'django.contrib.auth.views.login' , name='home'),
    url(r'^about/$', 'MyCloudBill_GES.views.about', name = 'about'),
    url(r'^features/$', 'MyCloudBill_GES.views.features', name = 'features'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^controlpanel/$', 'MyCloudBill_GES.views.controlpanel', name = 'controlpanel'),
    url('', include('django.contrib.auth.urls')),
    #url(r'^register/$', 'MyCloudBill_GES.views.register', name='register'), # ADD NEW PATTERN!
    url(r'^logout/$', 'MyCloudBill_GES.views.logout', name='logout'),

    url(r'^registrosolicitud/$', 'MyCloudBill_GES.views.registrosolicitud', name='RegistroSolicitud'),
    url(r'^consultasolicitud/$', 'MyCloudBill_GES.views.consultasolicitud', name='ConsultaSolicitud'),
    url(r'^eliminarsolicitud/$', 'MyCloudBill_GES.views.eliminarsolicitud', name='EliminarSolicitud'),
    url(r'^modificarsolicitud/$', 'MyCloudBill_GES.views.modificarsolicitud', name='ModificarSolicitud'),

    
    url(r'^revisarfactura/$', 'MyCloudBill_GES.views.revisarfactura', name='RevisarFactura'),
    url(r'^registronegociacion/$', 'MyCloudBill_GES.views.registronegociacion', name='RegistroNegociacion'),

    url(r'^registrousuario/$', 'MyCloudBill_GES.views.registrousuario', name='RegistroUsuario'),

    url(r'^getFactura/$', 'MyCloudBill_GES.views.getFactura', name='GetFactura'),
    url(r'^nuevorecurso/$', 'MyCloudBill_GES.views.nuevorecurso', name='NuevosRecursos'),
    url(r'^registronegociacion/$', 'MyCloudBill_GES.views.registronegociacion', name='RegistroNegociacion'),
    url(r'^facturaenlineabase/$', 'MyCloudBill_GES.views.facturaenlineabase', name='FacturaEnLB'),
    url(r'^facturamensualestimada/$', 'MyCloudBill_GES.views.facturamensualestimada', name='FacturaEstimada'),
    url(r'^facturamensualreal/$', 'MyCloudBill_GES.views.facturamensualreal', name='FacturaReal'),
    

    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)