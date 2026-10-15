"""DTOs: carga inicial de stock (PET-4)."""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class LineaCargaInicialDTO(BaseModel):
    """Un producto y la cantidad que se coloca en una ubicación."""

    producto_id: int
    ubicacion_id: int
    cantidad: int = Field(..., ge=1, le=1_000_000)


class CargaInicialDTO(BaseModel):
    """
    Todas las líneas de una carga inicial, en una sola operación.

    Se manda todo junto y no línea a línea porque una carga inicial de un
    almacén de verdad son cientos de productos, y hacerlos de uno en uno
    serían cientos de viajes de red y, peor, una transacción por unidad.
    """

    lineas: list[LineaCargaInicialDTO] = Field(..., min_length=1, max_length=1000)
    referencia: str | None = Field(None, max_length=64)
    observaciones: str | None = Field(None, max_length=255)

    @model_validator(mode="after")
    def _sin_duplicados(self) -> "CargaInicialDTO":
        """
        Prohíbe repetir producto + ubicación en la misma carga.

        Admitido, no daría error: las dos líneas se sumarían y el resultado
        sería correcto. Pero es casi siempre una equivocación al teclear, y
        avisar en el momento es más barato que descubrirlo al contar el stock.
        """
        vistas: set[tuple[int, int]] = set()
        repetidas: set[tuple[int, int]] = set()
        for l in self.lineas:
            clave = (l.producto_id, l.ubicacion_id)
            if clave in vistas:
                repetidas.add(clave)
            vistas.add(clave)
        if repetidas:
            detalle = ", ".join(f"producto {p} en ubicación {u}" for p, u in sorted(repetidas))
            raise ValueError(
                "Estas líneas repiten producto y ubicación, y se sumarían: "
                f"{detalle}. Deja una sola por combinación."
            )
        return self


class LineaCargaResultadoDTO(BaseModel):
    """Qué pasó con una línea concreta."""

    indice: int
    producto_id: int
    ubicacion_id: int
    cantidad: int
    movimiento_id: int | None = None
    ok: bool
    error: str | None = None


class CargaInicialResultadoDTO(BaseModel):
    """
    Resultado de la carga.

    `fallidas` y `registradas` van por separado a propósito: es normal que
    falle alguna línea (un producto dado de baja, una ubicación que ya no
    existe) y no debe tirar abajo las otras doscientas.
    """

    total_lineas: int
    registradas: int
    fallidas: int
    movimientos: list[LineaCargaResultadoDTO]