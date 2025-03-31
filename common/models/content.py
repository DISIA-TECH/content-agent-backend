from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ContentSection(BaseModel):
    """Sección de contenido generado."""
    title: Optional[str] = Field(None, description="Título de la sección")
    content: str = Field(..., description="Contenido de la sección")

class BaseContentResponse(BaseModel):
    """Respuesta base para contenido generado."""
    content: str = Field(..., description="Contenido completo generado")
    sections: Dict[str, str] = Field(..., description="Secciones del contenido")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadatos adicionales")