"""
Script: insertar usuarios de prueba faltantes.

Crea los usuarios de prueba que documenta API_FRONTEND.md:
- ana.torres@xyz.com (Administrador)
- carlos.ruiz@xyz.com (Supervisor)
- luis.mendoza@xyz.com (Almacenero)

Uso:
    python scripts/seed_usuarios.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from app.infrastructure.database.session import AsyncSessionLocal


USUARIOS_PRUEBA = [
    {
        "email": "ana.torres@xyz.com",
        "nombre": "Ana Torres",
        "rol_id": 1,  # Administrador
        "password": "Demo1234!",
    },
    {
        "email": "carlos.ruiz@xyz.com",
        "nombre": "Carlos Ruiz",
        "rol_id": 2,  # Supervisor
        "password": "Demo1234!",
    },
    {
        "email": "luis.mendoza@xyz.com",
        "nombre": "Luis Mendoza",
        "rol_id": 3,  # Almacenero
        "password": "Demo1234!",
    },
]


async def main() -> None:
    """Inserta los usuarios de prueba si no existen."""
    from app.infrastructure.security import BcryptPasswordHasher

    hasher = BcryptPasswordHasher()

    async with AsyncSessionLocal() as session:
        for usuario in USUARIOS_PRUEBA:
            # Verificar si ya existe
            result = await session.execute(
                text("SELECT id FROM usuarios WHERE email = :email"),
                {"email": usuario["email"]},
            )
            existente = result.fetchone()

            if existente:
                # Actualizar contraseña por si cambió
                password_hash = hasher.hash(usuario["password"])
                await session.execute(
                    text(
                        "UPDATE usuarios SET password_hash = :hash, "
                        "activo = 1 WHERE email = :email"
                    ),
                    {"hash": password_hash, "email": usuario["email"]},
                )
                print(f"  ✅ Usuario actualizado: {usuario['email']}")
            else:
                # Crear nuevo usuario
                password_hash = hasher.hash(usuario["password"])
                await session.execute(
                    text(
                        "INSERT INTO usuarios (nombre, email, password_hash, rol_id, activo) "
                        "VALUES (:nombre, :email, :hash, :rol_id, 1)"
                    ),
                    {
                        "nombre": usuario["nombre"],
                        "email": usuario["email"],
                        "hash": password_hash,
                        "rol_id": usuario["rol_id"],
                    },
                )
                print(f"  ✅ Usuario creado: {usuario['email']}")

        await session.commit()
        print("\n✅ Usuarios de prueba listos")
        print("Contraseña para todos: Demo1234!")

        # Verificar
        result = await session.execute(
            text(
                "SELECT u.email, u.nombre, r.nombre as rol "
                "FROM usuarios u JOIN roles r ON u.rol_id = r.id "
                "WHERE u.email LIKE '%@xyz.com'"
            )
        )
        usuarios = result.fetchall()
        print(f"\nUsuarios de prueba ({len(usuarios)}):")
        for email, nombre, rol in usuarios:
            print(f"  - {nombre} ({email}) - {rol}")


if __name__ == "__main__":
    asyncio.run(main())
