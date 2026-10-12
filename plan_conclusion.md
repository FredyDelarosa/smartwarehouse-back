# 📘 Plan de Trabajo — Backend SmartWarehouse

Documento guía para completar el backend del proyecto. Cada fase incluye: **objetivo**, **archivos**, **pasos**, **verificación** y **criterio de cierre**. Está diseñado para que puedas seguirlo sin ambigüedades y detectar errores temprano.

## 🎯 Estado actual

| Fase         | Contenido                                                                                              | Estado |
| ------------ | ------------------------------------------------------------------------------------------------------ | ------ |
| 1            | core/ (config, security, exceptions)                                                                   | ✅      |
| 2            | domain/entities/                                                                                       | ✅      |
| 3            | domain/value_objects/                                                                                  | ✅      |
| 4            | domain/exceptions/                                                                                     | ✅      |
| 5            | domain/repositories/ (puertos)                                                                         | ✅      |
| 6            | infrastructure/database/ (SQLAlchemy + 10 modelos)                                                     | ✅      |
| 7            | infrastructure/security/ (adaptadores)                                                                 | ✅      |
| 8            | infrastructure/repositories/ (10 impls + mappers)                                                      | ✅      |
| 9            | application/dtos/                                                                                      | ✅      |
| 10.1 - 10.8  | Casos de uso (auth, productos, ubicaciones, inventario, movimientos, búsquedas, incidencias, métricas) | ✅      |
| 11.1         | infrastructure/api/ (handlers, dependencies, health, main)                                             | ✅      |
| 11.2         | Router de auth                                                                                         | ✅      |
| 11.3 - 11.10 | Routers de negocio restantes                                                                           | ⏳      |
| 12.x         | Alembic + datos de seed                                                                                | ⏳      |
| 13.x         | Suite de tests automatizados                                                                           | ⏳      |
| 14           | Documentación (README)                                                                                 | ⏳      |
| 15           | Docker y cierre                                                                                        | ⏳      |

## 📏 Reglas transversales (lecciones aprendidas)

Estas reglas **aplican a toda fase** restante. Violarlas ha causado fallos previos.

1.  **`**from __future__ import annotations**` obligatorio** en cualquier módulo que defina un método llamado `list`, `dict`, `type`, `id`, `filter`, `map`, `input` o `next`.
2.  **Nunca referenciar filas por ID autoincremental** en scripts SQL. Siempre por clave natural (`codigo`, `email`, `codigo_ubicacion`).
3.  **Fechas siempre naive UTC**: `datetime.utcnow()`, nunca `datetime.now(timezone.utc)` cuando el destino sea una columna `DATETIME` de MySQL.
4.  **Los repositorios hacen `**flush**`, no `**commit**`**. El commit lo hace el endpoint o el test.
5.  **Los tests que mutan datos van con `**try/finally: rollback**`** o crean/borran su propio registro.
6.  **Antes de un `**assert**` sobre un total**, calcular a mano el resultado. Si un producto está en varias ubicaciones, sumar todas.
7.  **Ningún archivo fuera del plan** sin confirmación previa del responsable.
8.  **Cada verificación termina con un `**print(">>> FASE XX COMPLETA: ...")**`** para confirmar cierre.

## 🧭 Cómo leer cada fase

Cada fase sigue la misma estructura:

-   **Objetivo**: qué se logra al terminar.
-   **Archivos**: qué se crea y qué se modifica.
-   **Implementación**: contenido de cada archivo.
-   **Verificación**: bloque de código que debes ejecutar.
-   **Criterio de cierre**: qué debe pasar para avanzar.

# 🔷 BLOQUE 11 — Routers HTTP

## 📄 Fase 11.3 — Router de productos

### Objetivo

Exponer el CRUD de productos vía HTTP.

### Archivos

-   **Nuevo**: `infrastructure/api/v1/routes/productos.py`
-   **Modificado**: `infrastructure/api/v1/router.py` (agregar `productos.router`)

### Endpoints

| Método | Ruta              | Rol               | Caso de uso               |
| ------ | ----------------- | ----------------- | ------------------------- |
| GET    | /productos        | Autenticado       | ListarProductosUseCase    |
| GET    | /productos/buscar | Autenticado       | ProductoRepository.search |
| GET    | /productos/{id}   | Autenticado       | ObtenerProductoUseCase    |
| POST   | /productos        | Admin, Supervisor | CrearProductoUseCase      |
| PATCH  | /productos/{id}   | Admin, Supervisor | ActualizarProductoUseCase |
| DELETE | /productos/{id}   | Admin             | EliminarProductoUseCase   |

### Parámetros de `GET /productos`

-   `skip: int = 0`
-   `limit: int = 50` (validar con `Query(ge=1, le=100)`)
-   `categoria_id: Optional[int] = None`
-   `solo_activos: bool = False`

