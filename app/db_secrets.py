from enum import Enum


class DbCredentials(Enum):
    HOST: str = "localhost"
    DATABASE: str = "fastapi_db"
    USERNAME: str = "postgres"
    PORT: str = "5544"
    PASSWORD: str = "admin"
