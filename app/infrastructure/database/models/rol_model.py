"""Modelo ORM: roles."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.usuario_model import UsuarioModel


class RolModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True
    )

    # Relaciones
    usuarios: Mapped[List["UsuarioModel"]] = relationship(
        "UsuarioModel",
        back_populates="rol",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<RolModel id={self.id} nombre={self.nombre!r}>"