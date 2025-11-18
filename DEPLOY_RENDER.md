# Despliegue Backend SafeHome en Render

Este documento explica cómo desplegar el backend Django en Render.

## Archivos Preparados

✅ `build.sh` - Script de construcción
✅ `render.yaml` - Configuración de Render
✅ `requirements.txt` - Dependencias actualizadas
✅ `settings.py` - Configurado para producción
✅ `.env.example` - Template de variables de entorno

## Pasos para Desplegar

### 1. Preparar el Repositorio

```bash
cd E:\Tecsup\PreTesis\Backend
git add .
git commit -m "Preparar backend para deploy en Render"
git push origin main
```

### 2. Crear Cuenta en Render

1. Ve a https://render.com
2. Crea una cuenta o inicia sesión
3. Conecta tu cuenta de GitHub

### 3. Crear Web Service

1. Click en **"New +"** → **"Web Service"**
2. Conecta tu repositorio `Administrador-SafeHome`
3. Configura:
   - **Name**: `safehome-backend`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `Backend/service`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn service.wsgi:application`

### 4. Variables de Entorno

En la sección "Environment Variables", agrega:

```
SECRET_KEY=<genera-una-clave-segura>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<Render lo configura automáticamente>
CORS_ALLOWED_ORIGINS=https://tu-frontend.onrender.com,http://localhost:5173
```

**Para generar SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(50))
```

### 5. Base de Datos

**Opción A: Usar tu base de datos existente de Render**
```
DATABASE_URL=postgresql://admin:W6oN9J4BJGLJ3wf54wzH9EXgWR6rgtn1@dpg-d46mk7q4d50c738v6abg-a.oregon-postgres.render.com:5432/safe_home
```

**Opción B: Crear nueva base de datos en Render**
1. Click en **"New +"** → **"PostgreSQL"**
2. Nombra: `safehome-db`
3. Copia el `External Database URL`
4. Pégalo en la variable `DATABASE_URL` del Web Service

### 6. Deploy

1. Click en **"Create Web Service"**
2. Render comenzará a construir y desplegar
3. Espera 5-10 minutos
4. Tu API estará disponible en: `https://safehome-backend.onrender.com`

## Endpoints de la API

Una vez desplegado:

- **API Root**: `https://safehome-backend.onrender.com/api/`
- **Admin**: `https://safehome-backend.onrender.com/admin/`
- **Departamentos**: `https://safehome-backend.onrender.com/api/departamentos/`
- **Usuarios**: `https://safehome-backend.onrender.com/api/usuarios/`
- **Visitantes**: `https://safehome-backend.onrender.com/api/visitantes/`
- **Scanner**: `https://safehome-backend.onrender.com/api/scanner/`
- **Historial**: `https://safehome-backend.onrender.com/api/historial/`

## Actualizar Frontend

Después del deploy, actualiza el `.env` del frontend:

```env
VITE_API_BASE_URL=https://safehome-backend.onrender.com/api
```

## Troubleshooting

### Error: "No module named 'gunicorn'"
- Verifica que `requirements.txt` incluya `gunicorn==23.0.0`

### Error: "Database connection failed"
- Verifica que `DATABASE_URL` esté configurada correctamente
- Asegúrate de que la base de datos esté activa

### Error: "ALLOWED_HOSTS"
- Agrega tu dominio de Render a `ALLOWED_HOSTS`
- Ejemplo: `ALLOWED_HOSTS=safehome-backend.onrender.com,.onrender.com`

### Error: "CORS"
- Actualiza `CORS_ALLOWED_ORIGINS` con tu URL del frontend
- Incluye tanto HTTP como HTTPS si es necesario

## Comandos Útiles

**Ver logs en tiempo real:**
En el dashboard de Render → Pestaña "Logs"

**Ejecutar migraciones manualmente:**
En el dashboard → Pestaña "Shell"
```bash
python manage.py migrate
```

**Crear superusuario:**
```bash
python manage.py createsuperuser
```

## Plan Gratuito de Render

- ✅ 750 horas/mes de servicio web
- ✅ Base de datos PostgreSQL (90 días, luego expira)
- ⚠️ El servicio se "duerme" después de 15 min de inactividad
- ⚠️ Primera request después de dormir toma ~30-60 segundos

## Notas Importantes

1. **Seguridad**: Cambia el `SECRET_KEY` en producción
2. **DEBUG**: Siempre debe ser `False` en producción
3. **Database**: Considera migrar a un plan de pago para BD persistente
4. **HTTPS**: Render proporciona HTTPS automáticamente
5. **Backups**: Haz backups regulares de tu base de datos
