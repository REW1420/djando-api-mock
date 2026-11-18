# API de Salas (Django + DRF + PostgreSQL)

API REST con autenticación JWT para gestionar salas.

## Requisitos

- **Python 3.10+**: `python --version`
- **Docker Desktop**, para la base de datos PostgreSQL: `docker --version`

---

## Cómo correr el proyecto

Todos los comandos se ejecutan en la carpeta raíz del proyecto (donde está `manage.py`).

### 1. Levantar la base de datos (PostgreSQL en Docker)

```bash
docker compose up -d
```

Verifica que esté lista (el estado debe decir `healthy`):

```bash
docker compose ps
```

### 2. Crear y activar el entorno virtual

```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# Windows (Git Bash)
python -m venv venv
source venv/Scripts/activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Si ya existe la carpeta `venv`, no hace falta crearla otra vez; solo actívala.

> **PowerShell da error de "ejecución de scripts deshabilitada"?** Ejecuta una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar las migraciones (crea las tablas)

```bash
python manage.py migrate
```

### 5. (Opcional) Crear un superusuario para el panel de admin

```bash
python manage.py createsuperuser
```

### 6. Levantar el servidor

```bash
python manage.py runserver
```

La API queda en **http://127.0.0.1:8000/**. Para comprobar que funciona, abre http://127.0.0.1:8000/health/

---

## Uso diario (cuando ya está instalado)

```bash
docker compose up -d              # 1. base de datos
.\venv\Scripts\Activate.ps1       # 2. entorno virtual (PowerShell)
python manage.py runserver        # 3. servidor
```

---

## Configuración de la base de datos

Por defecto el proyecto usa los mismos datos que `docker-compose.yml`, así que no
necesitas configurar nada. Si tu base de datos usa otros datos, defínelos con
variables de entorno antes de correr el servidor:

| Variable      | Valor por defecto |
|---------------|-------------------|
| `DB_NAME`     | `app_db`          |
| `DB_USER`     | `app_user`        |
| `DB_PASSWORD` | `app_password`    |
| `DB_HOST`     | `localhost`       |
| `DB_PORT`     | `5432`            |

```powershell
# PowerShell
$env:DB_HOST = "localhost"
```

```bash
# Bash
export DB_HOST=localhost
```

---

## Endpoints

| Método | URL                    | Auth | Descripción                    |
|--------|------------------------|------|--------------------------------|
| GET    | `/health/`             | No   | Estado de la API               |
| POST   | `/auth/register/`      | No   | Registrar usuario              |
| POST   | `/auth/login/`         | No   | Iniciar sesión (devuelve JWT)  |
| GET    | `/auth/me/`            | Sí   | Datos del usuario autenticado  |
| GET    | `/salas/`              | No   | Listar salas                   |
| POST   | `/salas/create`        | No   | Crear sala                     |
| GET    | `/salas/<id>`          | No   | Obtener una sala               |
| DELETE | `/salas/<id>/delete`   | No   | Eliminar una sala              |
| -      | `/admin/`              | -    | Panel de administración        |

### Ejemplos

**Registrar e iniciar sesión**

```bash
curl -X POST http://127.0.0.1:8000/auth/register/ -H "Content-Type: application/json" -d "{\"username\": \"juan\", \"password\": \"secreta123\"}"

curl -X POST http://127.0.0.1:8000/auth/login/ -H "Content-Type: application/json" -d "{\"username\": \"juan\", \"password\": \"secreta123\"}"
```

**Usar el token en rutas protegidas** (el token `access` dura 15 minutos)

```bash
curl http://127.0.0.1:8000/auth/me/ -H "Authorization: Bearer <access_token>"
```

**Crear una sala**

```bash
curl -X POST http://127.0.0.1:8000/salas/create -H "Content-Type: application/json" -d "{\"nombre\": \"A-101\", \"capacidad\": 30, \"equipamiento\": [\"proyector\", \"pizarra\"]}"
```

> En PowerShell usa `curl.exe` en lugar de `curl`, o prueba los endpoints con Postman.

### Formato de respuesta

Las respuestas de `/salas/` y los errores de DRF (401, 403, 405, JSON inválido)
usan siempre la misma estructura (`core/responses.py`):

```json
{
  "success": true,
  "message": "Sala creada exitosamente",
  "data": { "id": 1, "nombre": "A-101", "capacidad": 30, "equipamiento": ["proyector"], "activa": true },
  "errors": null
}
```

---

## Comandos útiles

```bash
# Después de cambiar un modelo (models.py)
python manage.py makemigrations
python manage.py migrate

# Crear una app nueva (luego agrégala a INSTALLED_APPS en config/settings.py)
python manage.py startapp nombre_app

# Revisar que el proyecto no tenga errores de configuración
python manage.py check

# Guardar las dependencias después de instalar un paquete nuevo
pip freeze > requirements.txt

# Base de datos
docker compose down        # detener (los datos se conservan)
docker compose down -v     # detener y BORRAR todos los datos
docker compose logs db     # ver logs de PostgreSQL
```

## Estructura

```
config/   Configuración del proyecto (settings.py, urls.py)
core/     Código compartido: respuestas estándar y manejo de errores
auth/     Registro, login y JWT
salas/    CRUD de salas (models, serializers, service, views)
health/   Endpoint de estado
```
