from fastapi import APIRouter
from blog.api.routes import router as blog_router
#from linkedin.api.routes import router as linkedin_router

# Crear router principal
api_router = APIRouter()

# Incluir routers de dominios
api_router.include_router(blog_router)
#api_router.include_router(linkedin_router)

@api_router.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API."""
    return {"status": "ok"}