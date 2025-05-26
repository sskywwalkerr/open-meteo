from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()

broker_url = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0"
result_backend = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0"
broker_connection_retry_on_startup = True
