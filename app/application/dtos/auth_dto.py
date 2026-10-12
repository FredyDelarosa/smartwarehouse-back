"""DTOs: Autenticación."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=72)


class TokenDTO(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenPayloadDTO(BaseModel):
    sub: str
    type: str
    rol: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None


class RefreshTokenDTO(BaseModel):
    refresh_token: str = Field(..., min_length=10)


class ChangePasswordDTO(BaseModel):
    password_actual: str = Field(..., min_length=1, max_length=72)
    password_nuevo: str = Field(..., min_length=8, max_length=72)