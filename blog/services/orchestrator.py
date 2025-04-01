from typing import Dict, Any, List, Optional
from blog.agents.web_research_agent import WebResearchAgent
from blog.agents.outline_planner_agent import OutlinePlannerAgent
from blog.agents.content_writer_agent import ContentWriterAgent
from blog.agents.style_editor_agent import StyleCoherenceEditorAgent
from common.utils.text_processor import TextProcessor
import logging

logger = logging.getLogger(__name__)

class BlogOrchestrator:
    """Orquestador para la generación de contenido de blog."""
    
    def __init__(self, model_name: str = "gpt-4o"):
        """Inicializa el orquestador con los agentes necesarios.
        
        Args:
            model_name: Nombre del modelo a utilizar
        """
        self.outline_planner = OutlinePlannerAgent(model_name)
        self.content_writer = ContentWriterAgent(model_name)
        self.style_editor = StyleCoherenceEditorAgent(model_name)
        self.web_researcher = WebResearchAgent(model_name)
    
    def generate_blog_content(self, 
                             tema: str, 
                             longitud: str, 
                             estilos: List[str], 
                             urls: Optional[List[str]] = None, 
                             prompt_personalizado: Optional[str] = None) -> Dict[str, Any]:
        """Genera contenido de blog completo.
        
        Args:
            tema: Tema del artículo
            longitud: Longitud deseada ('short', 'medium', 'long')
            estilos: Lista de estilos ('informativo', 'persuasivo', 'narrativo', 'técnico')
            urls: Lista de URLs de referencia
            prompt_personalizado: Instrucciones adicionales
            
        Returns:
            Diccionario con el contenido generado
        """
        # Realizar investigación web si se proporcionan URLs
        url_research = ""
        if urls and len(urls) > 0:
            logger.info(f"Procesando {len(urls)} URLs para el tema: {tema}")
            research_results = self.web_researcher.research_urls(tema, urls)
            url_research = self.web_researcher.synthesize_research(research_results, tema)
            
            # Añadir la investigación al prompt personalizado
            additional_context = f"\n\nINFORMACIÓN DE REFERENCIA:\n{url_research}"
            if prompt_personalizado:
                prompt_personalizado += additional_context
            else:
                prompt_personalizado = additional_context
        
        # Generar estructura del artículo
        logger.info(f"Generando outline para tema: {tema}")
        outline = self.outline_planner.generate_outline(
            tema=tema,
            longitud=longitud,
            estilos=estilos,
            prompt_personalizado=prompt_personalizado
        )
        
        # Generar contenido inicial
        logger.info(f"Generando contenido para tema: {tema}")
        draft_content = self.content_writer.write_content(
            tema=tema,
            outline=outline,
            longitud=longitud,
            estilos=estilos,
            urls=urls,
            prompt_personalizado=prompt_personalizado
        )
        
        # Refinar el contenido
        logger.info(f"Refinando el contenido para tema: {tema}")
        final_content = self.style_editor.edit_content(
            content=draft_content,
            estilos=estilos
        )
        
        # Extraer un resumen breve del artículo
        summary = TextProcessor.extract_summary(final_content)
        
        return {
            "content": final_content,
            "title": outline["title"],
            "summary": summary,
            "sections": outline["sections"]
        }