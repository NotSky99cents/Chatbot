from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_output', views.get_output, name='get_output'),
]