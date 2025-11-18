# 🚀 Guía de Ejecución Local

## 📋 Prerequisitos

- Python 3.11+
- Node.js 20+
- Docker y Docker Compose (solo para DB)

## 🐳 Paso 1: Levantar Base de Datos

```powershell
# En la raíz del proyecto
docker-compose up -d
```

Esto levantará:
- PostgreSQL en `localhost:5432`

## 🔧 Paso 2: Configurar y Ejecutar Backend

```powershell
# Ir a la carpeta backend
cd backend

# Crear entorno virtual (primera vez)
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor (con hot-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará en: http://localhost:8000

## 🎨 Paso 3: Configurar y Ejecutar Frontend

**En otra terminal:**

```powershell
# Ir a la carpeta frontend
cd frontend

# Instalar dependencias (primera vez)
npm install

# Ejecutar servidor de desarrollo (con hot-reload)
npm run dev
```

El frontend estará en: http://localhost:5173

## ✅ Verificación

1. **Backend API**: http://localhost:8000/docs
2. **Frontend**: http://localhost:5173
3. **Base de datos**: Ya tiene los 20 productos cargados con imágenes reales

## 🔄 Cambios en Tiempo Real

Ahora cuando modifiques:
- **Backend**: El servidor se recargará automáticamente (uvicorn --reload)
- **Frontend**: Vite actualizará instantáneamente (HMR - Hot Module Replacement)

## 🛑 Detener Servicios

```powershell
# Detener backend/frontend: Ctrl+C en cada terminal

# Detener Docker (DB)
docker-compose down

# O para mantener los datos y solo pausar:
docker-compose stop
```

## 📝 Comandos Útiles

```powershell
# Ver logs de PostgreSQL
docker logs liquiverde_db

# Conectar a la base de datos
docker exec -it liquiverde_db psql -U postgres -d liquiverde

# Reiniciar solo la base de datos
docker-compose restart db
```

## 🎯 Credenciales de Prueba

- **Usuario**: testuser
- **Email**: test@example.com
- **Contraseña**: password123

¡Listo para desarrollar! 🚀
