from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    api_key: str = "secret"
    inner_key: str = "secret"


class ServiceUrls(BaseSettings):
    url_base: str = "http://127.0.0.1:8001"


service_urls = ServiceUrls()
auth_settings = AuthSettings()
