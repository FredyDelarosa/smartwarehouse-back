"""Caso de uso: configurar un almacén a partir del cuestionario (PET-4, fases 3 y 4)."""

from __future__ import annotations

import string

from app.application.dtos import (
    ConfigAlmacenDTO,
    GeneracionResultDTO,
    PrevisualizacionDTO,
    ResumenAlmacenDTO,
    UbicacionPrevisualizadaDTO,
)
from app.domain.entities import Ubicacion
from app.domain.exceptions import ValidacionError
from app.domain.repositories import AlmacenRepository, UbicacionRepository
from app.domain.value_objects import CodigoUbicacion

#: Estantes disponibles: una letra cada uno, por eso 26 y no 99.
LETRAS_ESTANTE = string.ascii_uppercase

#: Cuántas ubicaciones se enseñan en la previsualización. Suficiente para
#: reconocer el patrón sin volcar 1500 filas por pantalla.
MUESTRA_INICIO = 3
MUESTRA_FIN = 3

#: Por encima de esto la generación deja de ser trivial y avisamos.
AVISO_MUCHAS_UBICACIONES = 1000


class ConfigurarAlmacenUseCase:
    """
    Convierte las respuestas del cuestionario en ubicaciones, códigos y QR.

    ## Por qué dos métodos y no uno

    `previsualizar()` no escribe nada: dice cuántas filas habría y cómo se
    llamarían. `generar()` escribe. Están separados a propósito para que la
    pantalla de confirmación sea real — que se vea el resultado antes de
    tocar el almacén— y no un simple "¿seguro?" sin cifras.

    ## Por qué los estantes fuera de servicio se crean igual

    Un estante obstruido no se borra del almacén: sigue ahí, occupying sitio,
    y mañana vuelve a estar en servicio. Marcarlo `activo=False` en vez de
    omitirlo deja el hueco visible y hace que ponerlo en marcha sea cambiar un
    campo, no volver a crear 30 filas y reimprimir 30 etiquetas.

    ## El código no lo inventamos aquí

    Pasa por `CodigoUbicacion`, el mismo value object que valida las
    ubicaciones creadas a mano. Si el formato no cuadra, revienta en el
    servidor y no en la etiqueta de un estante real.
    """

    def __init__(
        self,
        ubicacion_repo: UbicacionRepository,
        almacen_repo: AlmacenRepository | None = None,
    ) -> None:
        self._ubicacion_repo = ubicacion_repo
        # Opcional: las tres rutas de previsualizar/generar no lo necesitan y
        # no tiene sentido exigir un repositorio que no van a usar.
        self._almacen_repo = almacen_repo

    # ------------------------------------------------------------------
    # Cálculo
    # ------------------------------------------------------------------
    def _expandir(self, dto: ConfigAlmacenDTO, almacen_id: int | None) -> list[Ubicacion]:
        """
        Cruza pasillos × estantes × niveles.

        El orden es pasillo → estante → nivel para que los códigos salgan
        ordenados como están en el almacén físicamente: recorriendo el pasillo
        de abajo arriba, estante por estante.
        """
        niveles = sorted((n.nombre for n in dto.niveles), key=int)
        ubicaciones: list[Ubicacion] = []

        for pasillo in sorted(dto.pasillos, key=lambda p: int(p.nombre)):
            fuera = {f.upper() for f in pasillo.estantes_fuera_servicio}
            for indice in range(pasillo.estantes):
                letra = LETRAS_ESTANTE[indice]
                for nivel in niveles:
                    codigo = CodigoUbicacion.desde_partes(pasillo.nombre, letra, nivel)
                    ubicaciones.append(
                        Ubicacion(
                            almacen_id=almacen_id,
                            pasillo=codigo.pasillo,
                            estante=codigo.estante,
                            nivel=str(codigo.nivel),
                            codigo_ubicacion=codigo.valor,
                            codigo_qr=f"QR-{codigo.valor}",
                            activo=letra not in fuera,
                        )
                    )
        return ubicaciones

    @staticmethod
    def _muestra(ubicaciones: list[Ubicacion]) -> list[UbicacionPrevisualizadaDTO]:
        elegidas = ubicaciones[:MUESTRA_INICIO]
        if len(ubicaciones) > MUESTRA_INICIO + MUESTRA_FIN:
            elegidas = elegidas + ubicaciones[-MUESTRA_FIN:]
        return [
            UbicacionPrevisualizadaDTO(
                codigo_ubicacion=u.codigo_ubicacion,
                codigo_qr=u.codigo_qr or "",
                pasillo=u.pasillo,
                estante=u.estante,
                nivel=u.nivel,
                activo=u.activo,
            )
            for u in elegidas
        ]

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------
    async def previsualizar(
        self, dto: ConfigAlmacenDTO, almacen_id: int | None
    ) -> PrevisualizacionDTO:
        """
        Dice lo que se crearía, sin escribir nada.

        `almacen_id` es `None` cuando quien pregunta aún no tiene cuenta: está
        en el paso de confirmar del alta, antes de que exista el almacén. En ese
        caso no hay nada que pueda existir ya, así que `ya_existentes` vale 0 y
        la pantalla no muestra esa columna.
        """
        ubicaciones = self._expandir(dto, almacen_id)

        fuera = [u for u in ubicaciones if not u.activo]
        por_pasillo: dict[str, int] = {}
        for u in ubicaciones:
            por_pasillo[u.pasillo] = por_pasillo.get(u.pasillo, 0) + 1

        # Cuántas de esas ya existen: si el usuario repite la generación, se
        # avisa en vez de devolver un error de duplicado a mitad.
        ya_existentes = 0
        if almacen_id is not None:
            for u in ubicaciones:
                if await self._ubicacion_repo.get_by_codigo(u.codigo_ubicacion) is not None:
                    ya_existentes += 1

        return PrevisualizacionDTO(
            total=len(ubicaciones),
            activas=len(ubicaciones) - len(fuera),
            fuera_servicio=len(fuera),
            por_pasillo=dict(sorted(por_pasillo.items())),
            total_pasillos=len(dto.pasillos),
            total_estantes=len({(u.pasillo, u.estante) for u in ubicaciones}),
            total_niveles=len(dto.niveles),
            muestra=self._muestra(ubicaciones),
            advertencias=self._advertencias(len(ubicaciones), len(fuera), ya_existentes),
            ya_existentes=ya_existentes,
        )

    async def generar(
        self, dto: ConfigAlmacenDTO, almacen_id: int
    ) -> GeneracionResultDTO:
        """
        Crea las ubicaciones que falten.

        Aquí el almacén es obligatorio: sin él las ubicaciones no tendrían a
        qué pertenecer, que es justamente lo que el aislamiento exige.
        """
        ubicaciones = self._expandir(dto, almacen_id)

        # Se filtran las que ya existen ANTES de insertar. Consultar una a una
        # dentro del bucle de inserción dejaría el almacén a medias si la
        # transacción no llegara a cerrarse; aquí se decide antes de escribir.
        nuevas: list[Ubicacion] = []
        omitidas = 0
        for u in ubicaciones:
            if await self._ubicacion_repo.get_by_codigo(u.codigo_ubicacion) is not None:
                omitidas += 1
                continue
            nuevas.append(u)

        if not nuevas:
            raise ValidacionError(
                "Todas esas ubicaciones ya existen. No hay nada nuevo que crear.",
                errores=[f"{omitidas} ya existen"],
            )

        creadas = await self._ubicacion_repo.create_many(nuevas, almacen_id=almacen_id)
        fuera = sum(1 for u in creadas if not u.activo)

        return GeneracionResultDTO(
            creadas=len(creadas),
            omitidas=omitidas,
            fuera_servicio=fuera,
            muestra=self._muestra(creadas),
        )

    async def resumen(self, almacen_id: int) -> ResumenAlmacenDTO:
        """Estado actual del almacén: sirve para saber si falta configurarlo."""
        existentes = await self._ubicacion_repo.list_by_almacen(
            almacen_id=almacen_id, solo_activas=False
        )
        pasillos = {u.pasillo for u in existentes}
        niveles = {u.nivel for u in existentes}
        almacen = await self._almacen_repo.get_by_id(almacen_id) if self._almacen_repo else None
        return ResumenAlmacenDTO(
            nombre=almacen.nombre if almacen else "Almacén",
            total_ubicaciones=len(existentes),
            activas=sum(1 for u in existentes if u.activo),
            fuera_servicio=sum(1 for u in existentes if not u.activo),
            pasillos=len(pasillos),
            niveles=len(niveles),
            configurado=len(existentes) > 0,
        )

    # ------------------------------------------------------------------
    @staticmethod
    def _advertencias(total: int, fuera: int, ya_existentes: int) -> list[str]:
        avisos: list[str] = []
        if total > AVISO_MUCHAS_UBICACIONES:
            avisos.append(
                f"Vas a crear {total} ubicaciones. Si son muchas, "
                "imprime las etiquetas por tandas: generar miles de QR de "
                "golpe deja el móvil sin memoria."
            )
        if fuera:
            avisos.append(
                f"{fuera} quedarán marcadas como FUERA DE SERVICIO: se crean "
                "y se ven en el listado, pero no admiten stock."
            )
        if ya_existentes:
            avisos.append(
                f"{ya_existentes} de esos códigos ya existen en el almacén. "
                "Se omitirán y solo se crearán los que falten."
            )
        return avisos