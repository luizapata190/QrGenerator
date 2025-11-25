from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Define el header donde se espera el API Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Valida el API Key del header X-API-Key
    """
    if api_key is None:
        logger.warning("API Key missing in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key requerida. Incluir header: X-API-Key"
        )
    
    if api_key != settings.API_KEY:
        # Loguear solo los primeros caracteres por seguridad
        masked_key = (api_key[:4] + "...") if api_key else "None"
        logger.warning(f"Invalid API Key attempt", extra={"provided_key_prefix": masked_key})
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida"
        )
    
    logger.debug("API Key validated successfully")
    return api_key
