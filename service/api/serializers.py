from rest_framework import serializers
from .models import Departamento, Usuario, Visitante, Scanner, HistorialAccesos


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'
        read_only_fields = ['iddepartamento', 'created_at']


class UsuarioSerializer(serializers.ModelSerializer):
    departamento_info = DepartamentoSerializer(source='iddepartamento', read_only=True)
    
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ['idusuario', 'created_at', 'updated_at']


class VisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitante
        fields = '__all__'
        read_only_fields = ['idvisitante', 'created_at']


class ScannerSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioSerializer(source='idusuario', read_only=True)
    visitante_info = VisitanteSerializer(source='idvisitante', read_only=True)
    
    class Meta:
        model = Scanner
        fields = '__all__'
        read_only_fields = ['idscanner', 'fecha']


class HistorialAccesosSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioSerializer(source='idusuario', read_only=True)
    visitante_info = VisitanteSerializer(source='idvisitante', read_only=True)
    scanner_info = ScannerSerializer(source='idscanner', read_only=True)
    
    class Meta:
        model = HistorialAccesos
        fields = '__all__'
        read_only_fields = ['idhistorial', 'created_at']
