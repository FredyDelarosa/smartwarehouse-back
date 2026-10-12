"""Modelo ORM: usuarios."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.busqueda_model import BusquedaModel
    from app.infrastructure.database.models.incidencia_model import IncidenciaModel
    from app.infrastructure.database.models.movimiento_model import MovimientoModel
    from app.infrastructure.database.models.rol_model import RolModel


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_creacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True
    )
    ultimo_acceso: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relaciones
    rol: Mapped["RolModel"] = relationship(
        "RolModel",
        back_populates="usuarios",
        lazy="raise",
    )
    movimientos: Mapped[List["MovimientoModel"]] = relationship(
        "MovimientoModel",
        back_populates="usuario",
        lazy="raise",
    )
    busquedas: Mapped[List["BusquedaModel"]] = relationship(
        "BusquedaModel",
        back_populates="usuario",
        lazy="raise",
    )
    incidencias: Mapped[List["IncidenciaModel"]] = relationship(
        "IncidenciaModel",
        back_populates="usuario",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<UsuarioModel id={self.id} email={self.email!r}>"