from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    """ database_url: str = "sqlite:///./skiza.db" """
    
    default_url:str="127.0.0.1:8000/"
    database_hostname:str = "localhost"
    database_port:str = "5432"
    database_name:str = "skiza"
    database_password:str = "Kirui%401991"
    database_username:str = "ken"
    secret_key: str = "d963346e21281c663b756f17a767b8e64d2664b70c6e4dc5d0d9e9dd7f14f69c"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = "..env"

settings = Settings()


