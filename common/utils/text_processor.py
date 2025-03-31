import re
from typing import Dict, List, Tuple, Optional

class TextProcessor:
    """Utilidades para procesamiento de texto en la generación de contenido."""
    
    @staticmethod
    def split_into_sections(text: str, separator: str = '\n\n') -> List[str]:
        """Divide un texto en secciones basadas en un separador."""
        return text.split(separator)
    
    @staticmethod
    def extract_content_sections(text: str) -> Dict[str, str]:
        """Extrae las secciones de contenido (hook, contexto, cuerpo, CTA)."""
        sections = text.split('\n\n')
        hook = sections[0] if len(sections) > 0 else ""
        context = sections[1] if len(sections) > 1 else ""
        body = '\n\n'.join(sections[2:-1]) if len(sections) > 3 else sections[2] if len(sections) > 2 else ""
        cta = sections[-1] if len(sections) > 2 else ""
        
        return {
            "hook": hook,
            "context": context,
            "body": body,
            "cta": cta,
            "content": text
        }
    
    @staticmethod
    def extract_bullet_points(text: str) -> List[str]:
        """Extrae puntos de una lista con viñetas."""
        bullet_pattern = r'(?:^|\n)(?:[-•*]|\d+[.)])\s+(.*?)(?=(?:\n(?:[-•*]|\d+[.)])|$))'
        matches = re.findall(bullet_pattern, text, re.DOTALL)
        return [match.strip() for match in matches]
    
    @staticmethod
    def add_emojis(text: str, emoji_map: Dict[str, str]) -> str:
        """Añade emojis a un texto basado en palabras clave."""
        result = text
        for keyword, emoji in emoji_map.items():
            if keyword in result.lower():
                pattern = fr'(?<!\S)({re.escape(keyword)})(?!\S)'
                replacement = f'{emoji} \\1'
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result
    
    @staticmethod
    def optimize_for_social_media(text: str, platform: str = "linkedin") -> str:
        """Optimiza el texto para plataformas de redes sociales."""
        # Asegurar espaciado adecuado entre párrafos
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Optimizaciones específicas por plataforma
        if platform.lower() == "linkedin":
            # Limitar longitud (LinkedIn tiene un límite de ~3000 caracteres)
            if len(text) > 2800:
                sections = TextProcessor.split_into_sections(text)
                # Acortar el cuerpo manteniendo hook, contexto y CTA
                if len(sections) > 3:
                    body_sections = sections[2:-1]
                    while len('\n\n'.join([sections[0], sections[1], '\n\n'.join(body_sections), sections[-1]])) > 2800 and body_sections:
                        body_sections.pop()
                    
                    text = '\n\n'.join([sections[0], sections[1], '\n\n'.join(body_sections), sections[-1]])
            
            # Asegurar que hay hashtags relevantes al final
            if not re.search(r'#\w+', text):
                text += "\n\n#contenido #linkedin #profesional"
        
        elif platform.lower() == "blog":
            # Para blogs, asegurar que los párrafos no sean demasiado largos
            paragraphs = text.split('\n\n')
            for i, paragraph in enumerate(paragraphs):
                if len(paragraph) > 500 and '\n' not in paragraph:
                    # Dividir párrafos muy largos
                    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                    mid = len(sentences) // 2
                    paragraphs[i] = '. '.join(sentences[:mid]) + '.\n\n' + '. '.join(sentences[mid:])
            
            text = '\n\n'.join(paragraphs)