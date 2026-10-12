"""
Value Object: Email.

Validación de correo con regex razonable (no exhaustiva RFC 5322, pero
cubre todos los casos prácticos y evita dependencias externas).

Reglas:
- Se normaliza a minúsculas y sin espacios.
- Debe tener usuario@dominio.ext con TLD de 2+ letras.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_PATRON = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


@dataclass(frozen=True, slots=True)
class Email:
    """Value object inmutable que representa un correo electrónico."""

    valor: str

    def __post_init__(self) -> None:
        normalizado = self._normalizar(self.valor)
        if not _PATRON.match(normalizado):
            raise ValueError(
                f"Correo electrónico inválido: '{self.valor}'"
            )
        object.__setattr__(self, "valor", normalizado)

    @staticmethod
    def _normalizar(valor: str) -> str:
        if not isinstance(valor, str):
            raise ValueError("El correo electrónico debe ser una cadena de texto")
        return valor.strip().lower()

    @property
    def usuario(self) -> str:
        """Parte anterior a la @."""
        return self.valor.split("@", 1)[0]

    @property
    def dominio(self) -> str:
        """Parte posterior a la @."""
        return self.valor.split("@", 1)[1]

    def __str__(self) -> str:
        return self.valor

    def __repr__(self) -> str:
        return f"Email('{self.valor}')"