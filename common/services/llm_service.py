from typing import Dict, Any, Optional, List, Union
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from common.models.config import ModelConfiguration, GenerationParameters

class LLMService:
    """Servicio centralizado para interactuar con modelos de lenguaje."""
    
    @staticmethod
    def get_llm(model_config: Optional[ModelConfiguration] = None, 
                generation_params: Optional[GenerationParameters] = None):
        """Obtiene una instancia de LLM configurada.
        
        Args:
            model_config: Configuración del modelo
            generation_params: Parámetros de generación
            
        Returns:
            Instancia de ChatOpenAI configurada
        """
        # Valores por defecto
        model_name = "gpt-4o"
        temperature = 0.7
        
        # Aplicar configuración de modelo si existe
        if model_config:
            model_name = model_config.model_id
            
            # Configurar API key personalizada si existe
            kwargs = {}
            if model_config.api_key:
                kwargs["openai_api_key"] = model_config.api_key
            if model_config.base_url:
                kwargs["openai_api_base"] = model_config.base_url
        else:
            kwargs = {}
        
        # Aplicar parámetros de generación si existen
        if generation_params:
            temperature = generation_params.temperature
            
            # Añadir otros parámetros si están definidos
            if generation_params.max_tokens:
                kwargs["max_tokens"] = generation_params.max_tokens
            if generation_params.top_p != 1.0:
                kwargs["top_p"] = generation_params.top_p
            if generation_params.frequency_penalty != 0.0:
                kwargs["frequency_penalty"] = generation_params.frequency_penalty
            if generation_params.presence_penalty != 0.0:
                kwargs["presence_penalty"] = generation_params.presence_penalty
        
        # Crear y devolver la instancia de LLM
        return ChatOpenAI(model_name=model_name, temperature=temperature, **kwargs)
    
    @staticmethod
    def generate_text(system_message: str, 
                      human_message: str, 
                      model_config: Optional[ModelConfiguration] = None,
                      generation_params: Optional[GenerationParameters] = None) -> str:
        """Genera texto usando un LLM.
        
        Args:
            system_message: Mensaje del sistema
            human_message: Mensaje del usuario
            model_config: Configuración del modelo
            generation_params: Parámetros de generación
            
        Returns:
            Texto generado
        """
        # Obtener LLM configurado
        llm = LLMService.get_llm(model_config, generation_params)
        
        # Crear prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
        ])
        
        # Crear y ejecutar cadena
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run({})