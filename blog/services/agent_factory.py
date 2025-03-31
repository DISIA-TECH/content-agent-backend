from typing import Dict, List, Type
from common.base_agent import BaseAgent
from blog.agents.educational import EducationalAgent
from blog.agents.case_study import CaseStudyAgent

class BlogAgentFactory:
    """Fábrica para crear instancias de agentes de blog."""
    
    _agent_classes = {
        "educational": EducationalAgent,
        "case_study": CaseStudyAgent,
        # Añadir otros agentes aquí
    }
    
    @classmethod
    def create_agent(cls, agent_type: str, model_name: str = "gpt-4o", temperature: float = 0.7) -> BaseAgent:
        """Crea una instancia de agente del tipo especificado.
        
        Args:
            agent_type: Tipo de agente a crear
            model_name: Nombre del modelo LLM a utilizar
            temperature: Parámetro de creatividad para el LLM
            
        Returns:
            Instancia del agente solicitado
            
        Raises:
            ValueError: Si el tipo de agente no es válido
        """
        if agent_type not in cls._agent_classes:
            valid_agents = list(cls._agent_classes.keys())
            raise ValueError(f"Tipo de agente inválido: {agent_type}. Opciones válidas: {valid_agents}")
        
        agent_class = cls._agent_classes[agent_type]
        return agent_class(model_name=model_name, temperature=temperature)
    
    @classmethod
    def get_available_agents(cls) -> List[str]:
        """Obtiene la lista de agentes disponibles.
        
        Returns:
            Lista de identificadores de agentes disponibles
        """
        return list(cls._agent_classes.keys())