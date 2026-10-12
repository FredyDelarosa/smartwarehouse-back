"""Adaptador: emisión y validación de JWT (vía core.security)."""

from datetime import timedelta
from typing import Any, Optional

from app.core.security import (
    create_access_token as _create_access,
)
from app.core.security import (
    create_refresh_token as _create_refresh,
)
from app.core.security import (
    decode_token as _decode,
)
from app.domain.ports import TokenProviderPort


class JWTTokenProvider(TokenProviderPort):
    """Implementación concreta del puerto TokenProviderPort usando python-jose."""

    def create_access_token(
        self,
        subject: str | int,
        extra_claims: Optional[dict[str, Any]] = None,
        expires_minutes: Optional[int] = None,
    ) -> str:
        delta = timedelta(minutes=expires_minutes) if expires_minutes else None
        return _create_access(subject, extra_claims, delta)

    def create_refresh_token(
        self,
        subject: str | int,
        expires_days: Optional[int] = None,
    ) -> str:
        delta = timedelta(days=expires_days) if expires_days else None
        return _create_refresh(subject, delta)

    def decode(self, token: str) -> dict[str, Any]:
        return _decode(token)