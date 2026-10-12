"""Tests del router de métricas."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_tiempo_promedio_busqueda(client: AsyncClient, admin_token: str):
    """Test: tiempo promedio global > 50 búsquedas, promedio > 0."""
    response = await client.get(
        "/api/v1/metricas/tiempo-promedio",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_busquedas"] > 50
    assert data["promedio_segundos"] > 0
    print(f"✅ Tiempo promedio: {data['promedio_segundos']}s")
    print(f"   Total búsquedas: {data['total_busquedas']}")


@pytest.mark.asyncio
async def test_comparativa_busquedas(client: AsyncClient, admin_token: str):
    """Test: comparativa julio vs septiembre → mejora > 200 s y > 50 %."""
    response = await client.get(
        "/api/v1/metricas/comparativa",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={
            "desde_anterior": "2024-07-01T00:00:00",
            "hasta_anterior": "2024-07-31T23:59:59",
            "desde_actual": "2024-09-01T00:00:00",
            "hasta_actual": "2024-09-30T23:59:59",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mejora_segundos"] > 200
    assert data["mejora_porcentaje"] > 50
    print(f"✅ Comparativa: mejora de {data['mejora_segundos']}s ({data['mejora_porcentaje']}%)")


@pytest.mark.asyncio
async def test_resumen_incidencias(client: AsyncClient, admin_token: str):
    """Test: resumen incidencias → total 12, abiertas 1, resueltas 11."""
    response = await client.get(
        "/api/v1/metricas/incidencias",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 12
    assert data["abiertas"] == 1
    assert data["resueltas"] == 11
    print(f"✅ Resumen incidencias: {data['total']} total, {data['abiertas']} abiertas, {data['resueltas']} resueltas")


@pytest.mark.asyncio
async def test_resumen_movimientos(client: AsyncClient, admin_token: str):
    """Test: resumen movimientos → total 45."""
    response = await client.get(
        "/api/v1/metricas/movimientos",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 45
    print(f"✅ Resumen movimientos: {data['total']}")


@pytest.mark.asyncio
async def test_dashboard(client: AsyncClient, admin_token: str):
    """Test: dashboard → 50 productos, 150 ubicaciones, 1 incidencia abierta."""
    response = await client.get(
        "/api/v1/metricas/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_productos"] == 50
    assert data["total_ubicaciones"] == 150
    assert data["total_incidencias_abiertas"] == 1
    print(f"✅ Dashboard: {data['total_productos']} productos, {data['total_ubicaciones']} ubicaciones")
    print(f"   Incidencias abiertas: {data['total_incidencias_abiertas']}")
    print(f"   Tiempo promedio búsqueda: {data['tiempo_promedio_busqueda_segundos']}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
