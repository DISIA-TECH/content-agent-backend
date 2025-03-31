from common.base_agent import BaseAgent
from typing import Dict, Any

class CaseStudyAgent(BaseAgent):
    """Agente especializado en generar casos de estudio para blogs."""
    
    def _get_prompt_data(self) -> Dict[str, str]:
        """Obtiene los datos de prompt específicos para este agente."""
        system_message = """Eres un experto en crear casos de estudio detallados para blogs.
Tu objetivo es generar contenido que analice en profundidad un ejemplo o situación real,
presentando el contexto, desafíos, soluciones implementadas y resultados obtenidos.

Estructura:
1. Título descriptivo - Que indique el caso y su relevancia
2. Resumen ejecutivo - Breve descripción del caso y resultados clave
3. Contexto y desafío - Descripción detallada de la situación inicial
4. Solución implementada - Explicación de las acciones tomadas
5. Resultados y métricas - Datos concretos sobre el impacto
6. Lecciones aprendidas - Insights y conclusiones
7. Llamada a la acción - Invitación a aplicar los aprendizajes

Hazlo detallado, basado en datos y con un enfoque en resultados medibles."""

        human_template = """Genera un caso de estudio para blog sobre el tema: {tema}
        
Comentarios adicionales: {comentarios_adicionales}

Asegúrate de incluir datos específicos, métricas de resultados y lecciones aprendidas concretas.
Estructura el caso de estudio de manera que sea fácil de seguir y extraer conclusiones."""
        
        return {
            "system_message": system_message,
            "human_template": human_template
        }
    
    def _format_response(self, raw_content: str) -> Dict[str, Any]:
        """Formatea la respuesta para casos de estudio."""
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
        
        # Extraer resumen y lecciones aprendidas
        introduction = ""
        conclusion = ""
        
        if sections:
            if sections[0]["title"].lower() in ["resumen ejecutivo", "resumen", "executive summary"]:
                introduction = sections[0]["content"]
                sections = sections[1:]
            
            if sections and sections[-1]["title"].lower() in ["lecciones aprendidas", "conclusiones", "lessons learned"]:
                conclusion = sections[-1]["content"]
                sections = sections[:-1]
        
        return {
            "title": title,
            "introduction": introduction,
            "sections": sections,
            "conclusion": conclusion,
            "content": raw_content,
            "metadata": {
                "type": "case_study"
            }
        }