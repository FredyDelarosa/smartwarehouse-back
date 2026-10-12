"""Modelo ORM: ubicaciones."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.almacen_model import AlmacenModel
    from app.infrastructure.database.models.incidencia_model import IncidenciaModel
    from app.infrastructure.database.models.inventario_model import InventarioModel
    from app.infrastructure.database.models.movimiento_model import MovimientoModel


class UbicacionModel(Base):
    __tablename__ = "ubicaciones"
    __table_args__ = (
        UniqueConstraint(
            "almacen_id", "pasillo", "estante", "nivel",
            name="uk_ubicacion_fisica",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    almacen_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("almacenes.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    pasillo: Mapped[str] = mapped_column(String(10), nullable=False)
    estante: Mapped[str] = mapped_column(String(10), nullable=False)
    nivel: Mapped[str] = mapped_column(String(10), nullable=False)
    codigo_ubicacion: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    codigo_qr: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, unique=True
    )
    coordenada_x: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    coordenada_y: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True
    )

    # Relaciones
    almacen: Mapped["AlmacenModel"] = relationship(
        "AlmacenModel",
        back_populates="ubicaciones",
        lazy="raise",
    )
    inventarios: Mapped[List["InventarioModel"]] = relationship(
        "InventarioModel",
        back_populates="ubicacion",
        lazy="raise",
    )
    movimientos_origen: Mapped[List["MovimientoModel"]] = relationship(
        "MovimientoModel",
        foreign_keys="MovimientoModel.ubicacion_origen_id",
        back_populates="ubicacion_origen",
        lazy="raise",
    )
    movimientos_destino: Mapped[List["MovimientoModel"]] = relationship(
        "MovimientoModel",
        foreign_keys="MovimientoModel.ubicacion_destino_id",
        back_populates="ubicacion_destino",
        lazy="raise",
    )
    incidencias: Mapped[List["IncidenciaModel"]] = relationship(
        "IncidenciaModel",
        back_populates="ubicacion",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<UbicacionModel id={self.id} codigo={self.codigo_ubicacion!r}>"