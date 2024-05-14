from pydantic_settings import BaseSettings, SettingsConfigDict

class Configs(BaseSettings):
    database_hostname:str
    database_port:str
    database_username:str
    database_password:str
    database_name:str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    ENV: str = "local"

    model_config = SettingsConfigDict(env_file=".env")

configs = Configs()