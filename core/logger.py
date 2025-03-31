import logging
import sys
from core.config import settings

# Configurar formato de logging
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Configurar nivel de logging
log_level = getattr(logging, settings.LOG_LEVEL.upper())

# Configurar handler para consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(log_format, date_format))

# Configurar logger raíz
root_logger = logging.getLogger()
root_logger.setLevel(log_level)
root_logger.addHandler(console_handler)

# Función para obtener logger configurado
def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger configurado con el nombre especificado.
    
    Args:
        name: Nombre del logger
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger