import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any

# 1. Importa la función principal de tu módulo de servicios
from services.qr_service import get_qr_response, get_qr_base64, get_qr_download_response

#Documentacion FastApi
app = FastAPI(
    title="Qr Generator API",
    description="API para creacion de Codigos Qr",
    version="1.0.0"
)

#http://127.0.0.1:8000/GenerateQr/
#http://127.0.0.1:8000/GenerateQr/?data=https://www.linkedin.com/in/luis-zapata-92839287/
@app.get("/GenerateQr/",
         response_class=StreamingResponse,
         summary="Genera una imagen QR")
async def generate_qr_get(
    #Se setea un valor por defecto para facilitar pruebas
    data: str = "https://google.com"
):
    """
    Genera un código QR basado en el parámetro 'data'
    y lo devuelve como una imagen PNG.
    """
    return get_qr_response(data)


#http://127.0.0.1:8000/GenerateQrBase64/
#http://127.0.0.1:8000/GenerateQrBase64/?data=https://www.linkedin.com/in/luis-zapata-92839287/
@app.get("/GenerateQrBase64/",
         response_model=Dict[str, str],
         summary="Genera un QR (Devuelve JSON con Base64)")
async def generate_qr_get_base64(
    data: str = "https://google.com"
):
    """
    Genera un código QR y lo devuelve como un JSON
    que contiene el string Base64 de la imagen.
    """
    return get_qr_base64(data)


#http://127.0.0.1:8000/DownloadQr/
#http://127.0.0.1:8000/DownloadQr/?data=https://www.linkedin.com/in/luis-zapata-92839287/
@app.get("/DownloadQr/",
         response_class=StreamingResponse,
         summary="Descarga una imagen QR (PNG)")
async def download_qr_get(
    data: str = "https://google.com",
    filename: str = "codigo_qr.png"
):
    """
    Genera un código QR y fuerza al navegador a DESCARGARLO
    como un archivo PNG.
    """
    # Llama al servicio que ahora se encarga de TODO
    return get_qr_download_response(data, filename)


#Iniciar api con uvicorn
# poetry run uvicorn main:app --reload
# poetry run uvicorn main:app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)