#from django.conf.urls import url
from django.urls import path
from .views import RegistroAtividadeListView, RegistroAtividadeCreateView
from .views import RegistroAtividadeUpdateView, RegistroAtividadeDeleteView

urlpatterns = [
    path('list/', RegistroAtividadeListView.as_view(), name='registroatividade_list'),
    path('cad/', RegistroAtividadeCreateView.as_view(), name='registroatividade_create'),
    path('<slug:slug>/', RegistroAtividadeUpdateView.as_view(), name='registroatividade_update'),
    path('<slug:slug>/delete/', RegistroAtividadeDeleteView.as_view(), name='registroatividade_delete'),
]
