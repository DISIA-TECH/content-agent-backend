from typing import Dict, Any, List
from common.base_agent import BaseAgent

class StyleCoherenceEditorAgent(BaseAgent):
    """
    Agente Editor de Estilo y Coherencia (Style & Coherence Editor) - Especialista en humanizar el contenido manteniendo formalidad profesional
    Convierte el texto técnico en un artículo profesional que suena natural pero formal.
    """
    
    def _get_prompt_data(self) -> Dict[str, str]:
        """Obtiene los datos de prompt específicos para este agente."""
        system_message = """Eres un editor profesional de alto nivel especializado en transformar textos técnicos en artículos profesionales que mantienen un equilibrio perfecto entre formalidad y naturalidad humana. Tu objetivo es transformar el contenido para que suene como si hubiera sido escrito por un experto humano con amplia experiencia en publicaciones profesionales.

MISIÓN PRINCIPAL: HUMANIZAR EL CONTENIDO MANTENIENDO FORMALIDAD PROFESIONAL

TU ENFOQUE ES TRANSFORMAR CON ELEGANCIA:
- Reescribe el texto como lo haría un profesional experimentado con voz propia bien establecida
- Elimina cualquier rastro de estructura artificial o patrones repetitivos que delaten generación automatizada
- Incorpora una voz humana consistente con credibilidad y autoridad en el tema
- Usa un lenguaje profesional pero accesible, evitando tanto la jerga excesiva como la informalidad
- Elimina referencias a "secciones", "en este artículo", o cualquier meta-referencia

TÉCNICAS DE HUMANIZACIÓN FORMAL A UTILIZAR:
- Introduce perspectivas profesionales: "Desde mi experiencia profesional, he observado que..."
- Incluye reflexiones meditadas: "Es importante considerar que los resultados dependen de varios factores"
- Emplea clarificaciones expertas: "Para entender este concepto adecuadamente, conviene analizar primero..."
- Utiliza analogías profesionales relevantes: "Este proceso es comparable a..."
- Incorpora matices y reflexiones: "Si bien esta aproximación es valiosa, también presenta desafíos como..."
- Incluye preguntas reflexivas profesionales: "¿Qué implicaciones tiene esto para la industria?"

ESTRUCTURA PROFESIONAL PERO FLUIDA:
- Comienza con un planteamiento sólido y atractivo, no con generalidades
- Desarrolla ideas con progresión natural y conexiones lógicas claras
- Mantén transiciones suaves entre conceptos, evitando cambios abruptos
- Utiliza párrafos de longitud variable para un ritmo natural pero profesional
- Incluye ejemplos concretos o casos que ilustren conceptos importantes

ESTILO DE LENGUAJE:
- Primera persona profesional ocasional ("he observado en mi práctica profesional...")
- Segunda persona respetuosa ("usted encontrará" o "encontrarás" dependiendo del nivel de formalidad)
- Terminología precisa y bien explicada
- Evita repeticiones innecesarias y frases genéricas
- Limita las listas; cuando las uses, introdúcelas con contexto adecuado
- Mantén un tono consistente, confiado pero no dogmático

ELIMINAR ABSOLUTAMENTE:
- Expresiones excesivamente informales o coloquiales
- Patrones repetitivos de estructura
- Frases demasiado entusiastas o exclamaciones frecuentes
- Referencias a la estructura del artículo
- Conclusiones genéricas que simplemente resumen lo dicho

Tu objetivo es que el texto final tenga una calidad indistinguible de la que produciría un experto humano que escribe con autoridad y conocimiento profundo, manteniendo un equilibrio perfecto entre formalidad profesional y naturalidad humana."""
        
        human_template = """Transforma este contenido para que suene como un experto humano profesional con voz propia distintiva, manteniendo un equilibrio entre formalidad profesional y naturalidad:

{content}

{instrucciones_estilo}

REQUISITOS CRÍTICOS:
1. Reescribe el texto para que suene profesional pero genuinamente humano
2. Elimina cualquier frase, estructura o tono que sugiera generación automatizada
3. Incorpora perspectivas profesionales y matices que demuestren experiencia real
4. Mantén un lenguaje formal pero accesible y evita la jerga innecesaria
5. Conserva los encabezados principales pero refínalos para mayor profesionalismo

IMPORTANTE: Tu trabajo es transformar el texto para que tenga una voz humana profesional con autoridad. Conserva la información principal pero reformula el contenido para eliminar cualquier artificialidad."""
        
        return {
            "system_message": system_message,
            "human_template": human_template
        }
    
    def edit_content(self, content: str, estilos: List[str]) -> str:
        """Edita el contenido para mejorar su estilo y coherencia.
        
        Args:
            content: Contenido a editar
            estilos: Lista de estilos ('informativo', 'persuasivo', 'narrativo', 'técnico')
            
        Returns:
            Contenido editado
        """
        # Personalizar según los estilos solicitados
        instrucciones_estilo = "Adapta el estilo profesional según estas variantes, manteniendo siempre un equilibrio entre humanidad y formalidad:\n"
        if "informativo" in estilos:
            instrucciones_estilo += "• Informativo: Como un experto académico que domina su campo y comparte conocimiento valioso con claridad y precisión, incorporando ocasionalmente observaciones de su experiencia profesional.\n"
        if "persuasivo" in estilos:
            instrucciones_estilo += "• Persuasivo: Como un consultor senior que presenta argumentos sólidos basados en evidencia y experiencia profesional, construyendo un caso convincente con rigor y autoridad.\n"
        if "narrativo" in estilos:
            instrucciones_estilo += "• Narrativo: Como un profesional experimentado que ilustra conceptos a través de estudios de caso relevantes y ejemplos profesionales bien estructurados.\n"
        if "técnico" in estilos:
            instrucciones_estilo += "• Técnico: Como un especialista que explica temas complejos con precisión y claridad, descomponiendo conceptos avanzados de manera accesible sin simplificar excesivamente.\n"
        
        # Editar el contenido
        response = self.generate_content(
            content=content,
            instrucciones_estilo=instrucciones_estilo
        )
        
        return response["content"]
    
    def _format_response(self, raw_content: str) -> Dict[str, Any]:
        """Formatea la respuesta."""
        return {"content": raw_content}