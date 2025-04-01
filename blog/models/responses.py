from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BlogResponse(BaseModel):
    """Modelo para respuestas de generación de blog."""
    content: str = Field(..., description="Contenido completo del artículo en formato markdown")
    title: str = Field(..., description="Título del artículo")
    summary: str = Field(..., description="Resumen del artículo")
    sections: List[Dict[str, Any]] = Field(..., description="Estructura de secciones del artículo")
    metadata: Optional[Dict[str, Any]] = Field({}, description="Metadatos adicionales")