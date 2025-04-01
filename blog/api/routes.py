from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import Dict, Any, List
import logging
from blog.models.requests import BlogRequest
from blog.models.responses import BlogResponse
from blog.services.orchestrator import BlogOrchestrator

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router - asegurarse de que se llame 'router' para que pueda ser importado
router = APIRouter(prefix="/blog", tags=["blog"])

# Inicializar orquestador
orchestrator = BlogOrchestrator()

@router.get("/")
async def blog_root():
    """Endpoint raíz del generador de blog."""
    return {"message": "Blog Content Generator API"}

@router.get("/estilos")
async def get_styles():
    """Obtiene los estilos y longitudes disponibles para la generación de blog."""
    return {
        "estilos": [
            {"id": "informativo", "name": "Informativo", "description": "Contenido objetivo, claro y basado en datos. Prioriza hechos y explicaciones."},
            {"id": "persuasivo", "name": "Persuasivo", "description": "Enfatiza beneficios, soluciones y argumentos convincentes. Incluye llamadas a la acción."},
            {"id": "narrativo", "name": "Narrativo", "description": "Incluye elementos de storytelling, casos de estudio y experiencias. Conecta emocionalmente."},
            {"id": "técnico", "name": "Técnico", "description": "Profundiza en aspectos especializados, incluye terminología del sector y detalles técnicos."}
        ],
        "longitudes": [
            {"id": "short", "name": "Corto", "description": "Aproximadamente 500 palabras"},
            {"id": "medium", "name": "Medio", "description": "Aproximadamente 1000 palabras"},
            {"id": "long", "name": "Largo", "description": "Aproximadamente 2000 palabras"}
        ]
    }

@router.post("/generar", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    """Genera contenido de blog basado en los parámetros proporcionados."""
    try:
        result = orchestrator.generate_blog_content(
            tema=request.tema,
            longitud=request.longitud,
            estilos=request.estilos,
            urls=request.urls,
            prompt_personalizado=request.prompt_personalizado
        )
        
        return BlogResponse(
            content=result["content"],
            title=result["title"],
            summary=result["summary"],
            sections=result["sections"]
        )
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generando contenido: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generando contenido. Por favor, inténtalo de nuevo.")

@router.post("/subir-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Recibe un archivo PDF para procesamiento futuro."""
    try:
        # Aquí se implementaría la lógica para procesar el PDF
        # Por ahora solo devolvemos confirmación
        return {"filename": file.filename, "status": "PDF recibido correctamente"}
    except Exception as e:
        logger.error(f"Error al procesar el PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al procesar el archivo PDF")