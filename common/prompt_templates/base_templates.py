from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BasePromptTemplate(ABC):
    """Clase base para todas las plantillas de prompts."""
    
    @abstractmethod
    def get_system_message(self) -> str:
        """Obtiene el mensaje del sistema que define el rol y comportamiento."""
        pass
    
    @abstractmethod
    def get_human_template(self) -> str:
        """Obtiene la plantilla para el mensaje del usuario."""
        pass
    
    def get_prompt_data(self) -> Dict[str, str]:
        """Obtiene los datos completos del prompt."""
        return {
            "system_message": self.get_system_message(),
            "human_template": self.get_human_template()
        }

class ContentPromptTemplate(BasePromptTemplate):
    """Plantilla base para prompts de generación de contenido."""
    
    def __init__(self, 
                 role_description: str,
                 content_objective: str,
                 style_guidance: str,
                 structure_description: str,
                 additional_instructions: Optional[str] = None):
        """Inicializa la plantilla con los componentes necesarios."""
        self.role_description = role_description
        self.content_objective = content_objective
        self.style_guidance = style_guidance
        self.structure_description = structure_description
        self.additional_instructions = additional_instructions
    
    def get_system_message(self) -> str:
        """Construye un mensaje del sistema estructurado."""
        system_message = f"""Eres un experto en {self.role_description}.
Tu objetivo es {self.content_objective}.

Estructura:
{self.structure_description}

{self.style_guidance}"""
        
        if self.additional_instructions:
            system_message += f"\n\n{self.additional_instructions}"
            
        return system_message
    
    def get_human_template(self) -> str:
        """Proporciona una plantilla genérica para el mensaje del usuario."""
        return """Genera contenido sobre el tema: {tema}

Comentarios adicionales: {comentarios_adicionales}

No uses asteriscos para negrita y usa emojis, es importante buscar la viralidad"""


class PromptBuilder:
    """Utilidad para construir prompts complejos a partir de componentes."""
    
    def __init__(self):
        self.system_components = []
        self.human_components = []
    
    def add_system_component(self, component: str) -> 'PromptBuilder':
        """Añade un componente al mensaje del sistema."""
        self.system_components.append(component)
        return self
    
    def add_human_component(self, component: str) -> 'PromptBuilder':
        """Añade un componente al mensaje del usuario."""
        self.human_components.append(component)
        return self
    
    def build(self) -> Dict[str, str]:
        """Construye el prompt completo."""
        return {
            "system_message": "\n\n".join(self.system_components),
            "human_template": "\n\n".join(self.human_components)
        }