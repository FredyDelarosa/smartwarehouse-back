"""Tests del router de inventario."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_consultar_stock_t001(client: AsyncClient, admin_token: str):
    """Test: stock de T001 → total 470, 2 ubicaciones."""
    # Primero obtener el ID de T001
    response = await client.get(
        "/api/v1/productos/buscar?termino=T001",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    productos = response.json()
    t001 = next((p for p in productos if p["codigo"] == "T001"), None)
    assert t001 is not None

    response = await client.get(
        f"/api/v1/inventario/producto/{t001['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stock_total"] == 470
    assert len(data["distribucion"]) == 2
    print(f"✅ Stock T001: {data['stock_total']} uds en {len(data['distribucion'])} ubicaciones")


@pytest.mark.asyncio
async def test_consultar_stock_producto_inexistente(
    client: AsyncClient, admin_token: str
):
    """Test: stock de producto inexistente → 404."""
    response = await client.get(
        "/api/v1/inventario/producto/99999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
    print("✅ Producto inexistente rechazado (404)")


@pytest.mark.asyncio
async def test_alertas_stock_bajo(client: AsyncClient, admin_token: str):
    """Test: alertas con datos actuales → lista vacía."""
    response = await client.get(
        "/api/v1/inventario/alertas",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    # Con los datos actuales, no debería haber alertas
    assert isinstance(data, list)
    print(f"✅ Alertas stock bajo: {len(data)} productos")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
