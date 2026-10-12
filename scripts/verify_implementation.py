"""
Script de verificación de la implementación.

Comprueba que la aplicación se importe correctamente y que todos
los routers y endpoints estén registrados sin necesidad de BD.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def verify_app() -> bool:
    """Verifica que la aplicación se importe correctamente."""
    print("=" * 60)
    print("VERIFICACIÓN DE IMPLEMENTACIÓN")
    print("=" * 60)
    
    try:
        from app.main import app
        print("✅ Aplicación importada correctamente")
    except Exception as e:
        print(f"❌ Error al importar la aplicación: {e}")
        return False
    
    # Verificar rutas registradas
    rutas = [r.path for r in app.routes if hasattr(r, "path")]
    print(f"\n✅ Rutas registradas: {len(rutas)}")
    
    # Verificar endpoints clave
    endpoints_esperados = [
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
        "/api/v1/productos/",
        "/api/v1/productos/buscar",
        "/api/v1/ubicaciones/",
        "/api/v1/ubicaciones/qr/{codigo_qr}",
        "/api/v1/inventario/producto/{producto_id}",
        "/api/v1/inventario/alertas",
        "/api/v1/movimientos/entrada",
        "/api/v1/movimientos/salida",
        "/api/v1/movimientos/traslado",
        "/api/v1/busquedas/iniciar",
        "/api/v1/busquedas/historial",
        "/api/v1/incidencias/",
        "/api/v1/metricas/tiempo-promedio",
        "/api/v1/metricas/comparativa",
        "/api/v1/metricas/dashboard",
    ]
    
    print("\n📋 Verificando endpoints clave:")
    todos_ok = True
    for endpoint in endpoints_esperados:
        if endpoint in rutas:
            print(f"  ✅ {endpoint}")
        else:
            print(f"  ❌ {endpoint} (NO ENCONTRADO)")
            todos_ok = False
    
    # Verificar routers
    print("\n📦 Routers registrados:")
    routers = [
        "auth",
        "productos",
        "ubicaciones",
        "inventario",
        "movimientos",
        "busquedas",
        "incidencias",
        "metricas",
        "health",
    ]
    for router in routers:
        encontrado = any(router in ruta for ruta in rutas)
        if encontrado:
            print(f"  ✅ {router}")
        else:
            print(f"  ❌ {router} (NO ENCONTRADO)")
            todos_ok = False
    
    print("\n" + "=" * 60)
    if todos_ok:
        print("✅ VERIFICACIÓN COMPLETA: Todos los endpoints y routers están registrados")
        return True
    else:
        print("❌ VERIFICACIÓN FALTANTE: Algunos endpoints o routers no están registrados")
        return False


def verify_use_cases() -> bool:
    """Verifica que todos los use cases estén implementados."""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE CASOS DE USO")
    print("=" * 60)
    
    use_cases = [
        # Auth
        ("LoginUseCase", "app.application.use_cases.auth.login_use_case"),
        ("RegisterUseCase", "app.application.use_cases.auth.register_use_case"),
        ("RefreshTokenUseCase", "app.application.use_cases.auth.refresh_token_use_case"),
        ("ChangePasswordUseCase", "app.application.use_cases.auth.change_password_use_case"),
        # Productos
        ("ListarProductosUseCase", "app.application.use_cases.productos.listar_productos"),
        ("CrearProductoUseCase", "app.application.use_cases.productos.crear_producto"),
        ("ObtenerProductoUseCase", "app.application.use_cases.productos.obtener_producto"),
        ("ActualizarProductoUseCase", "app.application.use_cases.productos.actualizar_producto"),
        ("EliminarProductoUseCase", "app.application.use_cases.productos.eliminar_producto"),
        # Ubicaciones
        ("ListarUbicacionesUseCase", "app.application.use_cases.ubicaciones.listar_ubicaciones"),
        ("CrearUbicacionUseCase", "app.application.use_cases.ubicaciones.crear_ubicacion"),
        ("BuscarUbicacionPorQRUseCase", "app.application.use_cases.ubicaciones.buscar_por_qr"),
        # Inventario
        ("ConsultarStockUseCase", "app.application.use_cases.inventario.consultar_stock"),
        ("AlertasStockBajoUseCase", "app.application.use_cases.inventario.alertas_stock_bajo"),
        # Movimientos
        ("RegistrarEntradaUseCase", "app.application.use_cases.movimientos.registrar_entrada"),
        ("RegistrarSalidaUseCase", "app.application.use_cases.movimientos.registrar_salida"),
        ("RegistrarTrasladoUseCase", "app.application.use_cases.movimientos.registrar_traslado"),
        # Búsquedas
        ("IniciarBusquedaUseCase", "app.application.use_cases.busquedas.iniciar_busqueda"),
        ("FinalizarBusquedaUseCase", "app.application.use_cases.busquedas.finalizar_busqueda"),
        ("HistorialBusquedasUseCase", "app.application.use_cases.busquedas.historial_busquedas"),
        # Incidencias
        ("ListarIncidenciasUseCase", "app.application.use_cases.incidencias.listar_incidencias"),
        ("CrearIncidenciaUseCase", "app.application.use_cases.incidencias.crear_incidencia"),
        ("ResolverIncidenciaUseCase", "app.application.use_cases.incidencias.resolver_incidencia"),
        # Métricas
        ("TiempoPromedioBusquedaUseCase", "app.application.use_cases.metricas.tiempo_promedio_busqueda"),
        ("CompararBusquedasUseCase", "app.application.use_cases.metricas.comparar_busquedas"),
        ("ResumenIncidenciasUseCase", "app.application.use_cases.metricas.resumen_incidencias"),
        ("ResumenMovimientosUseCase", "app.application.use_cases.metricas.resumen_movimientos"),
        ("DashboardResumenUseCase", "app.application.use_cases.metricas.dashboard_resumen"),
    ]
    
    todos_ok = True
    for nombre, ruta in use_cases:
        try:
            modulo, clase = ruta.rsplit(".", 1)
            mod = __import__(modulo, fromlist=[clase])
            getattr(mod, clase)
            print(f"  ✅ {nombre}")
        except Exception as e:
            print(f"  ❌ {nombre}: {e}")
            todos_ok = False
    
    print("\n" + "=" * 60)
    if todos_ok:
        print("✅ TODOS LOS CASOS DE USO ESTÁN IMPLEMENTADOS")
        return True
    else:
        print("❌ FALTAN CASOS DE USO POR IMPLEMENTAR")
        return False


def verify_repositories() -> bool:
    """Verifica que todos los repositorios estén implementados."""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE REPOSITORIOS")
    print("=" * 60)
    
    repos = [
        "ProductoRepositoryImpl",
        "UbicacionRepositoryImpl",
        "InventarioRepositoryImpl",
        "MovimientoRepositoryImpl",
        "BusquedaRepositoryImpl",
        "IncidenciaRepositoryImpl",
        "AlmacenRepositoryImpl",
        "CategoriaRepositoryImpl",
        "UsuarioRepositoryImpl",
        "RolRepositoryImpl",
    ]
    
    todos_ok = True
    try:
        from app.infrastructure.repositories import (
            ProductoRepositoryImpl,
            UbicacionRepositoryImpl,
            InventarioRepositoryImpl,
            MovimientoRepositoryImpl,
            BusquedaRepositoryImpl,
            IncidenciaRepositoryImpl,
            AlmacenRepositoryImpl,
            CategoriaRepositoryImpl,
            UsuarioRepositoryImpl,
            RolRepositoryImpl,
        )
        for repo in repos:
            print(f"  ✅ {repo}")
    except Exception as e:
        print(f"  ❌ Error al importar repositorios: {e}")
        todos_ok = False
    
    print("\n" + "=" * 60)
    if todos_ok:
        print("✅ TODOS LOS REPOSITORIOS ESTÁN IMPLEMENTADOS")
        return True
    else:
        print("❌ FALTAN REPOSITORIOS POR IMPLEMENTAR")
        return False


def main() -> bool:
    """Ejecuta todas las verificaciones."""
    ok = True
    ok = verify_app() and ok
    ok = verify_use_cases() and ok
    ok = verify_repositories() and ok
    
    print("\n" + "=" * 60)
    if ok:
        print("🎉 IMPLEMENTACIÓN COMPLETA Y VERIFICADA")
        print("=" * 60)
        return True
    else:
        print("⚠️  LA IMPLEMENTACIÓN TIENE ERRORES")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
