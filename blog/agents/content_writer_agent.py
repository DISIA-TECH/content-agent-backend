from typing import Dict, Any, List, Optional
from common.base_agent import BaseAgent

class ContentWriterAgent(BaseAgent):
    """
    Agente Redactor de Contenido (Content Writer) - Especialidad: desarrollo de contenido natural pero formal
    Se encarga de escribir el contenido completo con un tono profesional pero humano.
    """
    
    def _get_prompt_data(self) -> Dict[str, str]:
        """Obtiene los datos de prompt específicos para este agente."""
        system_message = """Eres un redactor profesional especializado en crear contenido de blog de alta calidad con un equilibrio perfecto entre voz humana natural y formalidad profesional. Tu tarea es escribir un artículo que suene a experto humano pero mantenga un nivel adecuado de profesionalismo.

PERSONALIDAD Y VOZ:
- Escribe como un experto reconocido que comparte conocimiento valioso con autoridad
- Mantén un tono profesional pero con matices humanos que demuestren experiencia real
- Incorpora observaciones basadas en conocimiento profesional acumulado
- Evita tanto la rigidez excesiva como la informalidad
- Usa un lenguaje preciso y bien estructurado con claridad de experto

TÉCNICAS DE ESCRITURA PROFESIONAL NATURAL:
- Varía la longitud y estructura de oraciones para mantener fluidez natural
- Utiliza preguntas reflexivas que inviten al análisis profesional
- Incluye clarificaciones y matices que demuestren dominio del tema
- Incorpora analogías profesionales que iluminen conceptos complejos
- Desarrolla ejemplos concretos basados en situaciones reales del sector
- Muestra consideración de diferentes perspectivas y matices contextuales
- Ocasionalmente, ofrece reflexiones basadas en experiencia profesional

ESTRUCTURA PROFESIONAL:
- Comienza con un planteamiento sólido que establezca relevancia y contexto
- Desarrolla ideas con progresión lógica, no de forma mecánica o predecible
- Conecta conceptos con transiciones naturales que mantengan coherencia
- Presenta información compleja en componentes accesibles sin simplificar en exceso
- Cierra con reflexiones valiosas o implicaciones prácticas, no con resúmenes genéricos
- Evita metareferencias al artículo mismo o su estructura

ASPECTOS TÉCNICOS:
- Usa el formato markdown para la estructura (# para títulos, ## para secciones)
- Limita las listas a cuando realmente aportan claridad; prefiere descripción narrativa
- Si usas listas, introdúcelas adecuadamente y contextualiza cada elemento
- Mantén la terminología consistente y precisa a lo largo del texto

Tu objetivo final es que el lector perciba el artículo como obra de un profesional experto con años de experiencia en el tema, que escribe con claridad, autoridad y un toque personal pero manteniendo formalidad profesional."""
        
        human_template = """Redacta un artículo profesional de blog sobre: {tema}

{instrucciones_longitud}

{instrucciones_estilo}

{urls_text}

INFORMACIÓN A INCLUIR:
Título: {title}

Puntos para la introducción:
{introduction_points}

Secciones principales:
{sections_info}

Puntos para la conclusión:
{conclusion_points}

{prompt_personalizado}

REQUISITOS FUNDAMENTALES:
1. Escribe como un experto profesional con voz propia y experiencia real
2. Mantén un equilibrio entre formalidad profesional y naturalidad humana
3. Evita estructuras artificiales o fórmulas predecibles
4. Incorpora perspectivas basadas en experiencia profesional cuando sea apropiado
5. Utiliza el formato markdown para encabezados y estructura

OBJETIVO: Crear un artículo profesional que demuestre autoridad y expertise, manteniendo una voz humana natural pero adecuadamente formal."""
        
        return {
            "system_message": system_message,
            "human_template": human_template
        }
    
    def write_content(self, tema: str, outline: Dict[str, Any], longitud: str, estilos: List[str], 
                     urls: Optional[List[str]] = None, prompt_personalizado: Optional[str] = None) -> str:
        """Escribe el contenido del artículo.
        
        Args:
            tema: Tema del artículo
            outline: Estructura del artículo
            longitud: Longitud deseada ('short', 'medium', 'long')
            estilos: Lista de estilos ('informativo', 'persuasivo', 'narrativo', 'técnico')
            urls: Lista de URLs de referencia
            prompt_personalizado: Instrucciones adicionales
            
        Returns:
            Contenido del artículo
        """
        # Preparar el outline de forma más organizada
        title = outline['title']
        introduction_points = outline['introduction']
        
        # Preparar secciones
        sections_info = ""
        for section in outline['sections']:
            sections_info += f"- {section['heading']}\n"
            
            # Añadir subheadings si existen
            if 'subheadings' in section and section['subheadings']:
                sections_info += "  Aspectos a cubrir:\n"
                for point in section['subheadings']:
                    sections_info += f"  • {point}\n"
            
            # Añadir key_points si existen
            if 'key_points' in section and section['key_points']:
                if 'subheadings' not in section or not section['subheadings']:
                    sections_info += "  Aspectos a cubrir:\n"
                for point in section['key_points']:
                    sections_info += f"  • {point}\n"
        
        conclusion_points = outline['conclusion']
        
        # Adaptar según la longitud solicitada
        instrucciones_longitud = {
            "short": "Elabora un artículo conciso pero completo (aproximadamente 500 palabras) que presente los puntos esenciales con precisión y claridad.",
            "medium": "Desarrolla un artículo de profundidad adecuada (aproximadamente 1000 palabras) que aborde el tema con el nivel de detalle necesario.",
            "long": "Crea un artículo exhaustivo (aproximadamente 2000 palabras) que explore el tema en profundidad con análisis detallado y ejemplos elaborados."
        }
        
        # Adaptar según los estilos solicitados
        instrucciones_estilo = "Adapta el contenido a estos estilos, manteniendo siempre un equilibrio entre naturalidad y profesionalismo:\n"
        if "informativo" in estilos:
            instrucciones_estilo += "• Informativo: Presenta información valiosa con precisión y rigor, incorporando datos relevantes y contexto adecuado. Mantén un enfoque objetivo pero no árido.\n"
        if "persuasivo" in estilos:
            instrucciones_estilo += "• Persuasivo: Construye argumentos sólidos basados en evidencia y razonamiento lógico. Anticipa objeciones y presenta beneficios con respaldo adecuado, evitando lenguaje exagerado.\n"
        if "narrativo" in estilos:
            instrucciones_estilo += "• Narrativo: Incorpora ejemplos profesionales y estudios de caso estructurados para ilustrar conceptos clave. Utiliza narrativa profesional para establecer contexto y relevancia.\n"
        if "técnico" in estilos:
            instrucciones_estilo += "• Técnico: Explica conceptos complejos con precisión y claridad, equilibrando terminología especializada con explicaciones accesibles. Proporciona el nivel adecuado de detalle técnico sin abrumar.\n"
        
        # Preparar información de URLs
        urls_text = ""
        if urls and len(urls) > 0:
            urls_text = "Incorpora referencias a estos recursos de manera natural cuando sea pertinente:\n"
            for url in urls:
                urls_text += f"- {url}\n"
        
        # Generar el contenido
        response = self.generate_content(
            tema=tema,
            title=title,
            introduction_points=introduction_points,
            sections_info=sections_info,
            conclusion_points=conclusion_points,
            instrucciones_longitud=instrucciones_longitud.get(longitud, instrucciones_longitud["medium"]),
            instrucciones_estilo=instrucciones_estilo,
            urls_text=urls_text,
            prompt_personalizado=prompt_personalizado if prompt_personalizado else "Sin instrucciones adicionales."
        )
        
        return response["content"]
    
    def _format_response(self, raw_content: str) -> Dict[str, Any]:
        """Formatea la respuesta."""
        return {"content": raw_content}