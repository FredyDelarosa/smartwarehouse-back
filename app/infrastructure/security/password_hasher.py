"""Adaptador: hashing de contraseñas con bcrypt (vía core.security)."""

from app.core.security import hash_password, verify_password
from app.domain.ports import PasswordHasherPort


class BcryptPasswordHasher(PasswordHasherPort):
    """Implementación concreta del puerto PasswordHasherPort usando bcrypt."""

    def hash(self, plain_password: str) -> str:
        return hash_password(plain_password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)