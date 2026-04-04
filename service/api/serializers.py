from rest_framework import serializers
from .models import Departamento, Usuario, Visitante, Scanner, HistorialAccesos, PerfilAplicacion


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'
        read_only_fields = ['iddepartamento', 'created_at']


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ['idusuario']


class VisitanteSerializer(serializers.ModelSerializer):
    depart_visita = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = Visitante
        fields = [
            'idvisitante', 'nombre', 'apellido', 'dni', 'motivo', 'fecha_visita',
            'hora_visita', 'iddepartamento', 'acepta_foto', 'observacion_privacidad',
            'foto', 'depart_visita'
        ]
        read_only_fields = ['idvisitante']
        extra_kwargs = {
            'iddepartamento': {'required': False},
            'acepta_foto': {'required': False},
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

        # Si no acepta foto, no persistir imagen.
        if validated_data.get('acepta_foto') is False:
            validated_data['foto'] = None
            if not validated_data.get('observacion_privacidad'):
                validated_data['observacion_privacidad'] = 'Visitante no autoriza captura de foto.'
        
        return super().create(validated_data)


class PerfilAplicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilAplicacion
        fields = '__all__'
        read_only_fields = ['idperfil', 'updated_at']


class ScannerSerializer(serializers.ModelSerializer):
    usuario_info = serializers.SerializerMethodField()
    visitante_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Scanner
        fields = '__all__'
        read_only_fields = ['idscanner', 'fecha']

    def get_usuario_info(self, obj):
        if obj.idusuario:
            try:
                usuario = obj.idusuario
                return {
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'departamento': usuario.iddepartamento.codigo if usuario.iddepartamento else 'N/A'
                }
            except:
                return None
        return None

    def get_visitante_info(self, obj):
        if obj.idvisitante:
            try:
                visitante = obj.idvisitante
                return {
                    'nombre': visitante.nombre,
                    'apellido': visitante.apellido,
                    'depart_visita': visitante.iddepartamento.codigo if visitante.iddepartamento else 'N/A'
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
        read_only_fields = ['idhistorial']

    def get_usuario_info(self, obj):
        if obj.idusuario:
            try:
                usuario = obj.idusuario
                return {
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'departamento': usuario.iddepartamento.codigo if usuario.iddepartamento else 'N/A'
                }
            except Exception as e:
                print(f"Error obteniendo usuario_info: {e}")
                return None
        return None

    def get_visitante_info(self, obj):
        if obj.idvisitante:
            try:
                visitante = obj.idvisitante
                return {
                    'nombre': visitante.nombre,
                    'apellido': visitante.apellido,
                    'depart_visita': visitante.iddepartamento.codigo if visitante.iddepartamento else 'N/A'
                }
            except Exception as e:
                print(f"Error obteniendo visitante_info: {e}")
                return None
        return None

    def get_scanner_info(self, obj):
        if obj.idscanner:
            try:
                scanner = obj.idscanner
                return {
                    'tipo_persona': scanner.tipo_persona,
                    'fecha': scanner.fecha
                }
            except Exception as e:
                print(f"Error obteniendo scanner_info: {e}")
                return None
        return None
