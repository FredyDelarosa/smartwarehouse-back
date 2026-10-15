"""DTOs: configuración del almacén por cuestionario (PET-4, fases 3 y 4).

Cada cliente describe cómo es su almacén y el backend genera las ubicaciones,
sus códigos y sus QR. El cuestionario va en el cuerpo porque es la única forma
de que el sistema funcione con un almacén real: nadie tiene 150 estantes
iguales.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

# El código de ubicación es `P<pasillo>-<estante>-<nivel>` y el value object
# obliga a que el estante sea UNA sola letra mayúscula. Son 26 estantes como
# máximo por pasillo, y no es una decisión nuestra: viene del formato del QR
# que ya se imprimió en el almacén original.
MAX_ESTANTES = 26
MAX_PASILLOS = 99
MAX_NIVELES = 99


class PasilloConfigDTO(BaseModel):
    """Un pasillo con sus estantes."""

    nombre: str = Field(..., min_length=1, max_length=10)
    estantes: int = Field(..., ge=1, le=MAX_ESTANTES)
    # Letras de estante que existen pero no se usan (obstruidos, en
    # reforma...). Se crean igual, pero marcadas como inactivas: así el
    # trabajador ve que el hueco es real y no un fallo de generación.
    estantes_fuera_servicio: list[str] = Field(default_factory=list, max_length=MAX_ESTANTES)

    @field_validator("nombre")
    @classmethod
    def _nombre_sin_espacios(cls, v: str) -> str:
        limpio = v.strip().upper().lstrip("P")
        if not limpio.isdigit():
            raise ValueError("El pasillo debe numerarse (P1, P2, 3…): usa su número.")
        n = int(limpio)
        if not 1 <= n <= MAX_PASILLOS:
            raise ValueError(f"El pasillo debe estar entre 1 y {MAX_PASILLOS}.")
        return str(n)

    @field_validator("estantes_fuera_servicio")
    @classmethod
    def _letras_validas(cls, v: list[str]) -> list[str]:
        return [x.strip().upper() for x in v if x and x.strip()]


class NivelConfigDTO(BaseModel):
    """Un nivel del estante. El suelo es el nivel 1."""

    nombre: str = Field(..., min_length=1, max_length=10)

    @field_validator("nombre", mode="before")
    @classmethod
    def _acepta_numero(cls, v: object) -> object:
        """
        Acepta `3` además de `"3"`.

        Pydantic es estricto con los tipos y un nivel es un número: lo natural
        es que el formulario lo mande como número. Sin esto, el cliente tiene
        que acordarse de serializarlo como cadena para no recibir un 422.
        """
        if isinstance(v, int):
            return str(v)
        return v

    @field_validator("nombre")
    @classmethod
    def _a_numero(cls, v: str) -> str:
        limpio = v.strip()
        if limpio.isdigit():
            n = int(limpio)
            if not 1 <= n <= MAX_NIVELES:
                raise ValueError(f"El nivel debe estar entre 1 y {MAX_NIVELES}.")
            return str(n)
        raise ValueError("Los niveles se numeran (1, 2, 3…); el suelo es el 1.")


class ConfigAlmacenDTO(BaseModel):
    """Respuestas del cuestionario."""

    pasillos: list[PasilloConfigDTO] = Field(..., min_length=1, max_length=MAX_PASILLOS)
    niveles: list[NivelConfigDTO] = Field(..., min_length=1, max_length=MAX_NIVELES)

    @field_validator("pasillos")
    @classmethod
    def _pasillos_unicos(cls, v: list[PasilloConfigDTO]) -> list[PasilloConfigDTO]:
        nombres = [p.nombre for p in v]
        repetidos = {n for n in nombres if nombres.count(n) > 1}
        if repetidos:
            raise ValueError(
                "Estos pasillos están repetidos: "
                + ", ".join(sorted(repetidos))
            )
        return v

    @field_validator("niveles")
    @classmethod
    def _niveles_unicos(cls, v: list[NivelConfigDTO]) -> list[NivelConfigDTO]:
        nombres = [n.nombre for n in v]
        repetidos = {n for n in nombres if nombres.count(n) > 1}
        if repetidos:
            raise ValueError("Estos niveles están repetidos: " + ", ".join(sorted(repetidos)))
        return v


class UbicacionPrevisualizadaDTO(BaseModel):
    codigo_ubicacion: str
    codigo_qr: str
    pasillo: str
    estante: str
    nivel: str
    activo: bool


class PrevisualizacionDTO(BaseModel):
    """
    Lo que se va a crear, sin escribir nada.

    Existe para que nadie descubra que ha puesto 8 estantes en vez de 3 con
    500 filas nuevas en el almacén. El botón de generar siempre va detrás de
    esta pantalla.
    """

    total: int
    activas: int
    fuera_servicio: int
    por_pasillo: dict[str, int]
    total_pasillos: int
    total_estantes: int
    total_niveles: int
    # Solo unas pocas: son 96 filas y no tiene sentido devolverlas todas.
    muestra: list[UbicacionPrevisualizadaDTO]
    advertencias: list[str] = Field(default_factory=list)
    # Cuántas ya existen en el almacén con esos mismos códigos. Si es > 0,
    # la generación los omitirá en lugar de fallar a mitad.
    ya_existentes: int = 0


class GeneracionResultDTO(BaseModel):
    creadas: int
    omitidas: int
    fuera_servicio: int
    muestra: list[UbicacionPrevisualizadaDTO]


class ResumenAlmacenDTO(BaseModel):
    """Lo que ya tiene el almacén, para saber si falta configurarlo."""

    # El nombre va aquí porque la hoja de estante se imprime y se cuelga en el
    # almacén: sin él, una lista de la nave de arriba es indistinguible de una
    # de la de abajo.
    nombre: str
    total_ubicaciones: int
    activas: int
    fuera_servicio: int
    pasillos: int
    niveles: int
    # False cuando el almacén aún no tiene ninguna ubicación: es lo que decide
    # si el cuestionario se ofrece como algo pendiente o como una ampliación.
    configurado: bool