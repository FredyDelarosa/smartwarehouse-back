"""Tests del router de búsquedas."""

from __future__ import annotations

import asyncio

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_iniciar_busqueda(client: AsyncClient, admin_token: str):
    """Test: iniciar búsqueda 'Tornillos 1/4' → devuelve busqueda_id, producto T001, total 470, 2 ubicaciones."""
    response = await client.post(
        "/api/v1/busquedas/iniciar",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"termino_busqueda": "Tornillos 1/4"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["busqueda_id"] is not None
    assert data["producto"]["codigo"] == "T001"
    assert data["stock_total"] == 470
    assert len(data["ubicaciones"]) == 2
    print(f"✅ Búsqueda iniciada: id={data['busqueda_id']}")
    print(f"   Producto: {data['producto']['nombre']}")
    print(f"   Stock total: {data['stock_total']}")
    print(f"   Ubicaciones: {len(data['ubicaciones'])}")


@pytest.mark.asyncio
async def test_finalizar_busqueda(client: AsyncClient, admin_token: str):
    """Test: finalizar búsqueda con ubicación P3-A-01 → exito=true, tiempo_segundos>=1."""
    # Iniciar búsqueda
    response = await client.post(
        "/api/v1/busquedas/iniciar",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"termino_busqueda": "Tornillos 1/4"},
    )
    assert response.status_code == 201
    data = response.json()
    busqueda_id = data["busqueda_id"]

    # Esperar 1.2 segundos
    await asyncio.sleep(1.2)

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

    # Finalizar búsqueda
    response = await client.post(
        f"/api/v1/busquedas/{busqueda_id}/finalizar",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"ubicacion_encontrada_id": p3a01["id"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["exito"] is True
    assert data["tiempo_busqueda_segundos"] >= 1
    print(f"✅ Búsqueda finalizada: exito={data['exito']}")
    print(f"   Tiempo: {data['tiempo_busqueda_segundos']}s")


@pytest.mark.asyncio
async def test_iniciar_busqueda_sin_match(
    client: AsyncClient, admin_token: str
):
    """Test: iniciar búsqueda que no matchea → 404."""
    response = await client.post(
        "/api/v1/busquedas/iniciar",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"termino_busqueda": "PRODUCTO_INEXISTENTE_XYZ"},
    )
    assert response.status_code == 404
    print("✅ Búsqueda sin match rechazada (404)")


@pytest.mark.asyncio
async def test_historial_busquedas(client: AsyncClient, admin_token: str):
    """Test: historial → incluye las 2 búsquedas recientes."""
    response = await client.get(
        "/api/v1/busquedas/historial",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    print(f"✅ Historial búsquedas: {len(data)} registros")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
