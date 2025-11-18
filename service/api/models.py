from django.db import models


class Departamento(models.Model):
    iddepartamento = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20)
    torre = models.CharField(max_length=10)
    piso = models.IntegerField()
    numero = models.IntegerField()
    area_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    habitaciones = models.IntegerField(null=True, blank=True)
    banos = models.IntegerField(null=True, blank=True)
    estacionamientos = models.IntegerField(default=0)
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return f"{self.codigo} - Torre {self.torre}"


class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    correo = models.EmailField(max_length=150, null=True, blank=True)
    departamento = models.CharField(max_length=20)
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, db_column='iddepartamento')
    foto = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id_usuario = models.BigIntegerField()

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"


class Visitante(models.Model):
    idvisitante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    motivo = models.CharField(max_length=255, null=True, blank=True)
    fecha_visita = models.CharField(max_length=255)
    hora_visita = models.CharField(max_length=255)
    depart_visita = models.CharField(max_length=20)
    foto = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id_visitante = models.BigIntegerField()

    class Meta:
        db_table = 'visitante'
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"


class Scanner(models.Model):
    idscanner = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, db_column='idusuario', related_name='scanners_usuario')
    idvisitante = models.ForeignKey(Visitante, on_delete=models.SET_NULL, null=True, blank=True, db_column='idvisitante', related_name='scanners_visitante')
    foto_capturada = models.TextField(null=True, blank=True)
    tipo_persona = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    id_scanner = models.BigIntegerField()
    id_usuario = models.BigIntegerField(null=True, blank=True)
    id_visitante = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'scanner'
        verbose_name = 'Escaneo'
        verbose_name_plural = 'Escaneos'

    def __str__(self):
        return f"Scanner {self.idscanner} - {self.tipo_persona}"


class HistorialAccesos(models.Model):
    ESTADOS = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('pendiente', 'Pendiente'),
    ]

    idhistorial = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, db_column='idusuario', related_name='historial_accesos')
    idvisitante = models.ForeignKey(Visitante, on_delete=models.SET_NULL, null=True, blank=True, db_column='idvisitante', related_name='historial_visitas')
    idscanner = models.ForeignKey(Scanner, on_delete=models.SET_NULL, null=True, blank=True, db_column='idscanner', related_name='historial_scanner')
    fecha_entrada = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    created_at = models.DateTimeField(auto_now_add=True)
    id_historial = models.BigIntegerField()
    id_scanner = models.BigIntegerField(null=True, blank=True)
    id_usuario = models.BigIntegerField(null=True, blank=True)
    id_visitante = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'historialaccesos'
        verbose_name = 'Historial de Acceso'
        verbose_name_plural = 'Historial de Accesos'
        ordering = ['-fecha_entrada', '-hora_entrada']

    def __str__(self):
        return f"Acceso {self.idhistorial} - {self.estado}"
