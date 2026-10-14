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

        # --- 5. Ubicaciones: el mismo problema -----------------------------
        # Se añadió después de la fase 1, cuando ya había almacenes nuevos, y
        # `codigo_ubicacion` y `codigo_qr` seguían ÚNICOS EN TODA LA TABLA.
        # Efecto: el almacén 2 no podía tener un P1-A-01 porque el almacén 1 ya
        # tenía uno, y la generación del cuestionario moría con un 1062.
        #
        # Nota sobre `codigo_qr`: el QR es lo que lleva la etiqueta pegada en el
        # estante. Que dos almacenes puedan tener el mismo contenido de QR es
        # lo correcto (se escanea dentro del almacén), y se puede comprobar:
        # el endpoint de lectura por QR ya va acotado al almacén del usuario.
        for columna, indice_nuevo in (
            ("codigo_ubicacion", "uq_ubicaciones_almacen_codigo"),
            ("codigo_qr", "uq_ubicaciones_almacen_qr"),
        ):
            if await existe_indice(c, "ubicaciones", indice_nuevo):
                print(f"  · {indice_nuevo} ya existe")
                continue
            # El índice global es el que choca. El no único (`idx_...`) se
            # deja: sirve para buscar por código sin recorrer, y el único por
            # almacén ya no puede cumplir esa función.
            if await existe_indice(c, "ubicaciones", columna):
                await c.execute(text(f"ALTER TABLE ubicaciones DROP INDEX {columna}"))
                print(f"  ✓ índice global '{columna}' eliminado")
            await c.execute(
                text(
                    f"CREATE UNIQUE INDEX {indice_nuevo} "
                    f"ON ubicaciones (almacen_id, {columna})"
                )
            )
            print(f"  ✓ {indice_nuevo} creado (único por almacén)")

        # Índice de lectura por código dentro del almacén: el escáner y el
        # listado filtran siempre por los dos.
        if await existe_indice(c, "ubicaciones", "ix_ubicaciones_almacen_codigo"):
            print("  · ix_ubicaciones_almacen_codigo ya existe")
        else:
            await c.execute(
                text(
                    "CREATE INDEX ix_ubicaciones_almacen_codigo "
                    "ON ubicaciones (almacen_id, codigo_ubicacion)"
                )
            )
            print("  ✓ ix_ubicaciones_almacen_codigo creado")

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
        print("    índices de ubicaciones:")
        r = await c.execute(
            text(
                "SELECT INDEX_NAME, NON_UNIQUE FROM INFORMATION_SCHEMA.STATISTICS "
                "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ubicaciones' "
                "GROUP BY INDEX_NAME, NON_UNIQUE ORDER BY INDEX_NAME"
            )
        )
        for nombre, no_unico in r:
            marca = "único " if no_unico == "0" else "índice"
            columnas = await c.execute(
                text(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.STATISTICS "
                    "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ubicaciones' "
                    "AND INDEX_NAME = :i ORDER BY SEQ_IN_INDEX"
                ),
                {"i": nombre},
            )
            cols = ", ".join(x[0] for x in columnas)
            print(f"      {marca} {nombre} ({cols})")

    await engine.dispose()
    print("\n  Migración completada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
