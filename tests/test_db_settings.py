from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresTestSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file=".env.test", env_prefix="POSTGRES_", env_file_encoding="utf-8",  extra='ignore'
    )

    def get_sqlalchemy_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class AuthTestSettings(BaseSettings):
    key: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="SECRET_", env_file_encoding="utf-8", extra='ignore'
    )


test_postgres_settings = PostgresTestSettings()
test_auth_settings = AuthTestSettings()

TEST_DATABASE_URL = test_postgres_settings.get_sqlalchemy_dsn()
