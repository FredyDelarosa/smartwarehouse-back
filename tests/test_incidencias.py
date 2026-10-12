"""Tests del router de incidencias."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_listar_incidencias(client: AsyncClient, admin_token: str):
    """Test: listar todas (espera 12)."""
    response = await client.get(
        "/api/v1/incidencias/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 12
    print(f"✅ Total incidencias: {len(data)}")


@pytest.mark.asyncio
async def test_listar_incidencias_filtradas(
    client: AsyncClient, admin_token: str
):
    """Test: filtrar por tipo."""
    # MAL_UBICADO (5)
    response = await client.get(
        "/api/v1/incidencias/?tipo=MAL_UBICADO",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    print(f"✅ Incidencias MAL_UBICADO: {len(data)}")

    # FALTANTE (3)
    response = await client.get(
        "/api/v1/incidencias/?tipo=FALTANTE",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    print(f"✅ Incidencias FALTANTE: {len(data)}")

    # DANADO (3)
    response = await client.get(
        "/api/v1/incidencias/?tipo=DANADO",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    print(f"✅ Incidencias DANADO: {len(data)}")

    # OTRO (1)
    response = await client.get(
        "/api/v1/incidencias/?tipo=OTRO",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    print(f"✅ Incidencias OTRO: {len(data)}")


@pytest.mark.asyncio
async def test_listar_incidencias_abiertas(
    client: AsyncClient, admin_token: str
):
    """Test: filtrar por resuelta=false (1)."""
    response = await client.get(
        "/api/v1/incidencias/?resuelta=false",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    print(f"✅ Incidencias abiertas: {len(data)}")


@pytest.mark.asyncio
async def test_crear_y_resolver_incidencia(
    client: AsyncClient, admin_token: str
):
    """Test: crear nueva, resolverla, intentar resolverla de nuevo → 422."""
    # Crear
    response = await client.post(
        "/api/v1/incidencias/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "tipo": "OTRO",
            "descripcion": "Incidencia de prueba para tests",
        },
    )
    assert response.status_code == 201
    creada = response.json()
    incidencia_id = creada["id"]
    print(f"✅ Incidencia creada: id={incidencia_id}")

    # Resolver
    response = await client.post(
        f"/api/v1/incidencias/{incidencia_id}/resolver",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    resuelta = response.json()
    assert resuelta["resuelta"] is True
    print(f"✅ Incidencia resuelta: id={incidencia_id}")

    # Intentar resolver de nuevo → 422
    response = await client.post(
        f"/api/v1/incidencias/{incidencia_id}/resolver",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422
    print("✅ Resolución duplicada rechazada (422)")


@pytest.mark.asyncio
async def test_crear_incidencia_producto_inexistente(
    client: AsyncClient, admin_token: str
):
    """Test: producto inexistente → 404."""
    response = await client.post(
        "/api/v1/incidencias/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "tipo": "FALTANTE",
            "producto_id": 99999,
            "descripcion": "Producto inexistente",
        },
    )
    assert response.status_code == 404
    print("✅ Producto inexistente rechazado (404)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
