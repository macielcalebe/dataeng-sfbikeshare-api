"""
Application configuration settings using Pydantic Settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    postgres_db_app: str = "sfbikeshare"
    postgres_user_app: str = "postgres"
    postgres_password_app: str = "postgres"
    postgres_host_app: str = "localhost"
    postgres_port_app: int = 5432

    api_title: str = "SF Bike Share API"
    api_description: str = "RESTful API for managing SF Bike Share data"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v2"

    @property
    def database_url(self) -> str:
        """
        Constructs the PostgreSQL database URL.
        """
        return (
            f"postgresql://{self.postgres_user_app}:{self.postgres_password_app}"
            f"@{self.postgres_host_app}:{self.postgres_port_app}/{self.postgres_db_app}"
        )


settings = Settings()
