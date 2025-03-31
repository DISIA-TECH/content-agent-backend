from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Optional, Any, Union

class PromptConfiguration(BaseModel):
    """Configuración para personalización de prompts."""
    template_id: str = Field(description="ID de la plantilla predefinida")
    variables: Optional[Dict[str, Any]] = Field(None, description="Variables para la plantilla")
    custom_sections: Optional[Dict[str, str]] = Field(None, description="Secciones personalizadas")
    full_override: Optional[str] = Field(None, description="Anulación completa del prompt")

class ModelConfiguration(BaseModel):
    """Configuración para el modelo de lenguaje."""
    model_config = ConfigDict(protected_namespaces=())
    
    model_id: str = Field(description="ID del modelo (ej: 'gpt-4o')")
    provider: str = Field("openai", description="Proveedor del modelo")
    api_key: Optional[str] = Field(None, description="API key del usuario")
    base_url: Optional[str] = Field(None, description="URL base para API personalizada")

class GenerationParameters(BaseModel):
    """Parámetros para la generación de contenido."""
    temperature: float = Field(0.7, description="Temperatura (creatividad)", ge=0.0, le=1.0)
    top_p: float = Field(1.0, description="Top-p (diversidad)", ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, description="Longitud máxima en tokens")
    frequency_penalty: float = Field(0.0, description="Penalización por frecuencia", ge=0.0, le=2.0)
    presence_penalty: float = Field(0.0, description="Penalización por presencia", ge=0.0, le=2.0)

class UserConfiguration(BaseModel):
    """Configuración completa del usuario."""
    model_config = ConfigDict(protected_namespaces=())
    
    prompt_config: Optional[PromptConfiguration] = Field(None, description="Configuración del prompt")
    model_settings: Optional[ModelConfiguration] = Field(None, description="Configuración del modelo")  # Cambiado de model_config a model_settings
    generation_params: Optional[GenerationParameters] = Field(None, description="Parámetros de generación")