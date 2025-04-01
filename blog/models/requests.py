from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BlogRequest(BaseModel):
    """Modelo para solicitudes de generación de blog."""
    tema: str = Field(..., description="Tema principal del artículo")
    prompt_personalizado: Optional[str] = Field(None, description="Indicaciones personalizadas para la generación")
    longitud: str = Field("medium", description="Longitud del artículo: 'short' (500 palabras), 'medium' (1000 palabras), 'long' (2000 palabras)")
    estilos: List[str] = Field(default=["informativo"], description="Estilos de contenido: informativo, persuasivo, narrativo, técnico")
    urls: Optional[List[str]] = Field(None, description="URLs de referencia para el contenido")