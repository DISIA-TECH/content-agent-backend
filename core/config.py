from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from typing import List, Optional, Union
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings(BaseSettings):
    """Configuraciones de la aplicación."""
    
    # Información del proyecto
    PROJECT_NAME: str = "Content Generator API"
    PROJECT_DESCRIPTION: str = "API para generar contenido estratégico para LinkedIn y Blog usando agentes especializados"
    PROJECT_VERSION: str = "0.1.0"
    
    # API
    API_V1_STR: str = "/api/v1"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8001"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    model_config = {
        "case_sensitive": True,
        "env_file": ".env"
    }

# Instancia de configuración
settings = Settings()