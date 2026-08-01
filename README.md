<h1 align="center">🏟️ Sistema de Reservas de Canchas Deportivas</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
</p>

## 📖 Descripción del Proyecto
Este repositorio contiene el backend (API REST) para la administración y control de un complejo deportivo. El sistema permite registrar clientes, administrar las canchas disponibles y controlar la agenda de reservaciones, aplicando reglas de negocio estrictas para evitar el empalme de horarios y gestionar los estatus de pago de manera eficiente.

## 🚀 Características Principales
- **CRUD Completo:** Gestión integral de Clientes, Canchas y Reservas.
- **Validación de Negocio:** Lógica en tiempo real que previene empalmes (doble reserva) de la misma cancha en el mismo horario.
- **Búsqueda Dinámica:** Filtro avanzado por tipo de superficie de cancha (ej. *sintética*, *pasto*, *duela*).
- **Documentación Interactiva:** Interfaz autogenerada en vivo (Swagger UI).
- **Infraestructura Ágil:** Containerización lista para producción con Docker Compose.

## 🏗️ Estructura del Repositorio
- `app/models.py`: Modelos de la base de datos (SQLAlchemy).
- `app/schemas.py`: Esquemas de validación de datos (Pydantic).
- `app/main.py`: Rutas, endpoints y lógica de negocio (FastAPI).
- `app/database.py`: Motor de conexión a PostgreSQL.
- `alembic/`: Entorno de migraciones automáticas de base de datos.

## ⚙️ Pre-requisitos
Antes de comenzar, asegúrate de tener instalado en tu equipo:
- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)

## 🛠️ Instalación y Puesta en Marcha

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/AgustinGmz/canchas-backend.git
   cd canchas-backend
   ```

2. **Configurar el entorno**
   Crea un archivo `.env` en la raíz del proyecto basándote en `.env.example`.
   ```bash
   cp .env.example .env
   ```

3. **Levantar los contenedores (Servidor y Base de Datos)**
   El proyecto utiliza Docker Compose para orquestar los servicios sin necesidad de instalaciones locales pesadas.
   ```bash
   docker-compose up -d
   ```

4. **Ejecutar migraciones (Generar Tablas)**
   Aplica los cambios de la base de datos para generar las tablas.
   ```bash
   docker-compose exec web alembic upgrade head
   ```

## 🌐 Pruebas y Uso
Una vez que el servidor esté corriendo, puedes acceder a la interfaz de pruebas interactivas de Swagger UI en tu navegador:
👉 **[http://localhost:8001/docs](http://localhost:8001/docs)**

Desde aquí podrás interactuar directamente con la API, enviar payloads en formato JSON y ver las respuestas y validaciones en tiempo real.
