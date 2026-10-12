"""
Value Object: CodigoProducto.

Formato: 2 a 6 letras mayúsculas seguidas de 1 a 4 dígitos.
Ejemplos válidos: 'T001', 'HM01', 'G001', 'N007', 'HE05'.

Reglas:
- Se normaliza a mayúsculas sin espacios.
- Debe empezar por letras y terminar en números.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_PATRON = re.compile(r"^[A-Z]{1,6}\d{1,4}$")

@dataclass(frozen=True, slots=True)
class CodigoProducto:
    """Value object inmutable que representa el código de un producto."""

    valor: str

    def __post_init__(self) -> None:
        normalizado = self._normalizar(self.valor)
        if not _PATRON.match(normalizado):
            raise ValueError(
                f"Código de producto inválido: '{self.valor}'. "
                f"Formato esperado: letras mayúsculas seguidas de dígitos "
                f"(ej. 'T001', 'HM01', 'G001')"
            )
        object.__setattr__(self, "valor", normalizado)

    @staticmethod
    def _normalizar(valor: str) -> str:
        if not isinstance(valor, str):
            raise ValueError("El código de producto debe ser una cadena de texto")
        return valor.strip().upper().replace(" ", "").replace("-", "")

    @property
    def prefijo(self) -> str:
        """Parte alfabética del código. Ej: 'T', 'HM', 'HE'."""
        return "".join(c for c in self.valor if c.isalpha())

    @property
    def numero(self) -> int:
        """Parte numérica del código como entero. Ej: 1, 12, 7."""
        digitos = "".join(c for c in self.valor if c.isdigit())
        return int(digitos) if digitos else 0

    def __str__(self) -> str:
        return self.valor

    def __repr__(self) -> str:
        return f"CodigoProducto('{self.valor}')"