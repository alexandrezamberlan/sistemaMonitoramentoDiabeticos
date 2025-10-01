#from django.conf.urls import url
from django.urls import path
from .views import MedicamentoListView, MedicamentoCreateView
from .views import MedicamentoUpdateView, MedicamentoDeleteView

urlpatterns = [
    path('list/', MedicamentoListView.as_view(), name='medicamento_list'),
    path('cad/', MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('<slug:slug>/', MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('<slug:slug>/delete/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),
]
