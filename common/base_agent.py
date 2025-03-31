from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import SystemMessage, HumanMessage

class BaseAgent(ABC):
    """Clase base abstracta para todos los agentes de generación de contenido."""
    
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.7):
        """Inicializa el agente base con un modelo de lenguaje.
        
        Args:
            model_name: Nombre del modelo LLM a utilizar
            temperature: Parámetro de creatividad para el LLM (0.0-1.0)
        """
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    
    @abstractmethod
    def _get_prompt_data(self) -> Dict[str, str]:
        """Obtiene los datos de prompt específicos para este agente.
        
        Returns:
            Diccionario con system_message y human_template
        """
        pass
    
    def generate_content(self, tema: str, comentarios_adicionales: str, **kwargs) -> Dict[str, str]:
        """Genera contenido basado en el tema y comentarios proporcionados.
        
        Args:
            tema: Tema principal para la generación de contenido
            comentarios_adicionales: Contexto o requisitos adicionales
            **kwargs: Parámetros adicionales específicos del agente
            
        Returns:
            Diccionario con las partes del contenido generado
        """
        # Obtener datos de prompt específicos del agente
        prompt_data = self._get_prompt_data()
        
        # Crear el prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=prompt_data["system_message"]),
            HumanMessage(content=prompt_data["human_template"].format(
                tema=tema,
                comentarios_adicionales=comentarios_adicionales,
                **kwargs
            ))
        ])
        
        # Ejecutar la cadena
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run({})
        
        # Formatear y devolver la respuesta
        return self._format_response(response)
    
    def _format_response(self, raw_content: str) -> Dict[str, str]:
        """Formatea el contenido bruto en secciones estructuradas.
        
        Args:
            raw_content: Texto bruto del LLM
            
        Returns:
            Diccionario con hook, context, body, cta y contenido completo
        """
        from common.utils.text_processor import TextProcessor
        return TextProcessor.extract_content_sections(raw_content)