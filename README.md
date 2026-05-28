# taller-sesion-02

Aplicación fullstack con:

- **Backend** en FastAPI (`/backend`) para autenticación JWT.
- **Frontend** en React + Vite (`/frontend`) con login y página de bienvenida protegida.

## Características del frontend

- Página de **login** conectada al endpoint `POST /auth/token`.
- Token JWT guardado en `sessionStorage`.
- Página de **bienvenida** protegida: si no hay token en sesión, redirige al login.
- Botón de cierre de sesión que elimina el token.
- Estilos aplicados según el estándar visual definido en `DESING.md` (paleta verde/teal, tarjetas con borde redondeado y botones tipo pill).

## Requisitos

- Python 3.11+
- Poetry
- Node.js 18+ y npm

## Cómo ejecutar

### 1) Backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La API quedará disponible en `http://localhost:8000`.

### 2) Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

La aplicación web quedará disponible en `http://localhost:5173`.

## Credenciales de prueba

- Usuario: `admin`
- Contraseña: `admin123`

## Variables útiles del frontend

Puedes cambiar la URL del backend configurando:

```bash
VITE_API_URL=http://localhost:8000
```

Si no se define, el frontend usa `http://localhost:8000` por defecto.