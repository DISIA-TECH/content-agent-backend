from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
import os

# Corregir el import para usar el formato con guion
from langchain_openai import ChatOpenAI

class BaseAgent(ABC):
    """Clase base abstracta para todos los agentes de generación de contenido."""
    
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.7, **kwargs):
        """Inicializa el agente base con un modelo de lenguaje y parámetros.
        
        Args:
            model_name: Nombre del modelo LLM a utilizar
            temperature: Parámetro de creatividad para el LLM (0.0-1.0)
            **kwargs: Parámetros adicionales para el modelo
        """
        self.llm = ChatOpenAI(
            model=model_name, 
            temperature=temperature,
            top_p=kwargs.get('top_p', 1.0),
            max_tokens=kwargs.get('max_tokens'),
            presence_penalty=kwargs.get('presence_penalty', 0.0),
            frequency_penalty=kwargs.get('frequency_penalty', 0.0),
            stop=kwargs.get('stop'),
            seed=kwargs.get('seed')
        )
        self.output_parser = StrOutputParser()
    
    @abstractmethod
    def _get_prompt_data(self) -> Dict[str, str]:
        """Obtiene los datos de prompt específicos para este agente.
        
        Returns:
            Diccionario con system_message y human_template
        """
        pass
    
    def generate_content(self, **kwargs) -> Dict[str, Any]:
        """Genera contenido basado en los parámetros proporcionados.
        
        Args:
            **kwargs: Parámetros específicos del agente
            
        Returns:
            Diccionario con el contenido generado
        """
        # Obtener datos de prompt específicos del agente
        prompt_data = self._get_prompt_data()
        
        # Crear el prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=prompt_data["system_message"]),
            HumanMessage(content=prompt_data["human_template"].format(**kwargs))
        ])
        
        # Ejecutar la cadena
        chain = prompt | self.llm | self.output_parser
        response = chain.invoke({})
        
        # Formatear y devolver la respuesta
        return self._format_response(response)
    
    @abstractmethod
    def _format_response(self, raw_content: str) -> Dict[str, Any]:
        """Formatea el contenido bruto en el formato deseado.
        
        Args:
            raw_content: Texto bruto del LLM
            
        Returns:
            Diccionario con el contenido formateado
        """
        pass