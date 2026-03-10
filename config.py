from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    api_key: SecretStr
    base_url: str
    model: str
    temperature: float = 0.0
    recursion_limit: int = 100
    output_dir: str = "./generated_project"

    @property
    def api_key(self) -> str:
        return self.api_key.get_secret_value()

    @property
    def base_url(self) -> str:
        return self.base_url

    @property
    def model(self) -> str:
        return self.model
