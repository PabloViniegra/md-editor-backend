# md-editor-backend

Este proyecto es el backend de una aplicación de edición de Markdown. Proporciona una API para la gestión de usuarios y posts, utilizando Python y Flask, con SQLAlchemy para la gestión de la base de datos y Alembic para las migraciones.

## Características principales
- Registro y autenticación de usuarios
- Creación, edición y eliminación de posts en formato Markdown
- Gestión de base de datos con SQLAlchemy
- Migraciones de base de datos con Alembic

## Clonación del proyecto

```powershell
git clone https://github.com/tu-usuario/md-editor-backend.git
cd md-editor-backend
```

## Variables de entorno necesarias
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
SECRET_KEY=tu_clave_secreta
DATABASE_URL=sqlite:///app.db
```

- `SECRET_KEY`: Clave secreta para la aplicación Flask
- `DATABASE_URL`: URL de la base de datos (por defecto usa SQLite local)

## Instalación de dependencias

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Migraciones de base de datos

```powershell
alembic upgrade head
```

## Levantar el servidor en local

```powershell
python run.py
```

El servidor estará disponible en `http://localhost:8000`.

## Estructura del proyecto
- `app/`: Código fuente principal
- `migrations/`: Archivos de migración de Alembic
- `requirements.txt`: Dependencias del proyecto
- `run.py`: Script principal para ejecutar la aplicación

## Notas
- Asegúrate de tener Python 3.12 o superior instalado.
- Para desarrollo, puedes usar SQLite, pero en producción se recomienda una base de datos más robusta.
