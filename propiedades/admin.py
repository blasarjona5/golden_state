from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from .models import Publicacion, ImagenPropiedad, PerfilAgente, ConsultaContacto
from .models import AgenteCorporativo

# ==============================================================================
# 👥 CONFIGURACIÓN PARA ACOPLAR EL WHATSAPP AL AGENTE (USUARIO)
# ==============================================================================

class PerfilAgenteInline(admin.StackedInline):
    model = PerfilAgente
    can_delete = False
    verbose_name_plural = 'Información de Contacto del Agente'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilAgenteInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Desescribimos el User nativo y registramos el nuestro con el Inline acoplado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registramos PerfilAgente de forma independiente para control rápido desde el menú lateral de Jazzmin
@admin.register(PerfilAgente)
class PerfilAgenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'whatsapp')
    search_fields = ('user__username', 'whatsapp')


# ==============================================================================
# 🏠 CONFIGURACIÓN DEL PANEL DE PROPIEDADES (LUXURY)
# ==============================================================================

class ImagenPropiedadInline(admin.TabularInline):
    model = ImagenPropiedad
    extra = 0  
    fields = ('imagen', 'orden')


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    # 🟢 CORRECCIÓN: Agregamos 'destacada_hero' al listado para visualizarlo a simple vista
    list_display = ('titulo', 'tipo_operacion', 'tipo_propiedad', 'precio_formateado', 'barrio_localidad', 'agente', 'destacada', 'destacada_hero', 'disponible', 'visitas', 'acciones_propiedad')
    
    # 🟢 CORRECCIÓN: Permitimos editar 'destacada' y 'destacada_hero' con switch rápido en la tabla principal
    list_editable = ('destacada', 'destacada_hero', 'disponible')
    
    # 🟢 CORRECCIÓN: Sumamos 'destacada_hero' a los filtros rápidos de la derecha
    list_filter = ('tipo_operacion', 'tipo_propiedad', 'moneda', 'disponible', 'destacada', 'destacada_hero', 'agente')
    
    # Buscador superior en tiempo real
    search_fields = ('titulo', 'direccion', 'barrio_localidad')
    
    # Campo de solo lectura para evitar que alteren las métricas de visitas a mano
    readonly_fields = ('visitas',)
    
    # Inyección de las múltiples imágenes en formato tabla
    inlines = [ImagenPropiedadInline]  

    # Estructura visual por bloques de tus formularios
    fieldsets = (
        ('Asignación de Propiedad', {
            'fields': ('agente',)
        }),
        ('Información Principal', {
            # 🟢 CORRECCIÓN: Incorporado al formulario de edición en el panel
            'fields': ('titulo', 'descripcion', 'tipo_propiedad', 'tipo_operacion', 'disponible', 'destacada', 'destacada_hero')
        }),
        ('Precios y Gastos', {
            'fields': (('moneda', 'precio'), 'expensas') 
        }),
        ('Distribución y Espacio', {
            'fields': (('ambientes', 'dormitorios', 'banos'), ('metros_cubiertos', 'metros_totales'))
        }),
        ('Ubicación Geográfica', {
            'fields': ('direccion', 'barrio_localidad', 'provincia', 'codigo_postal')
        }),
        ('Multimedia Principal', {
            'fields': ('imagen_principal',)
        }),
    )

    # 🔗 PANEL DE ACCIONES INTERACTIVAS (Ver en Web y Copiado rápido para WhatsApp)
    def acciones_propiedad(self, obj):
        if obj.id:
            # Captura la URL del detalle en el frontend
            url_frontend = reverse('propiedades:detalle', args=[obj.id])
            
            # Renderiza los dos botones con lógica de portapapeles nativa
            return format_html(
                """
                <div style="display: flex; gap: 6px; align-items: center;">
                    <a href="{0}" target="_blank" title="Ver propiedad en la Web"
                       style="background-color: #0a0a0b; color: #c9a84c; border: 1px solid #c9a84c; 
                              padding: 5px 9px; border-radius: 3px; text-decoration: none; 
                              font-weight: 600; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">
                        👁️ Ver
                    </a>
                    
                    <button type="button" title="Copiar enlace para mandar por WhatsApp"
                            onclick="navigator.clipboard.writeText(window.location.origin + '{0}').then(() => {{ 
                                let btn = this; 
                                let txt = btn.innerHTML; 
                                btn.innerHTML = '✅ Copiado'; 
                                btn.style.backgroundColor = '#1da851';
                                btn.style.color = '#ffffff';
                                setTimeout(() => {{ btn.innerHTML = txt; btn.style.backgroundColor = '#c9a84c'; btn.style.color = '#0a0a0b'; }}, 1500); 
                            }})"
                            style="background-color: #c9a84c; color: #0a0a0b; border: none;
                                   padding: 5px 9px; border-radius: 3px; cursor: pointer;
                                   font-weight: 600; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">
                        📋 Copiar Link
                    </button>
                </div>
                """,
                url_frontend
            )
        return "Falta ID"

    # Título de la columna en Jazzmin
    acciones_propiedad.short_description = 'Acciones de Broker'


# ==============================================================================
# ✉️ CONFIGURACIÓN DEL DESPACHO DE CONSULTAS PRIVADAS (EXCLUSIVO ADMINS)
# ==============================================================================

@admin.register(ConsultaContacto)
class ConsultaContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'interes', 'creado_el', 'leido')
    list_filter = ('leido', 'interes', 'creado_el')
    search_fields = ('nombre', 'email', 'mensaje', 'telefono')
    readonly_fields = ('creado_el',)
    actions = ['marcar_como_leidas']

    def marcar_como_leidas(self, request, queryset):
        filas_actualizadas = queryset.update(leido=True)
        if filas_actualizadas == 1:
            self.message_user(request, "1 consulta fue marcada como gestionada.")
        else:
            self.message_user(request, f"{filas_actualizadas} consultas fueron marcadas como gestionadas.")
            
    marcar_como_leidas.short_description = "🟢 Marcar consultas seleccionadas como LEÍDAS / GESTIONADAS"
    
    fieldsets = (
        ('Datos del Solicitante', {
            'fields': ('nombre', 'email', 'telefono')
        }),
        ('Detalles del Requerimiento', {
            'fields': ('interes', 'mensaje', 'creado_el')
        }),
        ('Control de Gestión', {
            'fields': ('leido',),
            'description': 'Tilde este campo una vez que se haya comunicado con el cliente.'
        }),
    )

@admin.register(AgenteCorporativo)
class AgenteCorporativoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'email', 'orden', 'disponible')
    list_filter = ('cargo', 'disponible')
    search_fields = ('nombre', 'email', 'biografia')
    list_editable = ('orden', 'disponible')  
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'cargo', 'foto', 'biografia')
        }),
        ('Contacto & Jerarquía', {
            'fields': ('email', 'orden', 'disponible')
        }),
    )