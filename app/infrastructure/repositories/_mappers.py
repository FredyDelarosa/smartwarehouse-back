"""
Mappers ORM ↔ Entidad.

Convertidores puros, sin lógica de negocio. Cada entidad del dominio
tiene dos funciones:
  - `X_to_entity(model)`        → ORM a Entidad
  - `apply_X(entity, model)`    → copia los campos de la Entidad al ORM

Regla: NUNCA acceder a relaciones desde aquí. Si una entidad tiene
relación (ej. Usuario.rol), se carga explícitamente desde el repositorio
y se asigna después de construir la entidad.
"""

from __future__ import annotations

from app.domain.entities import (
    Almacen,
    Busqueda,
    Categoria,
    Incidencia,
    Inventario,
    Movimiento,
    Producto,
    Rol,
    Ubicacion,
    Usuario,
)
from app.infrastructure.database.models import (
    AlmacenModel,
    BusquedaModel,
    CategoriaModel,
    IncidenciaModel,
    InventarioModel,
    MovimientoModel,
    ProductoModel,
    RolModel,
    UbicacionModel,
    UsuarioModel,
)


# ============================================================
# Rol
# ============================================================
def rol_to_entity(m: RolModel) -> Rol:
    return Rol(
        id=m.id,
        nombre=m.nombre,
        descripcion=m.descripcion,
        created_at=m.created_at,
    )


def apply_rol(e: Rol, m: RolModel) -> None:
    m.nombre = e.nombre
    m.descripcion = e.descripcion


# ============================================================
# Usuario
# ============================================================
def usuario_to_entity(m: UsuarioModel, *, include_rol: bool = False) -> Usuario:
    rol = None
    if include_rol and m.rol is not None:
        rol = rol_to_entity(m.rol)
    return Usuario(
        id=m.id,
        nombre=m.nombre,
        email=m.email,
        password_hash=m.password_hash,
        rol_id=m.rol_id,
        activo=m.activo,
        almacen_id=m.almacen_id,
        fecha_creacion=m.fecha_creacion,
        ultimo_acceso=m.ultimo_acceso,
        rol=rol,
    )


def apply_usuario(e: Usuario, m: UsuarioModel) -> None:
    m.nombre = e.nombre
    m.email = e.email
    m.password_hash = e.password_hash
    m.rol_id = e.rol_id
    m.activo = e.activo
    m.almacen_id = e.almacen_id
    m.ultimo_acceso = e.ultimo_acceso


# ============================================================
# Almacen
# ============================================================
def almacen_to_entity(m: AlmacenModel) -> Almacen:
    return Almacen(
        id=m.id,
        nombre=m.nombre,
        direccion=m.direccion,
        activo=m.activo,
        created_at=m.created_at,
    )


def apply_almacen(e: Almacen, m: AlmacenModel) -> None:
    m.nombre = e.nombre
    m.direccion = e.direccion
    m.activo = e.activo
    # Sin `almacen_id`: un almacén no pertenece a un almacén. La línea estaba
    # aquí como resto de un intento de multialmacén y hacía que TODO alta de
    # almacén fallara con AttributeError.


# ============================================================
# Categoria
# ============================================================
def categoria_to_entity(m: CategoriaModel) -> Categoria:
    return Categoria(
        id=m.id,
        nombre=m.nombre,
        descripcion=m.descripcion,
        activo=m.activo,
        created_at=m.created_at,
    )


def apply_categoria(e: Categoria, m: CategoriaModel) -> None:
    m.nombre = e.nombre
    m.descripcion = e.descripcion
    m.activo = e.activo
    # Sin `almacen_id`: las categorías son taxonomía compartida. Mismo origen
    # que en `apply_almacen` — la línea hacía que POST /categorias devolviera
    # 500 con AttributeError, no un error de validación.


# ============================================================
# Producto
# ============================================================
def producto_to_entity(m: ProductoModel) -> Producto:
    return Producto(
        id=m.id,
        codigo=m.codigo,
        nombre=m.nombre,
        descripcion=m.descripcion,
        categoria_id=m.categoria_id,
        unidad_medida=m.unidad_medida,
        stock_minimo=m.stock_minimo,
        foto_url=m.foto_url,
        activo=m.activo,
        almacen_id=m.almacen_id,
        fecha_creacion=m.fecha_creacion,
        fecha_actualizacion=m.fecha_actualizacion,
    )


def apply_producto(e: Producto, m: ProductoModel) -> None:
    m.codigo = e.codigo
    m.nombre = e.nombre
    m.descripcion = e.descripcion
    m.categoria_id = e.categoria_id
    m.unidad_medida = e.unidad_medida
    m.stock_minimo = e.stock_minimo
    m.foto_url = e.foto_url
    m.activo = e.activo
    m.almacen_id = e.almacen_id


