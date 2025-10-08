#from django.conf.urls import url
from django.urls import path
from .views import DadoClinicoListView, DadoClinicoCreateView
from .views import DadoClinicoUpdateView, DadoClinicoDeleteView

urlpatterns = [
    path('list/', DadoClinicoListView.as_view(), name='dadoclinico_list'),
    path('cad/', DadoClinicoCreateView.as_view(), name='dadoclinico_create'),
    path('<slug:slug>/', DadoClinicoUpdateView.as_view(), name='dadoclinico_update'),
    path('<slug:slug>/delete/', DadoClinicoDeleteView.as_view(), name='dadoclinico_delete'),
]
