#from django.conf.urls import url
from django.urls import path
from .views import ExercicioListView, ExercicioCreateView
from .views import ExercicioUpdateView, ExercicioDeleteView

urlpatterns = [
    path('list/', ExercicioListView.as_view(), name='exercicio_list'),
    path('cad/', ExercicioCreateView.as_view(), name='exercicio_create'),
    path('<slug:slug>/', ExercicioUpdateView.as_view(), name='exercicio_update'),
    path('<slug:slug>/delete/', ExercicioDeleteView.as_view(), name='exercicio_delete'),
]
