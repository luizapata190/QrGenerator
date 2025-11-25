import qrcode
import io
import base64
import logging
from typing import Dict

# Configurar logger
logger = logging.getLogger(__name__)

def generate_qr_image(data: str) -> io.BytesIO:
    """
    Genera una imagen QR en memoria a partir de un string.
    Devuelve un buffer (io.BytesIO) con la imagen en formato PNG.
    """
    try:
        img_buffer = io.BytesIO()
        img = qrcode.make(data)
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        return img_buffer
    except Exception as e:
        logger.error(f"Error al generar QR para data='{data}': {e}")
        raise e

def generate_qr_base64(data: str) -> str:
    """
    Genera un QR y devuelve el string en Base64.
    """
    try:
        image_buffer = generate_qr_image(data)
        image_bytes = image_buffer.getvalue()
        base64_bytes = base64.b64encode(image_bytes)
        base64_string = base64_bytes.decode('utf-8')
        return base64_string
    except Exception as e:
        logger.error(f"Error al generar QR Base64 para data='{data}': {e}")
        raise e