# ============================================================
# Ubicacion
# ============================================================
def ubicacion_to_entity(m: UbicacionModel) -> Ubicacion:
    return Ubicacion(
        id=m.id,
        almacen_id=m.almacen_id,
        pasillo=m.pasillo,
        estante=m.estante,
        nivel=m.nivel,
        codigo_ubicacion=m.codigo_ubicacion,
        codigo_qr=m.codigo_qr,
        coordenada_x=m.coordenada_x,
        coordenada_y=m.coordenada_y,
        activo=m.activo,
        created_at=m.created_at,
    )


def apply_ubicacion(e: Ubicacion, m: UbicacionModel) -> None:
    m.almacen_id = e.almacen_id
    m.pasillo = e.pasillo
    m.estante = e.estante
    m.nivel = e.nivel
    m.codigo_ubicacion = e.codigo_ubicacion
    m.codigo_qr = e.codigo_qr
    m.coordenada_x = e.coordenada_x
    m.coordenada_y = e.coordenada_y
    m.activo = e.activo
    # `almacen_id` ya se asigna la primera línea de esta función. Estaba
    # duplicado al final; inofensivo, pero una línea que sugiere que el valor
    # importa más de lo que parece cuando se lee el mapper entero.


# ============================================================
# Inventario
# ============================================================
def inventario_to_entity(m: InventarioModel) -> Inventario:
    return Inventario(
        id=m.id,
        producto_id=m.producto_id,
        ubicacion_id=m.ubicacion_id,
        cantidad=m.cantidad,
        fecha_actualizacion=m.fecha_actualizacion,
    )


def apply_inventario(e: Inventario, m: InventarioModel) -> None:
    m.producto_id = e.producto_id
    m.ubicacion_id = e.ubicacion_id
    m.cantidad = e.cantidad


# ============================================================
# Movimiento
# ============================================================
def movimiento_to_entity(m: MovimientoModel) -> Movimiento:
    return Movimiento(
        id=m.id,
        tipo=m.tipo,
        producto_id=m.producto_id,
        ubicacion_origen_id=m.ubicacion_origen_id,
        ubicacion_destino_id=m.ubicacion_destino_id,
        cantidad=m.cantidad,
        usuario_id=m.usuario_id,
        fecha=m.fecha,
        referencia=m.referencia,
        observaciones=m.observaciones,
    )


def apply_movimiento(e: Movimiento, m: MovimientoModel) -> None:
    m.tipo = e.tipo
    m.producto_id = e.producto_id
    m.ubicacion_origen_id = e.ubicacion_origen_id
    m.ubicacion_destino_id = e.ubicacion_destino_id
    m.cantidad = e.cantidad
    m.usuario_id = e.usuario_id
    m.referencia = e.referencia
    m.observaciones = e.observaciones


# ============================================================
# Busqueda
# ============================================================
def busqueda_to_entity(m: BusquedaModel) -> Busqueda:
    return Busqueda(
        id=m.id,
        usuario_id=m.usuario_id,
        producto_id=m.producto_id,
        producto_nombre=None,  # Se asigna en el repositorio con JOIN
        termino_busqueda=m.termino_busqueda,
        fecha_hora_inicio=m.fecha_hora_inicio,
        fecha_hora_fin=m.fecha_hora_fin,
        tiempo_busqueda_segundos=m.tiempo_busqueda_segundos,
        ubicacion_encontrada_id=m.ubicacion_encontrada_id,
        exito=m.exito,
        observaciones=m.observaciones,
    )


def apply_busqueda(e: Busqueda, m: BusquedaModel) -> None:
    m.usuario_id = e.usuario_id
    m.producto_id = e.producto_id
    m.termino_busqueda = e.termino_busqueda
    m.fecha_hora_inicio = e.fecha_hora_inicio
    m.fecha_hora_fin = e.fecha_hora_fin
    m.tiempo_busqueda_segundos = e.tiempo_busqueda_segundos
    m.ubicacion_encontrada_id = e.ubicacion_encontrada_id
    m.exito = e.exito
    m.observaciones = e.observaciones


# ============================================================
# Incidencia
# ============================================================
def incidencia_to_entity(m: IncidenciaModel) -> Incidencia:
    return Incidencia(
        id=m.id,
        tipo=m.tipo,
        producto_id=m.producto_id,
        ubicacion_id=m.ubicacion_id,
        usuario_id=m.usuario_id,
        fecha=m.fecha,
        descripcion=m.descripcion,
        resuelta=m.resuelta,
        fecha_resolucion=m.fecha_resolucion,
    )


def apply_incidencia(e: Incidencia, m: IncidenciaModel) -> None:
    m.tipo = e.tipo
    m.producto_id = e.producto_id
    m.ubicacion_id = e.ubicacion_id
    m.usuario_id = e.usuario_id
    m.descripcion = e.descripcion
    m.resuelta = e.resuelta
    m.fecha_resolucion = e.fecha_resolucion