import os
import django
from datetime import datetime, time, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')
django.setup()

from api.models import Departamento, Usuario, Visitante, Scanner, HistorialAccesos

# Limpiar datos existentes (opcional)
print("⏳ Limpiando datos existentes...")
HistorialAccesos.objects.all().delete()
Scanner.objects.all().delete()
Visitante.objects.all().delete()
Usuario.objects.all().delete()
Departamento.objects.all().delete()

# ============================================
# 1. CREAR DEPARTAMENTOS
# ============================================
print("📦 Creando departamentos...")

departamentos_data = [
    ('A-501', 'A', 5, 1, 85.50, 3, 2, 1),
    ('A-502', 'A', 5, 2, 92.00, 3, 2, 1),
    ('B-302', 'B', 3, 2, 75.00, 2, 1, 1),
    ('B-303', 'B', 3, 3, 78.50, 2, 2, 1),
    ('C-105', 'C', 1, 5, 120.00, 4, 3, 2),
    ('C-106', 'C', 1, 6, 115.00, 4, 3, 2),
    ('D-201', 'D', 2, 1, 68.00, 2, 1, 1),
    ('E-403', 'E', 4, 3, 95.00, 3, 2, 1),
    ('F-105', 'F', 1, 5, 88.50, 3, 2, 1),
    ('F-205', 'F', 2, 5, 88.50, 3, 2, 1),
]

departamentos = {}
for codigo, torre, piso, numero, area, hab, banos, estac in departamentos_data:
    dept = Departamento.objects.create(
        codigo=codigo,
        torre=torre,
        piso=piso,
        numero=numero,
        area_m2=area,
        habitaciones=hab,
        banos=banos,
        estacionamientos=estac
    )
    departamentos[codigo] = dept
    print(f"  ✅ Departamento {codigo}")

# ============================================
# 2. CREAR USUARIOS (RESIDENTES)
# ============================================
print("👤 Creando usuarios (residentes)...")

usuarios_data = [
    ('Roberto', 'Silva Paredes', '45678912', 'roberto.silva@email.com', 'D-201', 
     'https://randomuser.me/api/portraits/men/10.jpg'),
    ('Lucía', 'Fernández Castro', '78945612', 'lucia.fernandez@email.com', 'E-403', 
     'https://randomuser.me/api/portraits/women/12.jpg'),
    ('Diego', 'Ramírez Ochoa', '32165498', 'diego.ramirez@email.com', 'F-105', 
     'https://randomuser.me/api/portraits/men/15.jpg'),
]

usuarios = {}
for nombre, apellido, dni, correo, dept_codigo, foto in usuarios_data:
    user = Usuario.objects.create(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        correo=correo,
        iddepartamento=departamentos[dept_codigo],
        foto=foto
    )
    usuarios[dni] = user
    print(f"  ✅ Usuario: {nombre} {apellido}")

# ============================================
# 3. CREAR VISITANTES
# ============================================
print("🚪 Creando visitantes...")

visitantes_data = [
    ('Carmen', 'Gutiérrez Díaz', '65498732', 'Visita familiar', '2025-01-19', '15:00:00', 'D-201', 
     'https://randomuser.me/api/portraits/women/20.jpg'),
    ('Miguel', 'Vargas Rojas', '14725836', 'Reparación de electrodomésticos', '2025-01-19', '11:30:00', 'E-403', 
     'https://randomuser.me/api/portraits/men/22.jpg'),
    ('Sofía', 'Delgado Moreno', '98765432', 'Reunión de trabajo', '2025-01-19', '17:20:00', 'F-105', 
     'https://randomuser.me/api/portraits/women/25.jpg'),
]

visitantes = {}
for nombre, apellido, dni, motivo, fecha_str, hora_str, dept_codigo, foto in visitantes_data:
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    hora = datetime.strptime(hora_str, '%H:%M:%S').time()
    
    visit = Visitante.objects.create(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        motivo=motivo,
        fecha_visita=fecha,
        hora_visita=hora,
        iddepartamento=departamentos[dept_codigo],
        foto=foto
    )
    visitantes[dni] = visit
    print(f"  ✅ Visitante: {nombre} {apellido}")

# ============================================
# 4. CREAR ESCANEOS
# ============================================
print("📸 Creando escaneos...")

# Escaneo 1: Roberto (residente)
scan1 = Scanner.objects.create(
    idusuario=usuarios['45678912'],
    idvisitante=None,
    foto_capturada='scan_roberto_20250119_073000.jpg',
    tipo_persona='residente',
    fecha=datetime.strptime('2025-01-19 07:30:00', '%Y-%m-%d %H:%M:%S')
)
print(f"  ✅ Escaneo: Roberto")

# Escaneo 2: Carmen (visitante)
scan2 = Scanner.objects.create(
    idusuario=None,
    idvisitante=visitantes['65498732'],
    foto_capturada='scan_carmen_20250119_150000.jpg',
    tipo_persona='visitante',
    fecha=datetime.strptime('2025-01-19 15:00:00', '%Y-%m-%d %H:%M:%S')
)
print(f"  ✅ Escaneo: Carmen")

# Escaneo 3: Lucía (residente)
scan3 = Scanner.objects.create(
    idusuario=usuarios['78945612'],
    idvisitante=None,
    foto_capturada='scan_lucia_20250119_084500.jpg',
    tipo_persona='residente',
    fecha=datetime.strptime('2025-01-19 08:45:00', '%Y-%m-%d %H:%M:%S')
)
print(f"  ✅ Escaneo: Lucía")

# ============================================
# 5. CREAR HISTORIAL DE ACCESOS
# ============================================
print("📋 Creando historial de accesos...")

# Acceso 1: Roberto
hist1 = HistorialAccesos.objects.create(
    idusuario=usuarios['45678912'],
    idvisitante=None,
    idscanner=scan1,
    fecha_entrada=date(2025, 1, 19),
    hora_entrada=time(7, 30, 0),
    hora_salida=time(19, 15, 0),
    estado='Permitido'
)
print(f"  ✅ Acceso: Roberto (Permitido)")

# Acceso 2: Carmen
hist2 = HistorialAccesos.objects.create(
    idusuario=None,
    idvisitante=visitantes['65498732'],
    idscanner=scan2,
    fecha_entrada=date(2025, 1, 19),
    hora_entrada=time(15, 0, 0),
    hora_salida=None,
    estado='Permitido'
)
print(f"  ✅ Acceso: Carmen (Permitido)")

# Acceso 3: Lucía
hist3 = HistorialAccesos.objects.create(
    idusuario=usuarios['78945612'],
    idvisitante=None,
    idscanner=scan3,
    fecha_entrada=date(2025, 1, 19),
    hora_entrada=time(8, 45, 0),
    hora_salida=None,
    estado='Permitido'
)
print(f"  ✅ Acceso: Lucía (Permitido)")

# ============================================
# RESUMEN
# ============================================
print("\n" + "="*50)
print("✅ DATOS CARGADOS EXITOSAMENTE EN NEON")
print("="*50)
print(f"📦 Departamentos: {Departamento.objects.count()}")
print(f"👤 Usuarios: {Usuario.objects.count()}")
print(f"🚪 Visitantes: {Visitante.objects.count()}")
print(f"📸 Escaneos: {Scanner.objects.count()}")
print(f"📋 Historial de Accesos: {HistorialAccesos.objects.count()}")
print("="*50)
