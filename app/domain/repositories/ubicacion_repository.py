"""Puerto: UbicacionRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Ubicacion


class UbicacionRepository(ABC):
    """Contrato de acceso a datos para ubicaciones físicas."""

    @abstractmethod
    async def get_by_id(self, ubicacion_id: int) -> Optional[Ubicacion]: ...

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> Optional[Ubicacion]:
        """Busca por código de ubicación, ej. 'P3-B-02'."""
        ...

    @abstractmethod
    async def get_by_qr(self, codigo_qr: str) -> Optional[Ubicacion]:
        """Busca por el contenido del código QR escaneado."""
        ...

    # OJO: este método tiene que declararse ANTES que `list` de más abajo.
    # El cuerpo de la clase se ejecuta de arriba abajo y, a partir de ahí,
    # `list` pasa a ser el método de la clase: las anotaciones que dicen
    # `list[Ubicacion]` dejan de resolverse y saltan
    # "TypeError: 'function' object is not subscriptable".
    async def create_many(
        self, ubicaciones: list[Ubicacion], *, almacen_id: int
    ) -> list[Ubicacion]:
        """
        Inserta varias filas de una vez y devuelve las entidades con su id.

        Existe para la generación del cuestionario, que puede crear cientos de
        ubicaciones de golpe. Ir de una en una serían cientos de viajes de
        ida y vuelta por red contra TiDB Cloud, que no es local.

        `almacen_id` es explícito y NO se deduce de la entidad: quien genera
        decide a qué almacén va, y el repositorio comprueba que sea el suyo.
        """
        ...

    @abstractmethod
    async def list_by_almacen(
        self,
        almacen_id: int,
        *,
        solo_activas: bool = True,
    ) -> list[Ubicacion]: ...

    @abstractmethod
    async def list(self, *, skip: int = 0, limit: int = 100) -> list[Ubicacion]: ...

    @abstractmethod
    async def create(self, ubicacion: Ubicacion) -> Ubicacion: ...

    @abstractmethod
    async def update(self, ubicacion: Ubicacion) -> Ubicacion: ...

    @abstractmethod
    async def delete(self, ubicacion_id: int) -> None: ...