"""Tests de la carga inicial (PET-4).

La parte que merece test no es el camino feliz —que es el mismo
`RegistrarEntradaUseCase` de siempre— sino el **fallo parcial**: que una
línea mala no arrastre a las demás. Es el comportamiento que evita que
cargar doscientas líneas sea «todo o nada».
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient


async def _primer_producto(client: AsyncClient, token: str) -> dict:
    r = await client.get(
        "/api/v1/productos/?limit=5",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    productos = r.json()
    assert productos, "el catálogo sembrado debería tener productos"
    return productos[0]


async def _primeras_ubicaciones(client: AsyncClient, token: str, n: int) -> list[int]:
    r = await client.get(
        f"/api/v1/ubicaciones/?limit={n}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    return [u["id"] for u in r.json()]


@pytest.mark.asyncio
async def test_carga_inicial_todas_validas(client: AsyncClient, admin_token: str):
    """Varias líneas correctas se cargan y suman stock."""
    producto = await _primer_producto(client, admin_token)
    ubicaciones = await _primeras_ubicaciones(client, admin_token, 2)

    antes = await client.get(
        f"/api/v1/inventario/producto/{producto['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    stock_antes = antes.json()["stock_total"]

    r = await client.post(
        "/api/v1/inventario/carga-inicial",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "referencia": "TEST-CARGA",
            "lineas": [
                {"producto_id": producto["id"], "ubicacion_id": ubicaciones[0], "cantidad": 7},
                {"producto_id": producto["id"], "ubicacion_id": ubicaciones[1], "cantidad": 3},
            ],
        },
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["total_lineas"] == 2
    assert data["registradas"] == 2
    assert data["fallidas"] == 0
    assert all(m["ok"] for m in data["movimientos"])
    assert all(m["movimiento_id"] is not None for m in data["movimientos"])

    # El stock se escribe de verdad: es la prueba de que hay commit.
    despues = await client.get(
        f"/api/v1/inventario/producto/{producto['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert despues.json()["stock_total"] == stock_antes + 10


@pytest.mark.asyncio
async def test_carga_inicial_una_linea_mala_no_arrastra_a_las_demas(
    client: AsyncClient, admin_token: str
):
    """
    Una línea con un producto inexistente falla; las otras se cargan igual.

    Cada línea va en su SAVEPOINT: es lo que evita que un solo dato malo
    deje sin cargar las demás. Si este test falla, alguien ha quitado el
    `begin_nested` y ha vuelto el todo-o-nada.
    """
    producto = await _primer_producto(client, admin_token)
    ubicaciones = await _primeras_ubicaciones(client, admin_token, 2)

    antes = await client.get(
        f"/api/v1/inventario/producto/{producto['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    stock_antes = antes.json()["stock_total"]

    r = await client.post(
        "/api/v1/inventario/carga-inicial",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "lineas": [
                {"producto_id": producto["id"], "ubicacion_id": ubicaciones[0], "cantidad": 4},
                {"producto_id": 999_999_999, "ubicacion_id": ubicaciones[1], "cantidad": 4},
                {"producto_id": producto["id"], "ubicacion_id": ubicaciones[1], "cantidad": 6},
            ]
        },
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["total_lineas"] == 3
    assert data["registradas"] == 2, "las dos líneas buenas deben registrarse"
    assert data["fallidas"] == 1

    fallida = next(m for m in data["movimientos"] if not m["ok"])
    assert fallida["indice"] == 1
    assert fallida["movimiento_id"] is None
    # El mensaje va para quien carga inventario, no para el backend.
    assert "no encontrado" in (fallida["error"] or "").lower()

    despues = await client.get(
        f"/api/v1/inventario/producto/{producto['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert despues.json()["stock_total"] == stock_antes + 10, (
        "solo deben contar las dos líneas válidas"
    )


@pytest.mark.asyncio
async def test_carga_inicial_rechaza_lineas_duplicadas(client: AsyncClient, admin_token: str):
    """Producto + ubicación repetidos en la misma carga → 422, antes de escribir."""
    producto = await _primer_producto(client, admin_token)
    ubicaciones = await _primeras_ubicaciones(client, admin_token, 1)

    antes = await client.get(
        f"/api/v1/inventario/producto/{producto['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    stock_antes = antes.json()["stock_total"]

    r = await client.post(
        "/api/v1/inventario/carga-inicial",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "lineas": [
                {"producto_id": producto["id"], "ubicacion_id": ubicaciones[0], "cantidad": 5},
                {"producto_id": producto["id"], "ubicacion_id": ubicaciones[0], "cantidad": 3},
            ]
        },
    )
    assert r.status_code == 422

    despues = await client.get(
        f"/api/v1/inventario/producto/{producto['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert despues.json()["stock_total"] == stock_antes, "no debe escribirse nada"


@pytest.mark.asyncio
async def test_carga_inicial_exige_permiso(
    client: AsyncClient, almacenero_token: str, supervisor_token: str
):
    """Un Almacenero no puede; un Supervisor sí."""
    producto = await _primer_producto(client, supervisor_token)
    ubicaciones = await _primeras_ubicaciones(client, supervisor_token, 1)
    payload = {
        "lineas": [
            {"producto_id": producto["id"], "ubicacion_id": ubicaciones[0], "cantidad": 1}
        ]
    }

    r = await client.post(
        "/api/v1/inventario/carga-inicial",
        headers={"Authorization": f"Bearer {almacenero_token}"},
        json=payload,
    )
    assert r.status_code == 403

    r = await client.post(
        "/api/v1/inventario/carga-inicial",
        headers={"Authorization": f"Bearer {supervisor_token}"},
        json=payload,
    )
    assert r.status_code == 201, r.text