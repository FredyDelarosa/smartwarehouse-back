"""Modelo ORM: incidencias."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.incidencia import TipoIncidencia
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.producto_model import ProductoModel
    from app.infrastructure.database.models.ubicacion_model import UbicacionModel
    from app.infrastructure.database.models.usuario_model import UsuarioModel


class IncidenciaModel(Base):
    __tablename__ = "incidencias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo: Mapped[TipoIncidencia] = mapped_column(
        SAEnum(
            TipoIncidencia,
            name="tipo_incidencia",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )
    producto_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("productos.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    ubicacion_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ubicaciones.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    fecha: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True, index=True
    )
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resuelta: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fecha_resolucion: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )

    # Relaciones
    producto: Mapped[Optional["ProductoModel"]] = relationship(
        "ProductoModel",
        back_populates="incidencias",
        lazy="raise",
    )
    ubicacion: Mapped[Optional["UbicacionModel"]] = relationship(
        "UbicacionModel",
        back_populates="incidencias",
        lazy="raise",
    )
    usuario: Mapped["UsuarioModel"] = relationship(
        "UsuarioModel",
        back_populates="incidencias",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return (
            f"<IncidenciaModel id={self.id} tipo={self.tipo} "
            f"resuelta={self.resuelta}>"
        )