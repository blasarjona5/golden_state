from django.shortcuts import render, get_object_or_404
from .models import Publicacion
from django.shortcuts import render
from django.contrib import messages
from .models import ConsultaContacto
from .models import AgenteCorporativo

def lista_propiedades(request):
    """Muestra la Home de AURUM Estates únicamente con las Destacadas"""
    propiedades_destacadas = Publicacion.objects.filter(disponible=True, destacada=True)[:5]
    contexto = {'propiedades': propiedades_destacadas}
    return render(request, 'propiedades/index.html', contexto)


def catalogo_completo(request):
    """Muestra el archivo propiedades.html con TODO el catálogo y sus filtros activos"""
    propiedades = Publicacion.objects.filter(disponible=True)
    
    # Captura de filtros desde la barra de Aurum
    tipo_operacion = request.GET.get('operacion')
    tipo_propiedad = request.GET.get('tipo')
    barrio = request.GET.get('barrio')

    if tipo_operacion:
        propiedades = propiedades.filter(tipo_operacion=tipo_operacion)
    if tipo_propiedad:
        propiedades = propiedades.filter(tipo_propiedad=tipo_propiedad)
    if barrio:
        propiedades = propiedades.filter(barrio_localidad__icontains=barrio)

    contexto = {'propiedades': propiedades}
    return render(request, 'propiedades/propiedades.html', contexto)


def detalle_propiedad(request, pk):
    """Muestra la ficha técnica interactiva de la propiedad (Fusión Luxury)"""
    propiedad = get_object_or_404(Publicacion, pk=pk)
    
    # Métricas automatizadas
    propiedad.visitas += 1
    propiedad.save()

    contexto = {'propiedad': propiedad}
    return render(request, 'propiedades/detalle.html', contexto)



def contacto(request):
    """Procesa el formulario seguro de Golden State y lo inyecta al Admin"""
    if request.method == 'POST':
        # 🔌 Capturamos los valores exactos mediante el atributo 'name' del HTML
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        interes = request.POST.get('interes')
        mensaje = request.POST.get('mensaje')

        # Combinamos Nombre + Apellido para que guarde limpio en el modelo
        nombre_completo = f"{nombre} {apellido}".strip()

        # Validación obligatoria de seguridad en Backend
        if nombre and email and mensaje and interes:
            # 💾 Insertamos la nueva fila directamente en la base de datos
            ConsultaContacto.objects.create(
                nombre=nombre_completo,
                email=email,
                telefono=telefono,
                interes=interes,
                mensaje=mensaje
            )
            
            # 🔥 Disparamos la notificación de éxito nativa para el HTML
            messages.success(request, "Su solicitud privada ha sido procesada con éxito. Un broker se contactará en la brevedad.")
        else:
            messages.error(request, "Error de validación: Por favor complete los pliegos requeridos.")

    # Si es GET (o después de procesar), renderiza normal
    return render(request, 'propiedades/contacto.html')

def nosotros(request):
    # Recuperamos los agentes corporativos que están marcados como disponibles
    # Django los ordena automáticamente según la Meta clase de su modelo
    staff = AgenteCorporativo.objects.filter(disponible=True)

    context = {
        'staff': staff,  # Pasamos la lista de agentes al template
    }
    return render(request, 'propiedades/nosotros.html', context)