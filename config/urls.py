"""
RUTAS PRINCIPALES DEL PROYECTO (equivale al "router" raíz de Express).

Aquí NO se definen las rutas de cada módulo, solo se "montan" las de cada app
con include(). Cada app tiene su propio urls.py con sus rutas.

Ejemplo:
    path('usuarios/', include('usuarios.urls'))
    -> todas las rutas de usuarios/urls.py quedan bajo /usuarios/
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Panel de administración de Django (/admin/)
    path('admin/', admin.site.urls),

    # Rutas de la app "usuarios"

    path('health/', include('health.urls')),
    path('auth/', include('auth.urls')),
    path('salas/', include('salas.urls'))
    # Cuando crees más apps, agrégalas aquí:
    # path('productos/', include('productos.urls')),
]
