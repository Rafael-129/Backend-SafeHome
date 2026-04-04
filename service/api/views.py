from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from datetime import date, datetime

from .models import Departamento, Usuario, Visitante, Scanner, HistorialAccesos
from .serializers import (
    DepartamentoSerializer, 
    UsuarioSerializer, 
    VisitanteSerializer, 
    ScannerSerializer, 
    HistorialAccesosSerializer
)


@api_view(['GET'])
def api_root(request):
    """
    Vista raíz de la API que devuelve información básica
    """
    return Response({
        'message': 'Bienvenido a la API de SafeHome',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'departamentos': '/api/departamentos/',
            'usuarios': '/api/usuarios/',
            'visitantes': '/api/visitantes/',
            'scanner': '/api/scanner/',
            'historial': '/api/historial/',
            'historial_estadisticas': '/api/historial/estadisticas/?desde=YYYY-MM-DD&hasta=YYYY-MM-DD',
            'health': '/api/health/',
        }
    })


@api_view(['GET'])
def health_check(request):
    """
    Endpoint para verificar el estado del servidor
    """
    return Response({
        'status': 'ok',
        'message': 'API funcionando correctamente'
    }, status=status.HTTP_200_OK)


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar departamentos
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['torre', 'piso', 'numero']
    search_fields = ['codigo', 'torre']
    ordering_fields = ['torre', 'piso', 'numero']
    ordering = ['torre', 'piso', 'numero']


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios/residentes
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['iddepartamento', 'dni']
    search_fields = ['nombre', 'apellido', 'dni', 'correo']
    ordering_fields = ['nombre', 'apellido', 'dni']
    ordering = ['nombre', 'apellido']

    @action(detail=False, methods=['get'])
    def buscar_por_dni(self, request):
        """Buscar usuario por DNI"""
        dni = request.query_params.get('dni', None)
        if dni:
            try:
                usuario = Usuario.objects.get(dni=dni)
                serializer = self.get_serializer(usuario)
                return Response(serializer.data)
            except Usuario.DoesNotExist:
                return Response(
                    {'error': 'Usuario no encontrado'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'DNI no proporcionado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class VisitanteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar visitantes
    """
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dni', 'iddepartamento', 'fecha_visita']
    search_fields = ['nombre', 'apellido', 'dni', 'motivo']
    ordering_fields = ['nombre', 'apellido', 'fecha_visita']
    ordering = ['-fecha_visita']

    @action(detail=False, methods=['get'])
    def hoy(self, request):
        """Obtener visitantes de hoy"""
        hoy = date.today()
        visitantes = self.queryset.filter(fecha_visita=hoy)
        serializer = self.get_serializer(visitantes, many=True)
        return Response(serializer.data)


class ScannerViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar escaneos
    """
    queryset = Scanner.objects.all()
    serializer_class = ScannerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_persona', 'idusuario', 'idvisitante']
    search_fields = ['tipo_persona']
    ordering_fields = ['fecha']
    ordering = ['-fecha']

    @action(detail=False, methods=['get'])
    def recientes(self, request):
        """Obtener los escaneos más recientes (últimos 50)"""
        escaneos = self.queryset.all()[:50]
        serializer = self.get_serializer(escaneos, many=True)
        return Response(serializer.data)


class HistorialAccesosViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar historial de accesos
    """
    queryset = HistorialAccesos.objects.select_related('idusuario', 'idvisitante', 'idusuario__iddepartamento', 'idvisitante__iddepartamento').all()
    serializer_class = HistorialAccesosSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'fecha_entrada', 'idusuario', 'idvisitante']
    search_fields = ['estado']
    ordering_fields = ['fecha_entrada', 'hora_entrada']
    ordering = ['-fecha_entrada', '-hora_entrada']

    @action(detail=False, methods=['get'])
    def hoy(self, request):
        """Obtener accesos de hoy"""
        hoy = date.today()
        accesos = self.queryset.filter(fecha_entrada=hoy)
        serializer = self.get_serializer(accesos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtener accesos activos (sin hora de salida)"""
        accesos = self.queryset.filter(hora_salida__isnull=True, estado='Permitido')
        serializer = self.get_serializer(accesos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtener estadísticas de accesos en un rango de fechas."""
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')

        qs = self.queryset
        try:
            if desde:
                qs = qs.filter(fecha_entrada__gte=datetime.strptime(desde, '%Y-%m-%d').date())
            if hasta:
                qs = qs.filter(fecha_entrada__lte=datetime.strptime(hasta, '%Y-%m-%d').date())
        except ValueError:
            return Response(
                {'error': 'Formato de fecha inválido. Use YYYY-MM-DD en desde/hasta.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total = qs.count()
        autorizados = qs.filter(estado='Permitido').count()
        denegados = qs.filter(estado='Denegado').count()
        residentes = qs.filter(idusuario__isnull=False).count()
        visitantes = qs.filter(idvisitante__isnull=False).count()
        por_estado = list(qs.values('estado').annotate(total=Count('idhistorial')).order_by('estado'))

        return Response(
            {
                'totalAccesos': total,
                'autorizados': autorizados,
                'denegados': denegados,
                'residentes': residentes,
                'visitantes': visitantes,
                'porEstado': por_estado,
                'desde': desde,
                'hasta': hasta,
            },
            status=status.HTTP_200_OK,
        )
