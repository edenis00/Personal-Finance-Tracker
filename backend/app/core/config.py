"""
Configuration settings
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    database_url: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_port: str | None = None
    db_host: str | None = None
    db_name: str | None = None

    secret_key: str
    algorithm: str

    access_token_expire_minutes: int = 60
    cors_allowed_origins: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

    @property
    def DATABASE_URL(self) -> str:
        """
        Construct the database URL from individual components if not provided directly.
        """
        if self.database_url:
            return self.database_url

        if not all([self.db_user, self.db_password, self.db_host, self.db_port, self.db_name]):
            raise ValueError("Incomplete database configuration")

        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def ALLOWED_ORIGINS(self):
        """
        Get the list of allowed origins for CORS from a comma-separated string.
        """
        return [origins.strip() for origins in self.cors_allowed_origins.split(",")]

settings = Settings()
