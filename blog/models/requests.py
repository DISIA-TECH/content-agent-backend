from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from common.models.config import UserConfiguration

class BlogContentRequest(BaseModel):
    """Solicitud para generación de contenido de blog."""
    tema: str = Field(..., description="Tema principal del blog")
    comentarios_adicionales: str = Field(..., description="Comentarios adicionales sobre el blog")
    agentes: List[str] = Field(..., description="Lista de agentes a utilizar (educational, case_study, how_to, industry_news)")
    user_config: Optional[UserConfiguration] = Field(None, description="Configuración personalizada del usuario")