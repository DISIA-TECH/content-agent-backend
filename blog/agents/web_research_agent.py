from typing import Dict, Any, List, Optional
from common.services.openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)

class WebResearchAgent:
    """
    Agente Investigador Web (Web Research Agent) - Especialidad: buscar y sintetizar información de URLs
    Se encarga de investigar en la web para enriquecer el contenido del artículo.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        """Inicializa el agente de investigación web.
        
        Args:
            model_name: Nombre del modelo a utilizar
        """
        self.openai_service = OpenAIService()
        self.model_name = model_name
    
    def research_urls(self, tema: str, urls: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """Investiga un tema usando la funcionalidad de búsqueda web y/o las URLs proporcionadas.
        
        Args:
            tema: Tema a investigar
            urls: Lista de URLs a analizar
            
        Returns:
            Lista de resultados de investigación
        """
        research_results = []
        
        # Si no hay URLs proporcionadas, realizar búsqueda web sobre el tema
        if not urls or len(urls) == 0:
            try:
                logger.info(f"Realizando búsqueda web sobre: {tema}")
                query = f"""Investiga información actualizada, estadísticas, y perspectivas 
                relevantes sobre: {tema}. Proporciona un resumen detallado de los hallazgos más importantes 
                que serían útiles para escribir un artículo de blog profesional sobre este tema."""
                
                research_summary = self.openai_service.web_search(query, self.model_name)
                research_results.append({"source": "web_search", "content": research_summary})
                
            except Exception as e:
                logger.error(f"Error en la búsqueda web: {str(e)}")
                research_results.append({"source": "web_search", "content": f"Error en la búsqueda web: {str(e)}"})
        
        # Investigar cada URL proporcionada
        if urls and len(urls) > 0:
            for url in urls:
                try:
                    logger.info(f"Analizando URL: {url}")
                    query = f"""Extrae la información más relevante y valiosa para crear un artículo de blog sobre: {tema}. 
                    Resume los puntos clave, datos importantes y perspectivas que serían útiles."""
                    
                    url_summary = self.openai_service.analyze_url(url, query, "gpt-4o-search-preview")
                    research_results.append({"source": url, "content": url_summary})
                    
                except Exception as e:
                    logger.error(f"Error al analizar URL {url}: {str(e)}")
                    research_results.append({"source": url, "content": f"Error al analizar esta URL: {str(e)}"})
        
        return research_results
    
    def synthesize_research(self, research_results: List[Dict[str, str]], tema: str) -> str:
        """Sintetiza los resultados de investigación en un formato útil para la generación de contenido.
        
        Args:
            research_results: Resultados de investigación
            tema: Tema del artículo
            
        Returns:
            Síntesis de la investigación
        """
        if not research_results:
            return "No se encontró información relevante."
            
        try:
            # Concatenar todos los resultados de investigación
            all_research = "\n\n".join([f"Fuente: {r['source']}\n{r['content']}" for r in research_results])
            
            system_message = """Eres un especialista en sintetizar investigaciones. 
            Tu tarea es analizar toda la información recopilada y organizarla en un formato útil para 
            la creación de contenido. Identifica tendencias, datos importantes, perspectivas valiosas 
            y puntos de vista diversos."""
            
            user_message = f"""Aquí está la información recopilada sobre: {tema}
            
            {all_research}
            
            Sintetiza esta información en un formato estructurado que sea útil para crear un artículo de blog. 
            Organiza los datos importantes, perspectivas valiosas, citas relevantes y tendencias en categorías 
            lógicas. Identifica también los puntos de consenso y controversia, si los hay."""
            
            return self.openai_service.chat_completion(system_message, user_message, self.model_name)
            
        except Exception as e:
            logger.error(f"Error al sintetizar la investigación: {str(e)}")
            return f"Error al sintetizar la investigación: {str(e)}"