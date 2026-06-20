from django.urls import path
from . import views
from propiedades.views import servicios_view

app_name = 'propiedades'

urlpatterns = [
    path('', views.lista_propiedades, name='index'),
    path('catalogo/', views.catalogo_completo, name='catalogo'), # 🌟 Nueva ruta para ver todo
    path('propiedad/<int:pk>/', views.detalle_propiedad, name='detalle'),
    path('contacto/', views.contacto, name='contacto'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('servicios/', views.servicios_view, name='servicios'),
]