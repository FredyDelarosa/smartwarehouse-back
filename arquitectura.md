backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                         # Punto de entrada FastAPI
│   │
│   ├── core/                           # Configuración transversal
│   │   ├── __init__.py
│   │   ├── config.py                   # Settings con pydantic-settings
│   │   ├── security.py                 # Hash de passwords + JWT
│   │   └── exceptions.py               # Excepciones de aplicación
│   │
│   ├── domain/                         # Núcleo: sin dependencias externas
│   │   ├── __init__.py
│   │   ├── entities/                   # Modelos de negocio puros (dataclasses)
│   │   │   ├── __init__.py
│   │   │   ├── almacen.py
│   │   │   ├── categoria.py
│   │   │   ├── producto.py
│   │   │   ├── ubicacion.py
│   │   │   ├── inventario.py
│   │   │   ├── movimiento.py
│   │   │   ├── busqueda.py
│   │   │   ├── incidencia.py
│   │   │   ├── usuario.py
│   │   │   └── rol.py
│   │   ├── value_objects/              # Objetos de valor (inmutables)
│   │   │   ├── __init__.py
│   │   │   └── codigo_ubicacion.py
│   │   ├── exceptions/                 # Excepciones del dominio
│   │   │   ├── __init__.py
│   │   │   └── domain_exceptions.py
│   │   └── repositories/               # 🔌 Puertos (interfaces abstractas)
│   │       ├── __init__.py
│   │       ├── almacen_repository.py
│   │       ├── categoria_repository.py
│   │       ├── producto_repository.py
│   │       ├── ubicacion_repository.py
│   │       ├── inventario_repository.py
│   │       ├── movimiento_repository.py
│   │       ├── busqueda_repository.py
│   │       ├── incidencia_repository.py
│   │       ├── usuario_repository.py
│   │       └── rol_repository.py
│   │
│   ├── application/                    # Casos de uso
│   │   ├── __init__.py
│   │   ├── dtos/                       # Data Transfer Objects (Pydantic)
│   │   │   ├── __init__.py
│   │   │   ├── almacen_dto.py
│   │   │   ├── categoria_dto.py
│   │   │   ├── producto_dto.py
│   │   │   ├── ubicacion_dto.py
│   │   │   ├── inventario_dto.py
│   │   │   ├── movimiento_dto.py
│   │   │   ├── busqueda_dto.py
│   │   │   ├── incidencia_dto.py
│   │   │   ├── usuario_dto.py
│   │   │   ├── auth_dto.py
│   │   │   └── metricas_dto.py
│   │   ├── use_cases/                  # Un archivo por caso de uso
│   │   │   ├── __init__.py
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── login_use_case.py
│   │   │   │   └── register_use_case.py
│   │   │   ├── productos/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── crear_producto.py
│   │   │   │   ├── listar_productos.py
│   │   │   │   ├── obtener_producto.py
│   │   │   │   ├── actualizar_producto.py
│   │   │   │   └── eliminar_producto.py
│   │   │   ├── ubicaciones/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── crear_ubicacion.py
│   │   │   │   ├── listar_ubicaciones.py
│   │   │   │   └── buscar_por_qr.py
│   │   │   ├── inventario/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── consultar_stock.py
│   │   │   │   └── alertas_stock_bajo.py
│   │   │   ├── movimientos/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── registrar_entrada.py
│   │   │   │   ├── registrar_salida.py
│   │   │   │   └── registrar_traslado.py
│   │   │   ├── busquedas/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── buscar_producto.py
│   │   │   │   └── registrar_busqueda.py
│   │   │   ├── incidencias/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── crear_incidencia.py
│   │   │   │   └── listar_incidencias.py
│   │   │   └── metricas/
│   │   │       ├── __init__.py
│   │   │       ├── tiempo_promedio_busqueda.py
│   │   │       ├── productos_mal_ubicados.py
│   │   │       └── rotacion_inventario.py
│   │   └── services/                   # Servicios que orquestan varios casos
│   │       └── __init__.py
│   │
│   └── infrastructure/                 # Adaptadores
│       ├── __init__.py
│       ├── database/
│       │   ├── __init__.py
│       │   ├── base.py                 # DeclarativeBase de SQLAlchemy
│       │   ├── session.py              # Engine + SessionLocal async
│       │   └── models/                 # Modelos ORM (mapean a las tablas)
│       │       ├── __init__.py
│       │       ├── almacen_model.py
│       │       ├── categoria_model.py
│       │       ├── producto_model.py
│       │       ├── ubicacion_model.py
│       │       ├── inventario_model.py
│       │       ├── movimiento_model.py
│       │       ├── busqueda_model.py
│       │       ├── incidencia_model.py
│       │       ├── usuario_model.py
│       │       └── rol_model.py
│       ├── repositories/               # Implementación de los puertos
│       │   ├── __init__.py
│       │   ├── almacen_repository_impl.py
│       │   ├── categoria_repository_impl.py
│       │   ├── producto_repository_impl.py
│       │   ├── ubicacion_repository_impl.py
│       │   ├── inventario_repository_impl.py
│       │   ├── movimiento_repository_impl.py
│       │   ├── busqueda_repository_impl.py
│       │   ├── incidencia_repository_impl.py
│       │   ├── usuario_repository_impl.py
│       │   └── rol_repository_impl.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── dependencies.py         # Inyección de dependencias (FastAPI Depends)
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── router.py           # Router agregador v1
│       │       └── routes/
│       │           ├── __init__.py
│       │           ├── auth.py
│       │           ├── productos.py
│       │           ├── ubicaciones.py
│       │           ├── inventario.py
│       │           ├── movimientos.py
│       │           ├── busquedas.py
│       │           ├── incidencias.py
│       │           └── metricas.py
│       └── security/
│           ├── __init__.py
│           ├── jwt_handler.py
│           └── password_hasher.py
│
├── migrations/                         # Alembic
│   └── (se genera con alembic init)
│
├── tests/
│   ├── __init__.py
│   └── ...
│
├── .env
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md