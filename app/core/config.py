"""
Configuración central de la aplicación.
Carga las variables desde el archivo .env usando pydantic-settings.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración tipada de la aplicación."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ----- Aplicación -----
    APP_NAME: str = "SmartWarehouse API"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = (
        "API para la localización y control de inventario en almacén"
    )
    DEBUG: bool = True

    # ----- API -----
    API_V1_PREFIX: str = "/api/v1"

    # ----- Base de datos -----
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "smart_warehouse"
    DB_ECHO: bool = False
    DB_SSL: bool = False
    DB_SSL_CA: str | None = None

    # ----- JWT -----
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480           # 8 horas
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ----- CORS (string separado por comas) -----
    CORS_ORIGINS: str = "http://localhost:4200,http://127.0.0.1:4200"

    # ========================================================
    # Propiedades derivadas
    # ========================================================
    @property
    def cors_origins_list(self) -> List[str]:
        """Devuelve la lista de orígenes CORS parseada."""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def database_url_async(self) -> str:
        """URL de conexión asíncrona (SQLAlchemy + asyncmy)."""
        return (
            f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )

    @property
    def database_url_sync(self) -> str:
        """URL de conexión síncrona (Alembic + pymysql)."""
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Devuelve una única instancia de Settings (cacheada).
    Útil para inyectar como dependencia en FastAPI.
    """
    return Settings()