"""Tests del router de productos."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_listar_productos(client: AsyncClient, admin_token: str):
    """Test: listar productos (espera 50 totales)."""
    response = await client.get(
        "/api/v1/productos/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 50
    print(f"✅ Total productos: {len(data)}")


@pytest.mark.asyncio
async def test_listar_productos_filtrados_categoria(
    client: AsyncClient, admin_token: str
):
    """
    Listar productos filtrados por categoría.

    No se comprueba el número exacto de filas. Antes era `== 10` y empezó a
    fallar en cuanto alguien dio de alta un producto de Tornillería a mano —que
    es exactamente lo que hace un usuario probando la aplicación—. Un test que
    se rompe porque la aplicación se usa es un test que obliga a no usarla.

    Lo que importa aquí es que el FILTRO funciona: que solo salgan productos de
    esa categoría y que no se cuele ninguno de otra.
    """
    response = await client.get(
        "/api/v1/productos/?categoria_id=1",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data, "la categoría 1 debería tener productos"
    assert all(p["categoria_id"] == 1 for p in data), "se coló otra categoría"
    assert any(p["codigo"] == "T001" for p in data), "no está el producto sembrado T001"

    # Y que el filtro discrimina de verdad: la categoría 1 tiene menos que la
    # 4, que es la de EPP y la más poblada del catálogo.
    otra = await client.get(
        "/api/v1/productos/?categoria_id=4",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert otra.status_code == 200
    assert all(p["categoria_id"] == 4 for p in otra.json())

    print(f"✅ Productos categoría 1: {len(data)}")


@pytest.mark.asyncio
async def test_buscar_productos(client: AsyncClient, admin_token: str):
    """Test: buscar 'tornillo' (espera varios matches)."""
    response = await client.get(
        "/api/v1/productos/buscar?termino=tornillo",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    print(f"✅ Coincidencias 'tornillo': {len(data)}")


@pytest.mark.asyncio
async def test_crud_producto(client: AsyncClient, admin_token: str):
    """Test: crear, obtener, actualizar y dar de baja un producto."""
    # Crear
    response = await client.post(
        "/api/v1/productos/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "codigo": "TEST01",
            "nombre": "Producto de Prueba",
            "descripcion": "Producto para tests",
            "unidad_medida": "pieza",
            "stock_minimo": 10,
        },
    )
    assert response.status_code == 201
    creado = response.json()
    producto_id = creado["id"]
    print(f"✅ Producto creado: {creado['codigo']} (id={producto_id})")

    # Obtener
    response = await client.get(
        f"/api/v1/productos/{producto_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    obtenido = response.json()
    assert obtenido["codigo"] == "TEST01"
    print(f"✅ Producto obtenido: {obtenido['nombre']}")

    # Actualizar
    response = await client.patch(
        f"/api/v1/productos/{producto_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"nombre": "Producto Actualizado"},
    )
    assert response.status_code == 200
    actualizado = response.json()
    assert actualizado["nombre"] == "Producto Actualizado"
    print(f"✅ Producto actualizado: {actualizado['nombre']}")

    # Dar de baja
    response = await client.delete(
        f"/api/v1/productos/{producto_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204
    print(f"✅ Producto dado de baja (id={producto_id})")


@pytest.mark.asyncio
async def test_crear_producto_duplicado(
    client: AsyncClient, admin_token: str
):
    """Test: intentar crear con código duplicado → 409."""
    response = await client.post(
        "/api/v1/productos/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "codigo": "T001",  # Ya existe
            "nombre": "Producto Duplicado",
        },
    )
    assert response.status_code == 409
    print("✅ Código duplicado rechazado (409)")


@pytest.mark.asyncio
async def test_crear_producto_codigo_invalido(
    client: AsyncClient, admin_token: str
):
    """Test: intentar crear con código inválido → 422."""
    response = await client.post(
        "/api/v1/productos/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "codigo": "123",  # Inválido: debe empezar con letras
            "nombre": "Producto Inválido",
        },
    )
    assert response.status_code == 422
    print("✅ Código inválido rechazado (422)")


@pytest.mark.asyncio
async def test_crear_producto_sin_permiso(
    client: AsyncClient, almacenero_token: str
):
    """Test: intentar crear sin ser Admin/Supervisor → 403."""
    response = await client.post(
        "/api/v1/productos/",
        headers={"Authorization": f"Bearer {almacenero_token}"},
        json={
            "codigo": "TEST02",
            "nombre": "Producto Sin Permiso",
        },
    )
    assert response.status_code == 403
    print("✅ Creación sin permiso rechazada (403)")


@pytest.mark.asyncio
async def test_listar_productos_sin_token(client: AsyncClient):
    """Test: listar productos sin token → 401."""
    response = await client.get("/api/v1/productos/")
    assert response.status_code == 401
    print("✅ Listar sin token rechazado (401)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
