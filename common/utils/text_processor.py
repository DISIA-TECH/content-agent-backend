import re
from typing import Dict, List, Optional, Any

class TextProcessor:
    """Utilidades para procesamiento de texto en la generación de contenido."""
    
    @staticmethod
    def extract_sections(content: str) -> Dict[str, str]:
        """Extrae secciones de un artículo en formato markdown."""
        # Extraer título
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""
        
        # Extraer secciones
        sections_pattern = r'^## (.+?)\n(.*?)(?=^## |\Z)'
        sections_matches = re.finditer(sections_pattern, content, re.MULTILINE | re.DOTALL)
        
        sections = {}
        for match in sections_matches:
            section_title = match.group(1).strip()
            section_content = match.group(2).strip()
            sections[section_title.lower()] = section_content
        
        # Extraer introducción (texto antes de la primera sección)
        intro_pattern = r'^# .+?\n\n(.*?)(?=^## |\Z)'
        intro_match = re.search(intro_pattern, content, re.MULTILINE | re.DOTALL)
        introduction = intro_match.group(1).strip() if intro_match else ""
        
        return {
            "title": title,
            "introduction": introduction,
            "sections": sections,
            "content": content
        }
    
    @staticmethod
    def extract_summary(content: str, max_length: int = 250) -> str:
        """Extrae un resumen breve del artículo."""
        # Intentar encontrar la introducción
        intro_section = None
        sections = TextProcessor.extract_sections(content)
        
        # Buscar sección de introducción
        for key, value in sections["sections"].items():
            if "introduc" in key.lower():
                intro_section = value
                break
        
        # Si no hay introducción, usar el primer párrafo después del título
        if not intro_section and sections["introduction"]:
            intro_section = sections["introduction"]
        
        # Si aún no tenemos resumen, usar las primeras líneas del contenido
        if not intro_section:
            content_without_title = re.sub(r'^# .+?\n\n', '', content, flags=re.MULTILINE)
            paragraphs = content_without_title.split('\n\n')
            if paragraphs:
                intro_section = paragraphs[0]
        
        # Si tenemos un resumen, acortarlo si es necesario
        if intro_section:
            if len(intro_section) > max_length:
                intro_section = intro_section[:max_length].rsplit(' ', 1)[0] + "..."
            return intro_section.strip()
        
        return "Resumen no disponible."