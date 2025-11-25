from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Dict
from app.services import qr_service

router = APIRouter()

@router.get("/GenerateQr/", summary="Genera una imagen QR", response_class=StreamingResponse)
async def generate_qr_get(data: str = Query("https://google.com", description="Texto o URL para el QR")):
    """
    Genera un código QR basado en el parámetro 'data' y lo devuelve como una imagen PNG.
    """
    try:
        img_buffer = qr_service.generate_qr_image(data)
        return StreamingResponse(img_buffer, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando QR: {str(e)}")

@router.get("/GenerateQrBase64/", summary="Genera un QR (Devuelve JSON con Base64)", response_model=Dict[str, str])
async def generate_qr_get_base64(data: str = Query("https://google.com", description="Texto o URL para el QR")):
    """
    Genera un código QR y lo devuelve como un JSON que contiene el string Base64 de la imagen.
    """
    try:
        base64_string = qr_service.generate_qr_base64(data)
        return {
            "data_original": data,
            "qr_base64": base64_string,
            "media_type": "image/png"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando QR Base64: {str(e)}")

@router.get("/DownloadQr/", summary="Descarga una imagen QR (PNG)", response_class=StreamingResponse)
async def download_qr_get(
    data: str = Query("https://google.com", description="Texto o URL para el QR"),
    filename: str = Query("codigo_qr.png", description="Nombre del archivo a descargar")
):
    """
    Genera un código QR y fuerza al navegador a DESCARGARLO como un archivo PNG.
    """
    try:
        img_buffer = qr_service.generate_qr_image(data)
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        return StreamingResponse(img_buffer, media_type="image/png", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error descargando QR: {str(e)}")
