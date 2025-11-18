from django.contrib import admin
from .models import Departamento, Usuario, Visitante, Scanner, HistorialAccesos


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['iddepartamento', 'codigo', 'torre', 'piso', 'numero', 'habitaciones', 'estacionamientos']
    list_filter = ['torre', 'piso']
    search_fields = ['codigo', 'torre']
    ordering = ['torre', 'piso', 'numero']


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['idusuario', 'nombre', 'apellido', 'dni', 'correo', 'departamento', 'created_at']
    list_filter = ['departamento', 'created_at']
    search_fields = ['nombre', 'apellido', 'dni', 'correo']
    ordering = ['-created_at']


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ['idvisitante', 'nombre', 'apellido', 'dni', 'depart_visita', 'fecha_visita', 'hora_visita']
    list_filter = ['depart_visita', 'fecha_visita']
    search_fields = ['nombre', 'apellido', 'dni', 'motivo']
    ordering = ['-created_at']


@admin.register(Scanner)
class ScannerAdmin(admin.ModelAdmin):
    list_display = ['idscanner', 'tipo_persona', 'idusuario', 'idvisitante', 'fecha']
    list_filter = ['tipo_persona', 'fecha']
    search_fields = ['tipo_persona']
    ordering = ['-fecha']


@admin.register(HistorialAccesos)
class HistorialAccesosAdmin(admin.ModelAdmin):
    list_display = ['idhistorial', 'get_persona', 'fecha_entrada', 'hora_entrada', 'hora_salida', 'estado']
    list_filter = ['estado', 'fecha_entrada']
    search_fields = ['estado']
    ordering = ['-fecha_entrada', '-hora_entrada']

    def get_persona(self, obj):
        if obj.idusuario:
            return f"Usuario: {obj.idusuario.nombre} {obj.idusuario.apellido}"
        elif obj.idvisitante:
            return f"Visitante: {obj.idvisitante.nombre} {obj.idvisitante.apellido}"
        return "N/A"
    get_persona.short_description = 'Persona'
