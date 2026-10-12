"""Modelo ORM: almacenes."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.ubicacion_model import UbicacionModel


class AlmacenModel(Base):
    __tablename__ = "almacenes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True
    )

    ubicaciones: Mapped[List["UbicacionModel"]] = relationship(
        "UbicacionModel",
        back_populates="almacen",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<AlmacenModel id={self.id} nombre={self.nombre!r}>"