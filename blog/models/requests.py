from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class GenerationParameters(BaseModel):
    """Parámetros de configuración para la generación de contenido."""
    model: str = Field("gpt-4o", description="Modelo a utilizar")
    temperature: float = Field(0.7, ge=0.0, le=1.0, description="Temperatura para la generación")
    top_p: float = Field(1.0, ge=0.0, le=1.0, description="Valor de Top P para nucleus sampling")
    max_tokens: Optional[int] = Field(None, description="Número máximo de tokens a generar")
    presence_penalty: float = Field(0.0, ge=-2.0, le=2.0, description="Penalización por presencia")
    frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0, description="Penalización por frecuencia")
    stop: Optional[List[str]] = Field(None, description="Secuencias de parada")
    seed: Optional[int] = Field(None, description="Semilla para la generación")

class BlogRequest(BaseModel):
    """Modelo para solicitudes de generación de blog."""
    tema: str = Field(..., description="Tema principal del artículo")
    prompt_personalizado: Optional[str] = Field(None, description="Indicaciones personalizadas para la generación")
    longitud: str = Field("medium", description="Longitud del artículo: 'short', 'medium', 'long'")
    estilos: List[str] = Field(default=["informativo"], description="Estilos de contenido")
    urls: Optional[List[str]] = Field(None, description="URLs de referencia para el contenido")
    parametros: Optional[GenerationParameters] = Field(None, description="Parámetros avanzados de generación")