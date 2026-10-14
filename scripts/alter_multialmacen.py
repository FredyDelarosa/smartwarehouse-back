"""
PET-4 · Multialmacén (Fase 1).

Añade `almacen_id` a `usuarios` y `productos`, hace el backfill y ajusta los
índices para que el código de producto sea único **dentro** de cada almacén.

Es idempotente: se puede ejecutar tantas veces como haga falta.

Uso:  .venv/bin/python scripts/alter_multialmacen.py

Se hace en Python y no en SQL con PREPARE por una razón concreta: TiDB no
acepta `ALTER TABLE ... ADD COLUMN` dentro de un bloqueIF(), y partir el
fichero por ';' parte las sentencias a mitad. En Python cada comprobación es
una consulta y cada cambio es un ALTER limpio.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text  # noqa: E402
from app.infrastructure.database.session import engine  # noqa: E402


async def existe_columna(c, tabla: str, columna: str) -> bool:
    r = await c.execute(
        text(
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t AND COLUMN_NAME = :c"
        ),
        {"t": tabla, "c": columna},
    )
    return bool(r.scalar())


async def existe_indice(c, tabla: str, indice: str) -> bool:
    r = await c.execute(
        text(
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t AND INDEX_NAME = :i"
        ),
        {"t": tabla, "i": indice},
    )
    return bool(r.scalar())


async def main() -> int:
    async with engine.begin() as c:
        # --- 1. Columnas --------------------------------------------------
        for tabla in ("usuarios", "productos"):
            if await existe_columna(c, tabla, "almacen_id"):
                print(f"  · {tabla}.almacen_id ya existe")
            else:
                await c.execute(
                    text(f"ALTER TABLE {tabla} ADD COLUMN almacen_id INT NOT NULL DEFAULT 1")
                )
                print(f"  ✓ {tabla}.almacen_id añadida")

        # --- 2. Backfill --------------------------------------------------
        # El DEFAULT 1 ya los deja en el almacén 1, pero se hace explícito:
        # depender del DEFAULT para datos reales es confiar en que nadie lo
        # tocó antes.
        await c.execute(text("UPDATE usuarios SET almacen_id = 1 WHERE almacen_id IS NULL OR almacen_id = 0"))
        await c.execute(text("UPDATE productos SET almacen_id = 1 WHERE almacen_id IS NULL OR almacen_id = 0"))
        print("  ✓ backfill al almacén 1")

        # --- 3. Índice de lectura ----------------------------------------
        # `productos` es la tabla más consultada (búsquedas, inventario,
        # métricas). Filtrar por almacén sin índice es un escaneo completo.
        if await existe_indice(c, "productos", "ix_productos_almacen_codigo"):
            print("  · ix_productos_almacen_codigo ya existe")
        else:
            await c.execute(
                text("CREATE INDEX ix_productos_almacen_codigo ON productos (almacen_id, codigo)")
            )
            print("  ✓ ix_productos_almacen_codigo creado")

        if await existe_indice(c, "usuarios", "ix_usuarios_almacen"):
            print("  · ix_usuarios_almacen ya existe")
        else:
            await c.execute(text("CREATE INDEX ix_usuarios_almacen ON usuarios (almacen_id)"))
            print("  ✓ ix_usuarios_almacen creado")

        # --- 4. Unicidad por almacén -------------------------------------
        # `codigo` es ÚNICO GLOBAL. Con multialmacén deja de serlo: el almacén 2
        # puede tener su propio T001 sin que sea un conflicto.
        if await existe_indice(c, "productos", "uq_productos_almacen_codigo"):
            print("  · uq_productos_almacen_codigo ya existe")
        else:
            if await existe_indice(c, "productos", "codigo"):
                await c.execute(text("ALTER TABLE productos DROP INDEX codigo"))
                print("  ✓ índice global 'codigo' eliminado")
            await c.execute(
                text("CREATE UNIQUE INDEX uq_productos_almacen_codigo ON productos (almacen_id, codigo)")
            )
            print("  ✓ uq_productos_almacen_codigo creado (único por almacén)")

    # --- Verificación ----------------------------------------------------
    print("\n  Verificación:")
    async with engine.connect() as c:
        for tabla in ("usuarios", "productos"):
            ok = await existe_columna(c, tabla, "almacen_id")
            print(f"    {tabla}.almacen_id = {'sí' if ok else 'NO'}")
        for t, r in await c.execute(text("SELECT almacen_id, COUNT(*) FROM usuarios GROUP BY almacen_id")):
            print(f"    usuarios en almacén {t}: {r}")
        for t, r in await c.execute(text("SELECT almacen_id, COUNT(*) FROM productos GROUP BY almacen_id")):
            print(f"    productos en almacén {t}: {r}")

    await engine.dispose()
    print("\n  Migración completada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
