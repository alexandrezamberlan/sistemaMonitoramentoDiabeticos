from django.urls import path

from .views import AtestadoManualListView, AtestadoManualCreateView
from .views import AtestadoManualUpdateView, AtestadoManualDeleteView
from .views import AtestadoManualPdfView


urlpatterns = [
	path('list/', AtestadoManualListView.as_view(), name='atestado_manual_list'),
	path('cad/', AtestadoManualCreateView.as_view(), name='atestado_manual_create'),
	path('<slug:slug>/pdf/', AtestadoManualPdfView.as_view(), name='atestado_manual_pdf'),
	path('<slug:slug>/', AtestadoManualUpdateView.as_view(), name='atestado_manual_update'),
	path('<slug:slug>/delete/', AtestadoManualDeleteView.as_view(), name='atestado_manual_delete'), 
]
 