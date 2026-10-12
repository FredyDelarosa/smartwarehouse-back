"""Tests del router de ubicaciones."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_listar_ubicaciones(client: AsyncClient, admin_token: str):
    """Test: listar ubicaciones (espera 150 con límite extendido)."""
    response = await client.get(
        "/api/v1/ubicaciones/?limit=200",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 150
    print(f"✅ Total ubicaciones: {len(data)}")


@pytest.mark.asyncio
async def test_crear_ubicacion(client: AsyncClient, admin_token: str):
    """Test: crear ubicación con código P9-Z-99."""
    response = await client.post(
        "/api/v1/ubicaciones/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "almacen_id": 1,
            "pasillo": "P9",
            "estante": "Z",
            "nivel": "99",
            "codigo_ubicacion": "P9-Z-99",
            "codigo_qr": "QR-P9-Z-99",
        },
    )
    assert response.status_code == 201
    creada = response.json()
    assert creada["codigo_ubicacion"] == "P9-Z-99"
    print(f"✅ Ubicación creada: {creada['codigo_ubicacion']}")

    # Verificar duplicado → 409
    response = await client.post(
        "/api/v1/ubicaciones/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "almacen_id": 1,
            "pasillo": "P9",
            "estante": "Z",
            "nivel": "99",
            "codigo_ubicacion": "P9-Z-99",
        },
    )
    assert response.status_code == 409
    print("✅ Ubicación duplicada rechazada (409)")

    # Código inválido → 422
    response = await client.post(
        "/api/v1/ubicaciones/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "almacen_id": 1,
            "pasillo": "P9",
            "estante": "Z",
            "nivel": "99",
            "codigo_ubicacion": "INVALIDO",
        },
    )
    assert response.status_code == 422
    print("✅ Código inválido rechazado (422)")


@pytest.mark.asyncio
async def test_escanear_qr(client: AsyncClient, admin_token: str):
    """Test: escanear QR-P3-A-01 → devuelve ubicación + T001 (350 uds)."""
    response = await client.get(
        "/api/v1/ubicaciones/qr/QR-P3-A-01",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ubicacion"]["codigo_ubicacion"] == "P3-A-01"
    # Buscar T001 en los productos
    t001 = next(
        (p for p in data["productos"] if p["codigo"] == "T001"), None
    )
    assert t001 is not None
    assert t001["cantidad"] == 350
    print(f"✅ QR escaneado: {data['ubicacion']['codigo_ubicacion']}")
    print(f"   Producto T001: {t001['cantidad']} uds")


@pytest.mark.asyncio
async def test_escanear_qr_inexistente(client: AsyncClient, admin_token: str):
    """Test: escanear QR inexistente → 404."""
    response = await client.get(
        "/api/v1/ubicaciones/qr/QR-INEXISTENTE",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
    print("✅ QR inexistente rechazado (404)")


@pytest.mark.asyncio
async def test_listar_ubicaciones_por_almacen(
    client: AsyncClient, admin_token: str
):
    """Test: listar ubicaciones de un almacén."""
    response = await client.get(
        "/api/v1/ubicaciones/almacen/1",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    print(f"✅ Ubicaciones almacén 1: {len(data)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
