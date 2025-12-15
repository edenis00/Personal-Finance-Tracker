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

settings = Settings()
