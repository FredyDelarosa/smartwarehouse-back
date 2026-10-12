"""
Script: actualizar contraseñas de usuarios sintéticos.

Permite que los usuarios de los datos sintéticos puedan iniciar sesión
con la contraseña `Demo1234!`.

Uso:
    python scripts/seed_usuarios_password.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from app.infrastructure.database.session import AsyncSessionLocal


async def main() -> None:
    """Actualiza el password_hash de todos los usuarios sintéticos."""
    engine = AsyncSessionLocal.kw["bind"]
    
    # Importar el hasher
    from app.infrastructure.security import BcryptPasswordHasher
    
    hasher = BcryptPasswordHasher()
    password = "Demo1234!"
    password_hash = hasher.hash(password)
    
    print(f"Generando hash para '{password}'...")
    print(f"Hash: {password_hash[:50]}...")
    
    async with AsyncSessionLocal() as session:
        # Actualizar todos los usuarios
        result = await session.execute(
            text(
                "UPDATE usuarios SET password_hash = :hash "
                "WHERE email LIKE '%@xyz.com'"
            ),
            {"hash": password_hash}
        )
        await session.commit()
        
        print(f"\n✅ Se actualizaron {result.rowcount} usuarios")
        print("Contraseña: Demo1234!")
        
        # Verificar
        result = await session.execute(
            text(
                "SELECT email, nombre FROM usuarios "
                "WHERE email LIKE '%@xyz.com'"
            )
        )
        usuarios = result.fetchall()
        print(f"\nUsuarios sintéticos ({len(usuarios)}):")
        for email, nombre in usuarios:
            print(f"  - {nombre} ({email})")
    
    await engine.dispose()
    print("\n>>> FASE 11.10 COMPLETA: Passwords actualizados")


if __name__ == "__main__":
    asyncio.run(main())
