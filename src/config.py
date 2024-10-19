from supabase import create_client, Client
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
