from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str = ""
