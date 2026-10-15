"""Caso de uso: carga inicial de stock en varias ubicaciones (PET-4)."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos import (
    CargaInicialDTO,
    CargaInicialResultadoDTO,
    LineaCargaResultadoDTO,
    MovimientoCreateDTO,
)
from app.domain.entities import TipoMovimiento
from app.domain.exceptions import DomainError
from app.domain.repositories import (
    InventarioRepository,
    MovimientoRepository,
    ProductoRepository,
    UbicacionRepository,
)
from app.application.use_cases.movimientos import RegistrarEntradaUseCase


class CargaInicialUseCase:
    """
    Coloca muchas existencias de golpe, una línea por producto y ubicación.

    ## Qué ES y qué NO es

    No es un atajo para registrar movimientos: **cada línea genera un
    movimiento ENTRADA de verdad**, con su usuario, su fecha y su referencia.
    Que el stock aparezca por la carga inicial no significa que su origen sea
    invisible. Un almacén queconcilia inventario necesita que toda entrada de
    stock tenga detrás una operación con fecha y responsable.

    ## Por qué no es todo-o-nada

    Una carga inicial real son doscientas líneas. Si la línea 137 falla porque
    ese producto está dado de baja, no puede ser motivo para que las otras
    199 se queden sin cargar y haya que reescribirlas. Cada línea va en su
    SAVEPOINT: la que falla se deshace sola y las demás siguen.

    ## Por qué este caso de uso recibe la sesión

    Es el único que gestiona la transacción él mismo, porque los savepoints no
    se pueden expresar en un puerto sin inventar una abstracción que nadie
    más necesita. Va documentado aquí para que la excepción no sorprenda.
    """

    def __init__(
        self,
        session: AsyncSession,
        producto_repo: ProductoRepository,
        ubicacion_repo: UbicacionRepository,
        inventario_repo: InventarioRepository,
        movimiento_repo: MovimientoRepository,
    ) -> None:
        self._session = session
        self._entrada = RegistrarEntradaUseCase(
            producto_repo, ubicacion_repo, inventario_repo, movimiento_repo
        )

    async def execute(
        self, dto: CargaInicialDTO, usuario_id: int
    ) -> CargaInicialResultadoDTO:
        referencia = dto.referencia or "CARGA-INICIAL"
        resultados: list[LineaCargaResultadoDTO] = []

        for indice, linea in enumerate(dto.lineas):
            try:
                # El savepoint es lo que permite que esta línea se deshaga sin
                # tocar las anteriores.
                async with self._session.begin_nested():
                    movimiento = await self._entrada.execute(
                        MovimientoCreateDTO(
                            tipo=TipoMovimiento.ENTRADA,
                            producto_id=linea.producto_id,
                            ubicacion_destino_id=linea.ubicacion_id,
                            cantidad=linea.cantidad,
                            referencia=referencia,
                            observaciones=dto.observaciones,
                        ),
                        usuario_id,
                    )
                    movimiento_id = movimiento.id
                resultados.append(
                    LineaCargaResultadoDTO(
                        indice=indice,
                        producto_id=linea.producto_id,
                        ubicacion_id=linea.ubicacion_id,
                        cantidad=linea.cantidad,
                        movimiento_id=movimiento_id,
                        ok=True,
                    )
                )
            except DomainError as exc:
                # Solo se capturan errores de dominio: los de infraestructura
                # (la base no responde) deben propagarse y abortar la carga
                # entera, porque si no se escribirían datos a medias sin que
                # nadie se entere.
                resultados.append(
                    LineaCargaResultadoDTO(
                        indice=indice,
                        producto_id=linea.producto_id,
                        ubicacion_id=linea.ubicacion_id,
                        cantidad=linea.cantidad,
                        ok=False,
                        error=self._mensaje(exc),
                    )
                )

        return CargaInicialResultadoDTO(
            total_lineas=len(dto.lineas),
            registradas=sum(1 for r in resultados if r.ok),
            fallidas=sum(1 for r in resultados if not r.ok),
            movimientos=resultados,
        )

    @staticmethod
    def _mensaje(exc: DomainError) -> str:
        """Mensaje entendible por quien carga el inventario, no por el backend."""
        default = getattr(exc, "default_message", None) or str(exc)
        detalles = getattr(exc, "details", None)
        if not isinstance(detalles, dict) or not detalles:
            return str(default)
        campos = ", ".join(f"{k}={v}" for k, v in detalles.items())
        return f"{default} ({campos})"