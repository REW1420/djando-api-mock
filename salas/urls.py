from django.urls import path

from . import views
app_name = 'salas'

urlpatterns = [
    path('', views.get_salas, name='get_salas'),
    path('create', views.create_sala_view, name='create_sala'),
    path('<int:sala_id>', views.get_sala_view, name='get_sala'),
    path('<int:sala_id>/delete', views.delete_sala_view, name='delete_sala'),
]
