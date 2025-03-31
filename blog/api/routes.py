from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import logging
from blog.models.requests import BlogContentRequest
from blog.models.responses import BlogContentResponse
from blog.services.orchestrator import BlogOrchestrator
from common.models.config import UserConfiguration

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/blog", tags=["blog"])

# Inicializar orquestador
orchestrator = BlogOrchestrator()

@router.get("/agentes")
async def get_agents():
    """Obtiene los agentes disponibles para generación de contenido de blog."""
    return {
        "agentes": [
            {"id": "educational", "name": "Educativo", "description": "Genera contenido educativo y explicativo"},
            {"id": "case_study", "name": "Caso de Estudio", "description": "Genera casos de estudio detallados"},
            {"id": "how_to", "name": "Tutorial", "description": "Genera tutoriales paso a paso"},
            {"id": "industry_news", "name": "Noticias del Sector", "description": "Genera análisis de noticias del sector"}
        ]
    }

@router.post("/generar", response_model=BlogContentResponse)
async def generate_content(request: BlogContentRequest):
    """Genera contenido de blog usando los agentes especificados."""
    try:
        # Crear configuración de usuario si se proporciona
        user_config = None
        if hasattr(request, 'user_config') and request.user_config:
            user_config = request.user_config
        
        # Generar contenido
        result = orchestrator.generate_content(
            tema=request.tema,
            comentarios_adicionales=request.comentarios_adicionales,
            agentes=request.agentes,
            user_config=user_config
        )
        
        # Crear respuesta
        return BlogContentResponse(
            content=result["content"],
            title=result.get("title", ""),
            introduction=result.get("introduction", ""),
            sections=result.get("sections", []),
            conclusion=result.get("conclusion", ""),
            metadata=result.get("metadata", {})
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generando contenido: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generando contenido. Por favor, inténtalo de nuevo.")