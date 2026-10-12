"""Modelo ORM: categorias."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.producto_model import ProductoModel


class CategoriaModel(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("1"), default=True
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True
    )

    productos: Mapped[List["ProductoModel"]] = relationship(
        "ProductoModel",
        back_populates="categoria",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<CategoriaModel id={self.id} nombre={self.nombre!r}>"