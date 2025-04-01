from typing import Dict, Any, Optional
from common.base_agent import BaseAgent
import json
import logging

logger = logging.getLogger(__name__)

class OutlinePlannerAgent(BaseAgent):
    """
    Agente Planificador (Outline Planner) - Especialidad: estructura y enfoque
    Se encarga de generar la estructura del artículo a partir de un tema dado.
    """
    
    def _get_prompt_data(self) -> Dict[str, str]:
        """Obtiene los datos de prompt específicos para este agente."""
        system_message = """Eres un experto en content marketing y redacción SEO. Vas a crear la estructura para un artículo de blog al estilo Product Hackers sobre el tema proporcionado.

Tu objetivo es elaborar un esquema para un artículo bien estructurado con:
- Un título profesional y atractivo que capte interés sobre el tema
- Una introducción efectiva que contextualice el tema y establezca su relevancia
- Secciones bien definidas con encabezados informativos que desarrollen el tema
- Una conclusión que ofrezca reflexiones finales valiosas

Directrices para la estructura:
1. El título debe ser claro y atractivo (formato H1)
2. La introducción debe establecer contexto y relevancia de manera profesional
3. El cuerpo debe organizarse en secciones lógicas con progresión clara
4. Los encabezados deben ser descriptivos y orientados al valor para el lector
5. Considera dónde podrían incluirse ejemplos concretos o casos de aplicación
6. La conclusión debe proporcionar perspectivas finales o recomendaciones prácticas

Responde con un objeto JSON que contenga:
- title: título del artículo
- introduction: breve descripción de la introducción
- sections: array de objetos, cada uno con:
  - heading: encabezado de la sección
  - subheadings: array de subtítulos y puntos a cubrir
  - key_points: puntos clave a desarrollar
- conclusion: descripción de la conclusión
"""
        
        human_template = """Genera una estructura profesional y bien organizada para un artículo de blog sobre: {tema}

{instrucciones_longitud}

Estilos solicitados:
{instrucciones_estilo}

{prompt_personalizado}

Crea un esquema que permita generar un artículo de calidad profesional que resulte natural y humano pero mantenga la formalidad y autoridad apropiadas.

Genera una estructura completa y bien organizada en formato JSON válido, siguiendo exactamente la estructura solicitada."""
        
        return {
            "system_message": system_message,
            "human_template": human_template
        }
    
    def generate_outline(self, tema: str, longitud: str, estilos: list, prompt_personalizado: Optional[str] = None) -> Dict[str, Any]:
        """Genera la estructura del artículo.
        
        Args:
            tema: Tema del artículo
            longitud: Longitud deseada ('short', 'medium', 'long')
            estilos: Lista de estilos ('informativo', 'persuasivo', 'narrativo', 'técnico')
            prompt_personalizado: Instrucciones adicionales
            
        Returns:
            Estructura del artículo en formato JSON
        """
        # Adaptar según la longitud solicitada
        instrucciones_longitud = {
            "short": "El artículo debe ser conciso (aproximadamente 500 palabras). Planifica 3-4 secciones principales enfocadas en los aspectos más relevantes.",
            "medium": "El artículo debe tener una extensión moderada (aproximadamente 1000 palabras). Planifica 4-6 secciones con un nivel adecuado de detalle.",
            "long": "El artículo debe ser completo y detallado (aproximadamente 2000 palabras). Planifica 6-8 secciones con desarrollo en profundidad."
        }
        
        # Adaptar según los estilos solicitados
        instrucciones_estilo = ""
        if "informativo" in estilos:
            instrucciones_estilo += "• Estilo informativo: Orientado a proporcionar información valiosa con precisión y contexto adecuado.\n"
        if "persuasivo" in estilos:
            instrucciones_estilo += "• Estilo persuasivo: Estructurado para construir argumentos convincentes basados en evidencia y beneficios.\n"
        if "narrativo" in estilos:
            instrucciones_estilo += "• Estilo narrativo: Incorporando ejemplos y estudios de caso para ilustrar conceptos clave de manera efectiva.\n"
        if "técnico" in estilos:
            instrucciones_estilo += "• Estilo técnico: Profundizando en aspectos especializados con precisión y claridad para audiencias con conocimiento del sector.\n"
        
        # Generar la estructura
        response = self.generate_content(
            tema=tema,
            instrucciones_longitud=instrucciones_longitud.get(longitud, instrucciones_longitud["medium"]),
            instrucciones_estilo=instrucciones_estilo,
            prompt_personalizado=prompt_personalizado if prompt_personalizado else "Sin instrucciones adicionales."
        )
        
        return response
    
    def _format_response(self, raw_content: str) -> Dict[str, Any]:
        """Formatea la respuesta JSON."""
        try:
            # Intentar parsear la respuesta como JSON
            return json.loads(raw_content)
        except json.JSONDecodeError:
            logger.error(f"Error parsing JSON response: {raw_content}")
            # Si falla, extraer la parte JSON de la respuesta
            try:
                json_start = raw_content.find('{')
                json_end = raw_content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = raw_content[json_start:json_end]
                    return json.loads(json_str)
                else:
                    raise ValueError("No se pudo encontrar un objeto JSON en la respuesta")
            except Exception as e:
                logger.error(f"Error extracting JSON from response: {e}")
                # Crear una estructura básica como fallback
                return {
                    "title": f"Artículo sobre {raw_content[:50]}...",
                    "introduction": "Introducción al tema.",
                    "sections": [{"heading": "Sección 1", "subheadings": [], "key_points": []}],
                    "conclusion": "Conclusión sobre el tema."
                }