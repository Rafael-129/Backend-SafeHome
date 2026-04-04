# 🚀 STARTUP COMMAND Y CONFIGURATION PARA AZURE

## 1️⃣ STARTUP COMMAND (Portal Azure)

**Ubicación:** App Service → Settings → Configuration → General settings → Startup Command

**COMANDO CORRECTO:**
```bash
cd service && gunicorn service.wsgi:application --bind 0.0.0.0 --workers 2 --timeout 120
```

**⚠️ NO USAR:**
```bash
# ❌ INCORRECTO - Ejecutar migrate cada startup es arriesgado
cd service && python manage.py migrate && gunicorn service.wsgi:application --bind 0.0.0.0 --workers 2 --timeout 120
```

**Por qué?**
- Si hay conflicto de migración → App no levanta → Downtime
- Cada restart innecesariamente espera las migraciones
- Las migraciones son operación de BD, no de app startup

---

## 2️⃣ VARIABLES DE ENTORNO (Application Settings)

**Ubicación:** App Service → Settings → Configuration → Application Settings

**AGREGAR ESTAS VARIABLES:**

```
Name                          | Value
──────────────────────────────────────────────────────────────────────
SECRET_KEY                    | [Generar con: python -c "import secrets; print(secrets.token_urlsafe(50))"]
DEBUG                         | False
ALLOWED_HOSTS                 | backendsafehome-dnakbxbragevcail.azurewebsites.net,.azurewebsites.net
CORS_ALLOWED_ORIGINS          | https://tu-frontend.azurewebsites.net,http://localhost:5173
CSRF_TRUSTED_ORIGINS          | https://backendsafehome-dnakbxbragevcail.azurewebsites.net
DATABASE_URL                  | postgresql://user:password@host:5432/dbname
DJANGO_LOG_LEVEL              | INFO
```

**Ejemplo con Neon PostgreSQL:**
```
DATABASE_URL = postgresql://neondb_owner:TOKEN@host.neon.tech/database?sslmode=require
```

---

## 3️⃣ CÓMO EJECUTAR MIGRACIONES EN PRODUCCIÓN

### Opción A: Cloud Shell de Azure (Recomendado)

1. Ve a Azure Portal → Abre Cloud Shell (arriba a la derecha)

2. Conéctate al App Service:
```bash
# Navega al directorio de la app
cd /home/site/wwwroot
```

3. Ejecuta migraciones:
```bash
# Asegúrate de estar en el directorio del manage.py
cd service
python manage.py migrate
```

4. Verifica el resultado:
```bash
python manage.py showmigrations
```

### Opción B: SSH directo

1. en App Service → Development Tools → SSH

2. Ejecuta:
```bash
cd /home/site/wwwroot/service
source /home/site/wwwroot/.venv/bin/activate  # Si existe venv
python manage.py migrate
```

### Opción C: Script de Pre-Deployment (Automatizado)

Crear archivo `.deployment` en raíz:

```ini
[config]
command = deploy.sh
```

Crear archivo `deploy.sh`:

```bash
#!/bin/bash
set -e

echo "Starting deployment..."

cd Backend/service

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
python manage.py collectstatic --no-input

# 3. Ejecutar migraciones
python manage.py migrate

# 4. Crear superusuario si no existe
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@safehome.local', 'admin123')
    print("✅ Superusuario creado")
else:
    print("✅ Superusuario ya existe")
END

echo "✅ Deployment completado"
```

---

## 4️⃣ PRIMERA VEZ: SETUP COMPLETO

```bash
# 1. Conectar al app service (SSH o Cloud Shell)

# 2. Navegar
cd /home/site/wwwroot

# 3. Ver estructura
ls -la

# 4. Ir a la carpeta del proyecto
cd service

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Crear base de datos (si es nueva)
python manage.py migrate

# 7. Crear superusuario para admin
python manage.py createsuperuser

# 8. Recolectar estáticos
python manage.py collectstatic --no-input

# 9. Verificar que todo esté bien
python manage.py check --deploy

# 10. Ver logs
az webapp log tail --name backendsafehome-dnakbxbragevcail --resource-group <TU_RESOURCE_GROUP>
```

---

## 5️⃣ POST-DEPLOYMENT: VERIFICACIÓN

### Verificar que el app levanta:

```bash
# Health check
curl https://backendsafehome-dnakbxbragevcail.azurewebsites.net/api/health/

# Debe devolver:
# {"status":"ok","message":"API funcionando correctamente"}
```

### Ver logs en tiempo real:

```bash
# En portal: App Service → Log stream

# O por CLI:
az webapp log tail --name backendsafehome-dnakbxbragevcail
```

### Probar endpoints:

```bash
# Listar departamentos
curl https://backendsafehome-dnakbxbragevcail.azurewebsites.net/api/departamentos/

# Admin panel
# https://backendsafehome-dnakbxbragevcail.azurewebsites.net/admin/
```

---

## 6️⃣ TROUBLESHOOTING

### Error: "ModuleNotFoundError: No module named 'django'"

**Causa:** Dependencias no instaladas

**Solución:**
```bash
cd /home/site/wwwroot/service
pip install -r requirements.txt
az webapp restart --name backendsafehome-dnakbxbragevcail
```

### Error: "Database connection refused"

**Causa:** DATABASE_URL incorrea o BD caída

**Verificar:**
```bash
# Ver valor actual
echo $DATABASE_URL

# Probar conexión manualmente
psql $DATABASE_URL -c "SELECT 1"
```

### Error: "SyntaxError" o migraciones falladas

**Causa:** Conflicto de migraciones

**Solución:**
```bash
# Ver estado
python manage.py showmigrations

# Revert última migración si es necesario
python manage.py migrate api 0001

# Aplicar de nuevo
python manage.py migrate
```

### App tarda mucho en responder

**Causa:** Pool de workers insuficiente o timeout bajo

**Solución en Startup Command:**
```bash
# Aumentar workers y timeout
cd service && gunicorn service.wsgi:application --bind 0.0.0.0 --workers 4 --timeout 180 --max-requests 1000
```

---

## 7️⃣ COMANDOS ÚTILES

```bash
# Ver todas las migraciones
python manage.py showmigrations

# Ver migraciones sin aplicar
python manage.py showmigrations --plan

# Rollback última migración
python manage.py migrate api 0002

# Crear nueva migración
python manage.py makemigrations

# Shell interactivo Django
python manage.py shell

# Estadísticas de BD
python manage.py dbshell
```

---

## ✅ CHECKLIST ANTES DE PRODUCCIÓN

- [ ] Startup Command actualizado (sin migrate)
- [ ] Todas las variables de entorno en Application Settings
- [ ] SECRET_KEY generado y cambiado
- [ ] DATABASE_URL configurada y probada
- [ ] Migraciones ejecutadas manualmente
- [ ] DEBUG=False
- [ ] .env NO está en repo
- [ ] Health check responde 200 OK
- [ ] Admin panel accesible
- [ ] Logs visibles en Log stream
