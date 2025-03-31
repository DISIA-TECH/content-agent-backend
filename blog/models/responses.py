from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BlogSection(BaseModel):
    """Sección de un blog."""
    title: str = Field(..., description="Título de la sección")
    content: str = Field(..., description="Contenido de la sección")

class BlogContentResponse(BaseModel):
    """Respuesta para contenido de blog generado."""
    content: str = Field(..., description="Contenido completo del blog")
    title: str = Field(..., description="Título del blog")
    introduction: str = Field(..., description="Introducción del blog")
    sections: List[BlogSection] = Field(..., description="Secciones del blog")
    conclusion: str = Field(..., description="Conclusión del blog")
    metadata: Optional[Dict[str, Any]] = Field({}, description="Metadatos adicionales")