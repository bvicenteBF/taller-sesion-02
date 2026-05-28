from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "supersecretkey_change_in_production"
    algorithm: str = "HS256"
    access_token_expire_seconds: int = 300

    model_config = {"env_file": ".env"}


settings = Settings()
