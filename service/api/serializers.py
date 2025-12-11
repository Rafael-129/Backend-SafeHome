from rest_framework import serializers
from .models import Departamento, Usuario, Visitante, Scanner, HistorialAccesos


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'
        read_only_fields = ['iddepartamento', 'created_at']


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ['idusuario', 'created_at', 'updated_at', 'id_usuario']


class VisitanteSerializer(serializers.ModelSerializer):
    depart_visita = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = Visitante
        fields = ['idvisitante', 'nombre', 'apellido', 'dni', 'motivo', 'fecha_visita', 'hora_visita', 'iddepartamento', 'foto', 'depart_visita']
        read_only_fields = ['idvisitante']
        extra_kwargs = {
            'iddepartamento': {'required': False}
        }
    
    def create(self, validated_data):
        # Si viene depart_visita (código), buscar el departamento por código
        depart_codigo = validated_data.pop('depart_visita', None)
        if depart_codigo:
            try:
                departamento = Departamento.objects.get(codigo=depart_codigo)
                validated_data['iddepartamento'] = departamento
            except Departamento.DoesNotExist:
                raise serializers.ValidationError({'depart_visita': f'Departamento {depart_codigo} no existe'})
        
        # Validar que iddepartamento esté presente
        if 'iddepartamento' not in validated_data:
            raise serializers.ValidationError({'depart_visita': 'Debe proporcionar un departamento'})
        
        return super().create(validated_data)


class ScannerSerializer(serializers.ModelSerializer):
    usuario_info = serializers.SerializerMethodField()
    visitante_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Scanner
        fields = '__all__'
        read_only_fields = ['idscanner', 'fecha', 'id_scanner']

    def get_usuario_info(self, obj):
        if obj.idusuario:
            try:
                from .models import Usuario
                usuario = Usuario.objects.get(idusuario=obj.idusuario)
                return {
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'departamento': usuario.departamento
                }
            except:
                return None
        return None

    def get_visitante_info(self, obj):
        if obj.idvisitante:
            try:
                from .models import Visitante
                visitante = Visitante.objects.get(idvisitante=obj.idvisitante)
                return {
                    'nombre': visitante.nombre,
                    'apellido': visitante.apellido,
                    'depart_visita': visitante.depart_visita
                }
            except:
                return None
        return None


class HistorialAccesosSerializer(serializers.ModelSerializer):
    usuario_info = serializers.SerializerMethodField()
    visitante_info = serializers.SerializerMethodField()
    scanner_info = serializers.SerializerMethodField()
    
    class Meta:
        model = HistorialAccesos
        fields = '__all__'
        read_only_fields = ['idhistorial', 'created_at', 'id_historial']

    def get_usuario_info(self, obj):
        if obj.idusuario:
            try:
                from .models import Usuario
                usuario = Usuario.objects.get(idusuario=obj.idusuario)
                return {
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'departamento': usuario.departamento
                }
            except:
                return None
        return None

    def get_visitante_info(self, obj):
        if obj.idvisitante:
            try:
                from .models import Visitante
                visitante = Visitante.objects.get(idvisitante=obj.idvisitante)
                return {
                    'nombre': visitante.nombre,
                    'apellido': visitante.apellido,
                    'depart_visita': visitante.depart_visita
                }
            except:
                return None
        return None

    def get_scanner_info(self, obj):
        if obj.idscanner:
            try:
                from .models import Scanner
                scanner = Scanner.objects.get(idscanner=obj.idscanner)
                return {
                    'tipo_persona': scanner.tipo_persona,
                    'fecha': scanner.fecha
                }
            except:
                return None
        return None
