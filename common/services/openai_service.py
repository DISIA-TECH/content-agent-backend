from typing import Dict, Any, List, Optional
from openai import OpenAI
import os
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """Servicio para interactuar directamente con la API de OpenAI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Inicializa el servicio de OpenAI.
        
        Args:
            api_key: Clave de API de OpenAI (opcional, por defecto usa la variable de entorno)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    
    def chat_completion(self, 
                        system_message: str, 
                        user_message: str, 
                        model: str = "gpt-4o", 
                        temperature: float = 0.7) -> str:
        """Genera una respuesta usando el modelo de chat de OpenAI.
        
        Args:
            system_message: Mensaje del sistema
            user_message: Mensaje del usuario
            model: Modelo a utilizar
            temperature: Temperatura para la generación
            
        Returns:
            Texto generado
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error en chat_completion: {str(e)}")
            raise
    
    def web_search(self, query: str, model: str = "gpt-4o") -> str:
        """Realiza una búsqueda web sobre un tema.
        
        Args:
            query: Consulta de búsqueda
            model: Modelo a utilizar
            
        Returns:
            Resultados de la búsqueda
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                tools=[{
                    "type": "web_search",
                    "search_context_size": "medium",
                }],
                messages=[
                    {"role": "system", "content": "Eres un investigador profesional especializado en encontrar información relevante."},
                    {"role": "user", "content": query}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error en web_search: {str(e)}")
            raise
    
    def analyze_url(self, url: str, query: str, model: str = "gpt-4o-search-preview") -> str:
        """Analiza una URL para extraer información relevante.
        
        Args:
            url: URL a analizar
            query: Consulta sobre qué información extraer
            model: Modelo a utilizar
            
        Returns:
            Información extraída
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                web_search_options={},
                messages=[
                    {"role": "system", "content": "Eres un investigador profesional especializado en analizar páginas web."},
                    {"role": "user", "content": f"Navega a esta URL: {url}. {query}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error al analizar URL {url}: {str(e)}")
            raise