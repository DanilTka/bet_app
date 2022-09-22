from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    api_key: str = "secret"
    inner_key: str = "secret"


class ServiceUrls(BaseSettings):
    url_base: str = "http://127.0.0.1:8000"


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "database_"

    driver: str = "postgresql+asyncpg"
    database: str = "bet"
    username: str = "postgres"
    password: str = "password"
    host: str = "localhost"

    echo: bool = False

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}/{self.database}"


db = DatabaseSettings()
service_urls = ServiceUrls()
auth_settings = AuthSettings()
