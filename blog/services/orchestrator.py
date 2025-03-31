from typing import Dict, List, Any, Optional
from common.services.llm_service import LLMService
from blog.services.agent_factory import BlogAgentFactory
from common.models.config import UserConfiguration
from common.utils.text_processor import TextProcessor
import logging

# Configurar logging
logger = logging.getLogger(__name__)

class BlogOrchestrator:
    """Orquestador para la generación de contenido de blog."""
    
    def __init__(self):
        """Inicializa el orquestador."""
        self.agent_factory = BlogAgentFactory
    
    def generate_content(self, 
                         tema: str, 
                         comentarios_adicionales: str, 
                         agentes: List[str],
                         user_config: Optional[UserConfiguration] = None) -> Dict[str, Any]:
        """Genera contenido de blog utilizando los agentes especificados.
        
        Args:
            tema: Tema principal del blog
            comentarios_adicionales: Comentarios adicionales sobre el blog
            agentes: Lista de agentes a utilizar
            user_config: Configuración personalizada del usuario
            
        Returns:
            Diccionario con el contenido generado
            
        Raises:
            ValueError: Si los agentes especificados no son válidos
        """
        # Validar agentes
        self._validate_agents(agentes)
        
        # Configurar modelo y parámetros
        model_config = user_config.model_settings if user_config else None
        generation_params = user_config.generation_params if user_config else None
        
        # Caso de un solo agente
        if len(agentes) == 1:
            agent = self.agent_factory.create_agent(
                agentes[0], 
                model_name=model_config.model_id if model_config else "gpt-4o",
                temperature=generation_params.temperature if generation_params else 0.7
            )
            return agent.generate_content(tema, comentarios_adicionales)
        
        # Caso de múltiples agentes
        return self._combine_agent_contents(tema, comentarios_adicionales, agentes, user_config)
    
    def _validate_agents(self, agentes: List[str]) -> None:
        """Valida que los agentes especificados sean válidos.
        
        Args:
            agentes: Lista de agentes a validar
            
        Raises:
            ValueError: Si algún agente no es válido
        """
        valid_agents = self.agent_factory.get_available_agents()
        if not agentes or not all(agente in valid_agents for agente in agentes):
            raise ValueError(f"Agentes inválidos. Opciones válidas: {valid_agents}")
    
    def _combine_agent_contents(self, 
                               tema: str, 
                               comentarios_adicionales: str, 
                               agentes: List[str],
                               user_config: Optional[UserConfiguration] = None) -> Dict[str, Any]:
        """Combina el contenido generado por múltiples agentes.
        
        Args:
            tema: Tema principal del blog
            comentarios_adicionales: Comentarios adicionales sobre el blog
            agentes: Lista de agentes a utilizar
            user_config: Configuración personalizada del usuario
            
        Returns:
            Diccionario con el contenido combinado
        """
        # Generar contenido con cada agente
        agent_contents = {}
        for agent_name in agentes:
            agent = self.agent_factory.create_agent(
                agent_name,
                model_name=user_config.model_settings.model_id if user_config and user_config.model_settings else "gpt-4o",
                temperature=user_config.generation_params.temperature if user_config and user_config.generation_params else 0.7
            )
            agent_contents[agent_name] = agent.generate_content(tema, comentarios_adicionales)
        
        # Combinar los contenidos usando un prompt de orquestación
        system_message = """Eres un experto orquestador de contenido para blogs.
        Tu tarea es combinar y sintetizar el contenido generado por diferentes agentes especializados
        en un único artículo de blog coherente y de alto impacto.
        
        Estructura final:
        1. Título atractivo
        2. Introducción que capte la atención
        3. Secciones principales con subtítulos claros
        4. Conclusión que resuma los puntos clave
        5. Llamada a la acción
        
        El resultado debe ser coherente, fluido y mantener la esencia de cada agente involucrado."""
        
        human_template = """Combina el contenido generado por los siguientes agentes en un único artículo de blog sobre el tema: {tema}
        
        Comentarios adicionales: {comentarios_adicionales}
        
        Contenido de los agentes:
        {agent_contents}
        
        Asegúrate de mantener la estructura: título, introducción, secciones con subtítulos, conclusión y llamada a la acción."""
        
        # Formatear el contenido de cada agente para el prompt
        formatted_contents = []
        for agent_name, content in agent_contents.items():
            formatted_contents.append(f"--- {agent_name.upper()} ---\n{content['content']}\n")
        
        # Generar contenido combinado
        combined_response = LLMService.generate_text(
            system_message=system_message,
            human_message=human_template.format(
                tema=tema,
                comentarios_adicionales=comentarios_adicionales,
                agent_contents="\n".join(formatted_contents)
            ),
            model_config=user_config.model_config if user_config else None,
            generation_params=user_config.generation_params if user_config else None
        )
        
        # Formatear la respuesta combinada
        return self._format_combined_response(combined_response)
    
    def _format_combined_response(self, raw_content: str) -> Dict[str, Any]:
        """Formatea la respuesta combinada.
        
        Args:
            raw_content: Contenido bruto generado
            
        Returns:
            Diccionario con el contenido formateado
        """
        import re
        
        # Extraer título
        title_match = re.match(r'^#\s+(.+?)$', raw_content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""
        
        # Dividir en secciones
        sections_raw = re.split(r'^##\s+(.+?)$', raw_content, flags=re.MULTILINE)[1:]
        
        # Agrupar títulos con contenido
        sections = []
        for i in range(0, len(sections_raw), 2):
            if i+1 < len(sections_raw):
                sections.append({
                    "title": sections_raw[i],
                    "content": sections_raw[i+1].strip()
                })
        
        # Extraer introducción y conclusión
        introduction = ""
        conclusion = ""
        
        if sections:
            if sections[0]["title"].lower() in ["introducción", "introduccion", "introduction"]:
                introduction = sections[0]["content"]
                sections = sections[1:]
            
            if sections and sections[-1]["title"].lower() in ["conclusión", "conclusion"]:
                conclusion = sections[-1]["content"]
                sections = sections[:-1]
        
        # Optimizar para blog
        optimized_content = TextProcessor.optimize_for_social_media(raw_content, "blog")
        
        return {
            "title": title,
            "introduction": introduction,
            "sections": sections,
            "conclusion": conclusion,
            "content": optimized_content
        }