"""
Configuración de pytest y fixtures compartidas.

## Los tests corren contra una base de datos APARTE

No es una preferencia: es la única forma de que ejecutar `pytest` no destruya
los datos de la aplicación.

La suite es de integración (pega contra la app entera por `ASGITransport`) y
había una época en que `POST /movimientos/entrada` no hacía `commit`, así que sus
escrituras se descartaban solas y tests y base real no se pisaban. Al arreglar
los commits, esa protección accidental desapareció: ahora cada `pytest` suma
movimientos, crea productos y baja stock **de verdad**. Sin este aislamiento, el
primer test que pasara reventaba el stock de producción.

Así que el arrangement es: cada test corre dentro de una transacción que se
deshace al terminar. Como las rutas llaman a `session.commit()`, la transacción
no se puede dejar pasar; de ahí `SesionDeTest`, que traduce `commit()` en un
`flush()` y descarta al final.
"""

from __future__ import annotations

from typing import Any, AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import (
    AsyncSessionLocal,
    engine,
    get_session,
)
from app.main import app


# ============================================================
# Sesión que no confirma nada
# ============================================================
class SesionDeTest:
    """
    Envoltorio de `AsyncSession` que convierte `commit()` en `flush()`.

    El objetivo es que la escritura llegue a la conexión —para que las
    validaciones y los `refresh()` se comporten igual que en producción— pero
    que nunca llegue a confirmarse. Al cerrar la transacción exterior, MySQL la
    deshace y la base queda como estaba.

    Se usa `__getattr__` para delegar todo lo demás (`add`, `scalar`, `execute`,
    `refresh`...) en la sesión real: no hay que ir replicando la API a mano.
    """

    def __init__(self, sesion: AsyncSession) -> None:
        self._sesion = sesion

    async def commit(self) -> None:
        """No confirma: solo vuelca lo pendiente en la transacción abierta."""
        await self._sesion.flush()

    async def rollback(self) -> None:
        await self._sesion.rollback()

    def __getattr__(self, nombre: str) -> Any:
        return getattr(self._sesion, nombre)


@pytest.fixture
async def sesion_de_test() -> AsyncGenerator[SesionDeTest, None]:
    """
    Transacción desechable para un test.

    Al terminar se **descarta el pool** además de deshacer la transacción.
    Sin eso, el pool del engine (de scope de sesión) sobrevive entre tests,
    cada uno con su propio event loop, y la segunda conexión reutilizada aparece
    atada al loop anterior: pytest falla con "got Future attached to a different
    loop". Descartarlo cuesta una conexión por test y elimina el problema de
    raíz en vez de pelearse con su síntoma.
    """
    sesion = AsyncSessionLocal()
    transaccion = await sesion.begin()
    try:
        yield SesionDeTest(sesion)
    finally:
        await transaccion.rollback()
        await sesion.close()
        await engine.dispose()


@pytest.fixture
async def client(sesion_de_test: SesionDeTest) -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP asíncrono contra la app, con la sesión de test inyectada."""
    app.dependency_overrides[get_session] = lambda: sesion_de_test
    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
    finally:
        app.dependency_overrides.pop(get_session, None)


# ============================================================
# Tokens
# ============================================================
async def _token(client: AsyncClient, email: str) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Demo1234!"},
    )
    assert response.status_code == 200, f"login falló para {email}: {response.text}"
    return response.json()["access_token"]


@pytest.fixture
async def admin_token(client: AsyncClient) -> str:
    """Token de administrador (ana.torres@xyz.com)."""
    return await _token(client, "ana.torres@xyz.com")


@pytest.fixture
async def supervisor_token(client: AsyncClient) -> str:
    """Token de supervisor (carlos.ruiz@xyz.com)."""
    return await _token(client, "carlos.ruiz@xyz.com")


@pytest.fixture
async def almacenero_token(client: AsyncClient) -> str:
    """Token de almacenero (luis.mendoza@xyz.com)."""
    return await _token(client, "luis.mendoza@xyz.com")
