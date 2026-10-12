"""
Value Object: CodigoUbicacion.

Formato canónico: P{pasillo}-{estante}-{nivel:02}
Ejemplos válidos: 'P1-A-01', 'P3-B-02', 'P5-J-03'

Reglas:
- Pasillo: 'P' seguido de 1 o 2 dígitos (P1..P99).
- Estante: una letra mayúscula (A..Z).
- Nivel: 1 o 2 dígitos, se normaliza a 2 dígitos con cero a la izquierda.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_PATRON = re.compile(r"^P(?P<pasillo>\d{1,2})-(?P<estante>[A-Z])-(?P<nivel>\d{1,2})$")


@dataclass(frozen=True, slots=True)
class CodigoUbicacion:
    """Value object inmutable que representa el código de una ubicación."""

    valor: str

    def __post_init__(self) -> None:
        normalizado = self._normalizar(self.valor)
        if not _PATRON.match(normalizado):
            raise ValueError(
                f"Código de ubicación inválido: '{self.valor}'. "
                f"Formato esperado: 'P{{pasillo}}-{{estante}}-{{nivel}}' "
                f"(ej. 'P3-B-02')"
            )
        # frozen=True => usar object.__setattr__ para normalizar
        object.__setattr__(self, "valor", normalizado)

    # ------------------------------------------------------------------
    # Constructores alternativos
    # ------------------------------------------------------------------
    @classmethod
    def desde_partes(cls, pasillo: int | str, estante: str, nivel: int | str) -> "CodigoUbicacion":
        """
        Construye el código a partir de sus componentes.

        Ejemplo:
            CodigoUbicacion.desde_partes(3, 'b', 2) -> 'P3-B-02'
        """
        p = str(pasillo).lstrip("Pp")
        e = str(estante).strip().upper()
        n = str(nivel).strip()
        return cls(f"P{p}-{e}-{int(n):02d}")

    # ------------------------------------------------------------------
    # Normalización
    # ------------------------------------------------------------------
    @staticmethod
    def _normalizar(valor: str) -> str:
        if not isinstance(valor, str):
            raise ValueError("El código de ubicación debe ser una cadena de texto")
        v = valor.strip().upper().replace(" ", "")
        # Aceptamos 'P3-B-2' y lo normalizamos a 'P3-B-02'
        m = _PATRON.match(v)
        if m:
            pasillo = m.group("pasillo").lstrip("0") or "0"
            estante = m.group("estante")
            nivel = int(m.group("nivel"))
            return f"P{pasillo}-{estante}-{nivel:02d}"
        return v

    # ------------------------------------------------------------------
    # Accesores
    # ------------------------------------------------------------------
    @property
    def pasillo(self) -> str:
        """Devuelve la parte del pasillo, con prefijo P. Ej: 'P3'."""
        return "P" + _PATRON.match(self.valor).group("pasillo")  # type: ignore[union-attr]

    @property
    def estante(self) -> str:
        """Devuelve la letra del estante. Ej: 'B'."""
        return _PATRON.match(self.valor).group("estante")  # type: ignore[union-attr]

    @property
    def nivel(self) -> int:
        """Devuelve el nivel como entero."""
        return int(_PATRON.match(self.valor).group("nivel"))  # type: ignore[union-attr]

    # ------------------------------------------------------------------
    # Dunders
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return self.valor

    def __repr__(self) -> str:
        return f"CodigoUbicacion('{self.valor}')"