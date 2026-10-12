# SmartWarehouse API

API para la localización y control de inventario en almacén. Proyecto de Ingeniería Industrial para optimizar los tiempos de búsqueda y mejorar el control de inventarios.

## Características

- **Gestión de productos**: CRUD completo con códigos únicos y categorías
- **Ubicaciones físicas**: Pasillo-Estante-Nivel con códigos QR
- **Control de inventario**: Stock por ubicación con alertas de stock bajo
- **Movimientos**: Entradas, salidas y traslados con registro histórico
- **Búsquedas**: Flujo completo de búsqueda con medición de tiempos
- **Incidencias**: Reporte y seguimiento de incidencias del almacén
- **Métricas**: Indicadores clave para Ingeniería Industrial

## Estructura del Proyecto

```
backend/
├── app/
│   ├── application/        # Capa de aplicación
│   │   ├── dtos/          # Data Transfer Objects
│   │   └── use_cases/     # Casos de uso
│   ├── core/              # Configuración y excepciones
│   ├── domain/            # Capa de dominio
│   │   ├── entities/      # Entidades
│   │   ├── exceptions/    # Excepciones de dominio
│   │   ├── ports/         # Puertos (interfaces)
│   │   ├── repositories/  # Contratos de repositorios
│   │   └── value_objects/ # Value objects
│   └── infrastructure/    # Capa de infraestructura
│       ├── api/          # API REST
│       │   ├── v1/
│       │   │   ├── routes/    # Routers
│       │   │   ├── dependencies.py  # Inyección de dependencias
│       │   │   └── exception_handlers.py
│       │   └── ...
│       ├── database/     # Modelos SQLAlchemy
│       ├── repositories/ # Implementaciones de repositorios
│       └── security/     # JWT, bcrypt
├── tests/                # Tests automatizados
├── scripts/              # Scripts de utilidad
├── migrations/           # Migraciones Alembic
├── .env                  # Variables de entorno
├── requirements.txt      # Dependencias
└── main.py               # Punto de entrada
```

## Requisitos

- Python 3.12+
- MySQL 8.0+
- pip

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno (copiar `.env.example` a `.env` y ajustar)

5. Ejecutar migraciones:
   ```bash
   alembic upgrade head
   ```

6. Cargar datos de seed:
   ```bash
   mysql -u usuario -p smart_warehouse < init.sql
   mysql -u usuario -p smart_warehouse < insert.sql
   ```

7. Actualizar contraseñas de usuarios sintéticos:
   ```bash
   python scripts/seed_usuarios_password.py
   ```

## Ejecución

```bash
# Desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API

La API estará disponible en `http://localhost:8000`

- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

### Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /api/v1/auth/login | Iniciar sesión |
| GET | /api/v1/productos/ | Listar productos |
| GET | /api/v1/ubicaciones/ | Listar ubicaciones |
| GET | /api/v1/inventario/producto/{id} | Stock de producto |
| POST | /api/v1/movimientos/entrada | Registrar entrada |
| POST | /api/v1/busquedas/iniciar | Iniciar búsqueda |
| GET | /api/v1/metricas/dashboard | Dashboard |

### Usuarios de prueba

| Email | Contraseña | Rol |
|-------|------------|-----|
| ana.torres@xyz.com | Demo1234! | Administrador |
| carlos.ruiz@xyz.com | Demo1234! | Supervisor |
| luis.mendoza@xyz.com | Demo1234! | Almacenero |

## Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar un archivo específico
pytest tests/test_productos.py -v

# Ejecutar con coverage
pytest tests/ --cov=app --cov-report=html
```

## Migraciones

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

## Docker

```bash
# Construir imagen
docker build -t smartwarehouse-api .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env smartwarehouse-api
```

## Licencia

MIT