### Respuesta paginada

Debe envolver la lista en un objeto `PaginadoDTO`:

python

class PaginadoProductosDTO(BaseModel):  
    items: list\[ProductoReadDTO\]  
    total: int  
    skip: int  
    limit: int

### Verificación

Test con `TestClient` que:

1.  Liste productos (espera 50 totales).
2.  Liste filtrados por categoría 1 (espera 10).
3.  Busque "tornillo" (espera varios matches).
4.  Cree uno nuevo, lo obtenga, lo actualice, lo dé de baja lógica.
5.  Intente crear con código duplicado → 409.
6.  Intente crear con código inválido → 422.
7.  Intente crear sin ser Admin/Supervisor → 403.

### Criterio de cierre

Test pasa completo y todos los códigos HTTP son los esperados.

## 📄 Fase 11.4 — Router de ubicaciones + QR

### Objetivo

Listar ubicaciones, crear ubicaciones y escanear QR.

### Archivos

-   **Nuevo**: `infrastructure/api/v1/routes/ubicaciones.py`
-   **Modificado**: `infrastructure/api/v1/router.py`

### Endpoints

| Método | Ruta                              | Rol         | Caso de uso                         |
| ------ | --------------------------------- | ----------- | ----------------------------------- |
| GET    | /ubicaciones                      | Autenticado | ListarUbicacionesUseCase            |
| GET    | /ubicaciones/{id}                 | Autenticado | UbicacionRepository.get_by_id       |
| POST   | /ubicaciones                      | Admin       | CrearUbicacionUseCase               |
| GET    | /ubicaciones/qr/{codigo}          | Autenticado | BuscarUbicacionPorQRUseCase         |
| GET    | /ubicaciones/almacen/{almacen_id} | Autenticado | ListarUbicacionesUseCase con filtro |

### Verificación

1.  Listar (espera 150).
2.  Crear nueva con `P9-Z-99`, verificar duplicado → 409.
3.  Código inválido → 422.
4.  Escanear `QR-P3-A-01` → devuelve ubicación + T001 (350 uds).
5.  Escanear QR inexistente → 404.

### Criterio de cierre

Test pasa. **Cleanup obligatorio** de la ubicación creada al final.

## 📄 Fase 11.5 — Router de inventario

### Objetivo

Consultar stock consolidado y alertas.

### Archivos

-   **Nuevo**: `infrastructure/api/v1/routes/inventario.py`
-   **Modificado**: `infrastructure/api/v1/router.py`

### Endpoints

| Método | Ruta                      | Caso de uso             |
| ------ | ------------------------- | ----------------------- |
| GET    | /inventario/producto/{id} | ConsultarStockUseCase   |
| GET    | /inventario/alertas       | AlertasStockBajoUseCase |

### Verificación

1.  Stock de T001 → total 470, 2 ubicaciones.
2.  Stock de producto inexistente → 404.
3.  Alertas con datos actuales → lista vacía.
4.  Forzar stock bajo (update temporal vía SQL), verificar alerta, restaurar.

### Criterio de cierre

Test pasa. Verificar post-restauración con `ConsultarStockUseCase`.

## 📄 Fase 11.6 — Router de movimientos

### Objetivo

Registrar entradas, salidas y traslados vía HTTP.

### Archivos

-   **Nuevo**: `infrastructure/api/v1/routes/movimientos.py`
-   **Modificado**: `infrastructure/api/v1/router.py`

### Endpoints

| Método | Ruta                  | Rol                    | Caso de uso               |
| ------ | --------------------- | ---------------------- | ------------------------- |
| POST   | /movimientos/entrada  | Almacenero, Supervisor | RegistrarEntradaUseCase   |
| POST   | /movimientos/salida   | Almacenero, Supervisor | RegistrarSalidaUseCase    |
| POST   | /movimientos/traslado | Almacenero, Supervisor | RegistrarTrasladoUseCase  |
| GET    | /movimientos          | Autenticado            | MovimientoRepository.list |

### Verificación

Ejecutar la misma secuencia de la Fase 10.5 pero vía HTTP. Envolver todo en un `try/finally` que haga `UPDATE` de restauración manual (el `TestClient` no permite rollback explícito).

Alternativa recomendada: usar un **producto de prueba temporal** creado al inicio y eliminar todo al final.

### Criterio de cierre

-   Total T001 vuelve a 470 al terminar.
-   Movimientos creados quedan en la BD como evidencia (no se borran).
-   Todos los códigos HTTP correctos.

## 📄 Fase 11.7 — Router de búsquedas

### Objetivo

Implementar el flujo central: iniciar, finalizar y consultar historial.

### Archivos

