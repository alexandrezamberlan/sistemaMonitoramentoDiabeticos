from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    
    path('participante/', include('appmembro.urls')), 
    
    path('atestado_manual/', include('atestado_manual.urls')), 
    path('aviso/', include('aviso.urls')), 
    path('evento/', include('evento.urls')), 
    path('frequencia/', include('frequencia.urls')), 
    path('instituicao/', include('instituicao.urls')), 
    path('inscricao/', include('inscricao.urls')),
    path('relatorio/', include('relatorio.urls')), 
    path('tipo_evento/', include('tipo_evento.urls')), 
    path('usuario/', include('usuario.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),
]

#url para arquivos de media quando em desenvolvimento
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, 
    document_root = settings.STATIC_ROOT)   
