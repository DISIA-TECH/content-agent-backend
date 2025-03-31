from common.base_agent import BaseAgent
from typing import Dict, Any

class EducationalAgent(BaseAgent):
    """Agente especializado en generar contenido educativo para blogs."""
    
    def _get_prompt_data(self) -> Dict[str, str]:
        """Obtiene los datos de prompt específicos para este agente."""
        system_message = """Eres un experto en crear contenido educativo para blogs.
Tu objetivo es generar contenido que explique conceptos complejos de manera clara y accesible,
proporcionando información valiosa y educativa para los lectores.

Estructura:
1. Título atractivo - Que capte la atención y describa el contenido
2. Introducción - Presenta el tema y por qué es importante
3. Secciones principales - Divididas con subtítulos claros
4. Conclusión - Resume los puntos clave y proporciona siguientes pasos
5. Llamada a la acción - Invita a los lectores a comentar o compartir

Hazlo educativo, informativo y basado en datos, pero manteniendo un tono conversacional y accesible."""

        human_template = """Genera contenido educativo de blog sobre el tema: {tema}
        
Comentarios adicionales: {comentarios_adicionales}

Asegúrate de incluir ejemplos prácticos, datos relevantes y explicaciones claras.
Divide el contenido en secciones con subtítulos descriptivos."""
        
        return {
            "system_message": system_message,
            "human_template": human_template
        }
    
    def _format_response(self, raw_content: str) -> Dict[str, Any]:
        """Formatea la respuesta para contenido de blog educativo."""
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
            introduction = sections[0]["content"] if sections[0]["title"].lower() in ["introducción", "introduccion", "introduction"] else ""
            if introduction and len(sections) > 1:
                sections = sections[1:]
            
            if sections and sections[-1]["title"].lower() in ["conclusión", "conclusion"]:
                conclusion = sections[-1]["content"]
                sections = sections[:-1]
        
        return {
            "title": title,
            "introduction": introduction,
            "sections": sections,
            "conclusion": conclusion,
            "content": raw_content
        }