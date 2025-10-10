#from django.conf.urls import url
from django.urls import path
from .views import RegistroRefeicaoListView, RegistroRefeicaoCreateView
from .views import RegistroRefeicaoUpdateView, RegistroRefeicaoDeleteView

urlpatterns = [
    path('list/', RegistroRefeicaoListView.as_view(), name='registrorefeicao_list'),
    path('cad/', RegistroRefeicaoCreateView.as_view(), name='registrorefeicao_create'),
    path('<slug:slug>/', RegistroRefeicaoUpdateView.as_view(), name='registrorefeicao_update'),
    path('<slug:slug>/delete/', RegistroRefeicaoDeleteView.as_view(), name='registrorefeicao_delete'),
]
