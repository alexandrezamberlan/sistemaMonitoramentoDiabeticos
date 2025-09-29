#from django.conf.urls import url
from django.urls import path
from .views import AlimentoListView, AlimentoCreateView
from .views import AlimentoUpdateView, AlimentoDeleteView

urlpatterns = [
    path('list/', AlimentoListView.as_view(), name='alimento_list'),
    path('cad/', AlimentoCreateView.as_view(), name='alimento_create'),
    path('<slug:slug>/', AlimentoUpdateView.as_view(), name='alimento_update'),
    path('<slug:slug>/delete/', AlimentoDeleteView.as_view(), name='alimento_delete'),
]
