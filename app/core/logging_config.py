import logging
import sys
import json
from app.core.config import settings

class JsonFormatter(logging.Formatter):
    def format(self, record):
        json_log = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        # Atributos estándar de LogRecord que queremos excluir de 'extra'
        standard_attrs = {
            'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
            'funcName', 'levelname', 'levelno', 'lineno', 'module',
            'msecs', 'message', 'msg', 'name', 'pathname', 'process',
            'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName'
        }
        
        # Agregar campos extra que no sean estándar
        for key, value in record.__dict__.items():
            if key not in standard_attrs and not key.startswith('_'):
                json_log[key] = value
                
        return json.dumps(json_log)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)
    
    # Limpiar handlers existentes
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    
    if settings.LOG_FORMAT.lower() == "json":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Ajustar logs de librerías ruidosas si es necesario
    logging.getLogger("uvicorn.access").handlers = []
    
    return logger
