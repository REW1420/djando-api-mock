
from django.urls import path

from . import views
# Nombre de la app, para usar {% url 'health:health' %} en templates
app_name = 'health'

urlpatterns = [
    path('', views.health, name='health'),
]
