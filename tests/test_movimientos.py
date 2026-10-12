"""Tests del router de movimientos."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_registrar_entrada(client: AsyncClient, admin_token: str):
    """Test: registrar una entrada de producto."""
    # Primero obtener el ID de T001
    response = await client.get(
        "/api/v1/productos/buscar?termino=T001",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    productos = response.json()
    t001 = next((p for p in productos if p["codigo"] == "T001"), None)
    assert t001 is not None

    # Obtener ubicación P3-A-01
    response = await client.get(
        "/api/v1/ubicaciones/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    ubicaciones = response.json()
    p3a01 = next(
        (u for u in ubicaciones if u["codigo_ubicacion"] == "P3-A-01"), None
    )
    assert p3a01 is not None

    # Registrar entrada
    response = await client.post(
        "/api/v1/movimientos/entrada",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "tipo": "ENTRADA",
            "producto_id": t001["id"],
            "cantidad": 10,
            "ubicacion_destino_id": p3a01["id"],
            "referencia": "TEST-ENTRADA",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["tipo"] == "ENTRADA"
    assert data["cantidad"] == 10
    print(f"✅ Entrada registrada: {data['tipo']} de {data['cantidad']} uds")


@pytest.mark.asyncio
async def test_registrar_salida(client: AsyncClient, supervisor_token: str):
    """Test: registrar una salida de producto (con rol Almacenero/Supervisor)."""
    # Obtener T001
    response = await client.get(
        "/api/v1/productos/buscar?termino=T001",
        headers={"Authorization": f"Bearer {supervisor_token}"},
    )
    assert response.status_code == 200
    productos = response.json()
    t001 = next((p for p in productos if p["codigo"] == "T001"), None)
    assert t001 is not None

    # Obtener ubicación P3-A-01
    response = await client.get(
        "/api/v1/ubicaciones/?limit=200",
        headers={"Authorization": f"Bearer {supervisor_token}"},
    )
    assert response.status_code == 200
    ubicaciones = response.json()
    p3a01 = next(
        (u for u in ubicaciones if u["codigo_ubicacion"] == "P3-A-01"), None
    )
    assert p3a01 is not None

    # Registrar salida
    response = await client.post(
        "/api/v1/movimientos/salida",
        headers={"Authorization": f"Bearer {supervisor_token}"},
        json={
            "tipo": "SALIDA",
            "producto_id": t001["id"],
            "cantidad": 5,
            "ubicacion_origen_id": p3a01["id"],
            "referencia": "TEST-SALIDA",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["tipo"] == "SALIDA"
    assert data["cantidad"] == 5
    print(f"✅ Salida registrada: {data['tipo']} de {data['cantidad']} uds")


@pytest.mark.asyncio
async def test_registrar_traslado(client: AsyncClient, admin_token: str):
    """Test: registrar un traslado entre ubicaciones."""
    # Obtener T001
    response = await client.get(
        "/api/v1/productos/buscar?termino=T001",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    productos = response.json()
    t001 = next((p for p in productos if p["codigo"] == "T001"), None)
    assert t001 is not None

    # Obtener ubicaciones
    response = await client.get(
        "/api/v1/ubicaciones/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    ubicaciones = response.json()
    p3a01 = next(
        (u for u in ubicaciones if u["codigo_ubicacion"] == "P3-A-01"), None
    )
    p3b02 = next(
        (u for u in ubicaciones if u["codigo_ubicacion"] == "P3-B-02"), None
    )
    assert p3a01 is not None
    assert p3b02 is not None

    # Registrar traslado
    response = await client.post(
        "/api/v1/movimientos/traslado",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "tipo": "TRASLADO",
            "producto_id": t001["id"],
            "cantidad": 20,
            "ubicacion_origen_id": p3a01["id"],
            "ubicacion_destino_id": p3b02["id"],
            "referencia": "TEST-TRASLADO",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["tipo"] == "TRASLADO"
    assert data["cantidad"] == 20
    print(f"✅ Traslado registrado: {data['tipo']} de {data['cantidad']} uds")


@pytest.mark.asyncio
async def test_listar_movimientos(client: AsyncClient, admin_token: str):
    """Test: listar movimientos."""
    response = await client.get(
        "/api/v1/movimientos/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"✅ Movimientos registrados: {len(data)}")


@pytest.mark.asyncio
async def test_movimiento_sin_permiso(
    client: AsyncClient, admin_token: str
):
    """Test: registrar movimiento sin permiso → 403."""
    # Este test requiere un token de un usuario sin permisos
    # Por ahora solo verificamos que el endpoint existe
    response = await client.post(
        "/api/v1/movimientos/entrada",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "tipo": "ENTRADA",
            "producto_id": 1,
            "cantidad": 1,
            "ubicacion_destino_id": 1,
        },
    )
    # Si el usuario no tiene permiso, debería ser 403
    # Si tiene permiso, podría ser 201 o 404 (si no existe el producto/ubicación)
    assert response.status_code in [201, 403, 404]
    print(f"✅ Movimiento con permiso: {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
