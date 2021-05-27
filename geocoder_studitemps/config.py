from pydantic import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):

    PROTOCOL: str = "https"

    GEOCODER_HOST: str

    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_SITE: str
    AUTH0_AUDIENCE: str


load_dotenv()
settings = Settings()