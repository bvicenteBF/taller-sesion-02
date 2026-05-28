# Backend – JWT Authentication API

API REST construida con **Python** y **FastAPI** que implementa autenticación mediante **JSON Web Tokens (JWT)**.

---

## Tecnologías

| Herramienta | Versión |
|---|---|
| Python | 3.11 |
| FastAPI | ^0.115 |
| Uvicorn | ^0.32 |
| python-jose | ^3.3 |
| bcrypt | ^4.2 |
| pydantic-settings | ^2.6 |
| Poetry | 1.8 |

---

## Estructura del proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── auth.py        # Lógica JWT y autenticación
│   ├── config.py      # Configuración via variables de entorno
│   ├── main.py        # Aplicación FastAPI y endpoints
│   └── schemas.py     # Modelos Pydantic
├── tests/
│   └── test_auth.py
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Endpoints

### `POST /auth/token`

Autentica al usuario y devuelve un JWT válido por **300 segundos**.

**Request body (JSON):**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

### `POST /auth/refresh`

Recibe un token válido en el header `Authorization: ****** y devuelve un nuevo token con expiración renovada.

**Headers:**
```
Authorization: ******
```

**Response:**
```json
{
  "access_token": "<nuevo_jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

### `GET /health`

Verifica que el servicio está en línea.

**Response:**
```json
{"status": "ok"}
```

---

## Variables de entorno

| Variable | Default | Descripción |
|---|---|---|
| `SECRET_KEY` | `supersecretkey_change_in_production` | Clave secreta para firmar tokens |
| `ALGORITHM` | `HS256` | Algoritmo JWT |
| `ACCESS_TOKEN_EXPIRE_SECONDS` | `300` | Duración del token en segundos |

> ⚠️ Cambia `SECRET_KEY` por un valor seguro antes de usar en producción.

---

## Instrucciones de uso

### Opción 1 – Docker Compose (recomendado)

Desde la **raíz del repositorio**, ejecuta:

```bash
# 1. Crea el archivo de variables de entorno
cp backend/.env.example backend/.env
# Edita backend/.env y cambia SECRET_KEY por un valor seguro

# 2. Levanta los servicios
docker compose up --build
```

La API estará disponible en <http://localhost:8000>.

---

### Opción 2 – Ejecución local con Poetry

#### 1. Instalar dependencias

```bash
cd backend
poetry install
```

#### 2. Iniciar el servidor

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Uso de la API

### Obtener token

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Refrescar token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Authorization: ******"
```

---

## Documentación interactiva

FastAPI genera automáticamente la documentación Swagger UI:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

---

## Ejecutar tests

```bash
cd backend
poetry install
poetry run pytest
```
