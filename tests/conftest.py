"""
Configuración de pytest y fixtures compartidas.

Los tests usan la BD real (MySQL/TiDB Cloud) configurada en .env.
"""

from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Crea un event loop para toda la sesión de tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP asíncrono para los tests."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def admin_token(client: AsyncClient) -> str:
    """Obtiene un token de administrador para los tests."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "ana.torres@xyz.com",
            "password": "Demo1234!",
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
async def supervisor_token(client: AsyncClient) -> str:
    """Obtiene un token de supervisor para los tests."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "carlos.ruiz@xyz.com",
            "password": "Demo1234!",
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
async def almacenero_token(client: AsyncClient) -> str:
    """Obtiene un token de almacenero para los tests."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "luis.mendoza@xyz.com",
            "password": "Demo1234!",
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]
