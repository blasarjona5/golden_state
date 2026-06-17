from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator

class Publicacion(models.Model):
    TIPOS_PROPIEDAD = (
        ("casa", "Casa"),
        ("departamento", "Departamento"),
        ("monoambiente", "Monoambiente"),
        ("ph", "PH"),
        ("loft", "Loft"),
        ("quinta", "Casa de Quinta / Barrio Cerrado"),
        ("terreno", "Terreno / Lote"),
        ("cochera", "Cochera"),
        ("local", "Local Comercial"),
        ("oficina", "Oficina"),
        ("galpon", "Galpón / Depósito"),
        ("campo", "Campo / Chacra"),
    )

    ESTADOS_OPERACION = (
        ("alquiler", "En Alquiler"),
        ("venta", "En Venta"),
        ("alquiler_temporal", "Alquiler Temporal"),
    )

    MONEDAS = (
        ("USD", "Dólares (USD)"),
        ("ARS", "Pesos (ARS)"),
    )

    agente = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Agente / Administrador")
    titulo = models.CharField(max_length=255, verbose_name="Título de la publicación")
    descripcion = models.TextField(verbose_name="Descripción o Detalles")
    tipo_propiedad = models.CharField(max_length=30, choices=TIPOS_PROPIEDAD, default="departamento", verbose_name="Tipo de Propiedad")
    tipo_operacion = models.CharField(max_length=20, choices=ESTADOS_OPERACION, default="venta", verbose_name="Operación")
    
    moneda = models.CharField(max_length=3, choices=MONEDAS, default="USD", verbose_name="Moneda")
    precio = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio")
    expensas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Expensas (0 si no aplica)", default=0)
    
    ambientes = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Ambientes")
    dormitorios = models.PositiveIntegerField(default=0, verbose_name="Dormitorios (0 si es monoambiente)")
    banos = models.PositiveIntegerField(default=1, verbose_name="Baños")
    metros_cubiertos = models.PositiveIntegerField(verbose_name="M² Cubiertos", blank=True, null=True)
    metros_totales = models.PositiveIntegerField(verbose_name="M² Totales")
    
    direccion = models.CharField(max_length=255, verbose_name="Dirección (Calle y Altura)")
    barrio_localidad = models.CharField(max_length=100, verbose_name="Barrio o Localidad")
    provincia = models.CharField(max_length=100, verbose_name="Provincia", default="Buenos Aires")
    codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal", blank=True, null=True)
    
    imagen_principal = models.ImageField(upload_to='propiedades/', verbose_name="Foto Principal", null=True, blank=True)
    
    visitas = models.PositiveIntegerField(default=0, editable=False, verbose_name="Cantidad de Visitas")
    disponible = models.BooleanField(default=True, verbose_name="Publicación Activa / Disponible")
    
    # Campo para la Home Exclusiva
    destacada = models.BooleanField(default=False, verbose_name="Propiedad Destacada (Sale en la Home)")
    
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"
        ordering = ['-creado_el']

    @property
    def precio_formateado(self):
        return f"{self.moneda} {self.precio:,.0f}".replace(",", ".")

    def __str__(self):
        return f"{self.titulo} - {self.tipo_operacion.upper()} ({self.precio_formateado})"


class ImagenPropiedad(models.Model):
    propiedad = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to='propiedades/galeria/', verbose_name="Foto")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Foto de la Propiedad"
        verbose_name_plural = "Galería de Fotos"
        ordering = ['orden']


# 🌟 AQUÍ ESTÁ EL MODELO QUE FALTA: Asegurate de que se guarde bien
class PerfilAgente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil", verbose_name="Usuario")
    whatsapp = models.CharField(
        max_length=20, 
        verbose_name="WhatsApp del Agente",
        help_text="Número completo: código de país + área sin el 15. Ej: 549116543210"
    )

    class Meta:
        verbose_name = "Perfil de Agente"
        verbose_name_plural = "Perfiles de Agentes"

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"
    # 🏛️ SISTEMA DE LEADS / CONSULTAS DE CONTACTO PREMIUM
class ConsultaContacto(models.Model):
    # Usamos exactamente las opciones lógicas que se corresponden con el formulario
    OPCIONES_INTERES = (
        ("adquisicion", "Adquisición Residencial Premium"),
        ("corporativo", "Búsqueda Corporativa / Comercial"),
        ("tasacion", "Tasación de Portafolio"),
    )

    nombre = models.CharField(max_length=150, verbose_name="Nombre Ilustre")
    email = models.EmailField(verbose_name="Dirección de Email Privada")
    telefono = models.CharField(max_length=30, blank=True, null=True, verbose_name="Teléfono / WhatsApp (Opcional)")
    interes = models.CharField(
        max_length=20, 
        choices=OPCIONES_INTERES, 
        default="adquisicion", 
        verbose_name="Tipo de Inversión"
    )
    mensaje = models.TextField(verbose_name="Detalles de su Requerimiento Inmobiliario")
    
    # Métricas de control para los administradores
    leido = models.BooleanField(default=False, verbose_name="¿Gestionado / Leído?")
    creado_el = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Recepción")

    class Meta:
        verbose_name = "Consulta de Contacto"
        verbose_name_plural = "Consultas de Asuntos Privados"
        ordering = ['-creado_el'] # Las consultas más nuevas aparecen arriba de todo

    def __str__(self):
        return f"Consulta de {self.nombre} - Interés: {self.get_interes_display()}"

class AgenteCorporativo(models.Model):
    # Definimos las posiciones posibles para el staff
    POSICIONES_CHOICES = [
        ('FOUNDER', 'Founder'),
        ('CEO', 'Ceo'),
        ('AGENTE', 'Agente'),
    ]

    nombre = models.CharField(max_length=100, help_text="Nombre completo del agente.")
    cargo = models.CharField(
        max_length=50, 
        choices=POSICIONES_CHOICES,
        default='AGENTE',
        help_text="Cargo o posición exclusiva en la firma."
    )
    foto = models.ImageField(
        upload_to='staff/', 
        help_text="Foto de perfil profesional (recomendado formato vertical)."
    )
    biografia = models.TextField(
        help_text="Breve reseña sobre su trayectoria y especialidad en el mercado premium."
    )
    email = models.EmailField(help_text="Correo electrónico de contacto profesional.")
    orden = models.PositiveIntegerField(
        default=0, 
        help_text="Número para ordenar la aparición en la web (menor número primero)."
    )
    disponible = models.BooleanField(
        default=True, 
        help_text="Tilda para mostrar u ocultar al agente en la web pública."
    )
    fecha_incorporacion = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Agente Corporativo"
        verbose_name_plural = "Nuestro Staff Exclusivo"
        ordering = ['orden', 'fecha_incorporacion']  # Ordenamos por jerarquía definida y luego por antigüedad

    def __str__(self):
        return f"{self.nombre} - {self.get_cargo_display()}"