-   **Nuevo**: `infrastructure/api/v1/routes/busquedas.py`
-   **Modificado**: `infrastructure/api/v1/router.py`

### Endpoints

| Método | Ruta                      | Caso de uso               |
| ------ | ------------------------- | ------------------------- |
| POST   | /busquedas/iniciar        | IniciarBusquedaUseCase    |
| POST   | /busquedas/{id}/finalizar | FinalizarBusquedaUseCase  |
| GET    | /busquedas/historial      | HistorialBusquedasUseCase |

### Verificación

1.  Iniciar búsqueda "Tornillos 1/4" → devuelve `busqueda_id`, producto T001, total 470, 2 ubicaciones.
2.  Esperar 1.2 s.
3.  Finalizar con la ubicación P3-A-01 → `exito=true`, `tiempo_segundos>=1`.
4.  Iniciar búsqueda que no matchea → 404.
5.  Historial → incluye las 2 búsquedas recientes.

### Criterio de cierre

Test pasa. Los registros de búsqueda creados **quedan en BD** (son datos válidos de uso).

## 📄 Fase 11.8 — Router de incidencias

### Objetivo

CRUD de incidencias.

### Archivos

-   **Nuevo**: `infrastructure/api/v1/routes/incidencias.py`
-   **Modificado**: `infrastructure/api/v1/router.py`

### Endpoints

| Método | Ruta                       | Rol                    | Caso de uso               |
| ------ | -------------------------- | ---------------------- | ------------------------- |
| GET    | /incidencias               | Autenticado            | ListarIncidenciasUseCase  |
| POST   | /incidencias               | Autenticado            | CrearIncidenciaUseCase    |
| POST   | /incidencias/{id}/resolver | Almacenero, Supervisor | ResolverIncidenciaUseCase |

### Filtros de `GET /incidencias`

-   `tipo: Optional[TipoIncidencia]`
-   `resuelta: Optional[bool]`
-   `producto_id: Optional[int]`
-   `desde`, `hasta`: `Optional[datetime]`

### Verificación

1.  Listar todas (espera 12).
2.  Filtrar por `MAL_UBICADO` (5), `FALTANTE` (3), `DANADO` (3), `OTRO` (1).
3.  Filtrar por `resuelta=false` (1).
4.  Crear nueva, resolverla, intentar resolverla de nuevo → 422.
5.  Producto inexistente → 404.

### Criterio de cierre

Test pasa. Incidencia creada se elimina al final (o se deja como OTRO válido si prefieres preservarla).

## 📄 Fase 11.9 — Router de métricas

### Objetivo

Exponer los indicadores del proyecto.

### Archivos

-   **Nuevo**: `infrastructure/api/v1/routes/metricas.py`
-   **Modificado**: `infrastructure/api/v1/router.py`

### Endpoints

| Método | Ruta                      | Caso de uso                   |
| ------ | ------------------------- | ----------------------------- |
| GET    | /metricas/tiempo-promedio | TiempoPromedioBusquedaUseCase |
| GET    | /metricas/comparativa     | CompararBusquedasUseCase      |
| GET    | /metricas/incidencias     | ResumenIncidenciasUseCase     |
| GET    | /metricas/movimientos     | ResumenMovimientosUseCase     |
| GET    | /metricas/dashboard       | DashboardResumenUseCase       |

### Query params de `/metricas/comparativa`

-   `desde_anterior`, `hasta_anterior`, `desde_actual`, `hasta_actual` (todos `datetime`)

### Verificación

1.  Tiempo promedio global > 50 búsquedas, promedio > 0.
2.  Comparativa julio vs septiembre → mejora > 200 s y > 50 %.
3.  Resumen incidencias → total 12, abiertas 1, resueltas 11.
4.  Resumen movimientos → total 45.
5.  Dashboard → 50 productos, 150 ubicaciones, 1 incidencia abierta.

### Criterio de cierre

**Este es el endpoint de cierre del proyecto**: si el comparativo muestra > 50 % de mejora, el objetivo de Ingeniería Industrial está demostrado.

## 📄 Fase 11.10 — Actualizar hashes de usuarios sintéticos

### Objetivo

Permitir que los usuarios de los datos sintéticos puedan iniciar sesión con la contraseña `Demo1234!`.

### Implementación

Script `backend/scripts/seed_usuarios_password.py` que:

1.  Importe `BcryptPasswordHasher`.
2.  Genere el hash de `Demo1234!`.
3.  Ejecute `UPDATE usuarios SET password_hash = :h`.
4.  Confirme y cierre.

### Verificación

`POST /api/v1/auth/login` con `ana.torres@xyz.com` / `Demo1234!` → 200 y token válido.

### Criterio de cierre

Los 6 usuarios sintéticos pueden autenticarse.