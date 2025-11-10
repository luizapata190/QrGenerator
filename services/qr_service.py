# services/qr_service.py

import qrcode
import io
import base64
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict

def create_qr_image(data: str) -> io.BytesIO:
    """
    Función interna: Toma un string y genera la imagen QR en memoria.
    (Esta función no cambia)
    """
    try:
        #Crea un 'buffer' (un archivo temporal) en la memoria RAM a partir de la Url
        img_buffer = io.BytesIO()
        #Llama a la librería 'qrcode' para generar la imagen QR con los datos
        img = qrcode.make(data)
        #Guarda la imagen generada (que está en formato PIL/Pillow)
        #directamente en el buffer de memoria, especificando el formato 'PNG'.
        img.save(img_buffer, format="PNG")
        #Mueve el "puntero" del buffer al inicio (posición 0).
        #es necesario porque .save() dejó el puntero al *final* del archivo en memoria.
        #para que StreamingResponse pueda leerlo, debe empezar desde el principio.
        img_buffer.seek(0)
        #Devuelve el buffer de memoria (el archivo PNG en RAM) para que el
        #servicio lo pueda enviar como respuesta.
        return img_buffer
    except Exception as e:
        print(f"Error al generar QR: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar el QR: {str(e)}")


def get_qr_response(data: str) -> StreamingResponse:
    """
    Servicio para el endpoint GET: genera el QR y prepara la respuesta de imagen.
    (Esta función no cambia)
    """
    image_buffer = create_qr_image(data)
    return StreamingResponse(image_buffer, media_type="image/png")



def get_qr_base64(data: str) -> Dict[str, str]:
    """
    Servicio para el endpoint Base64: genera el QR y lo devuelve como un
    diccionario listo para ser convertido a JSON.
    """
    try:
        #Crea un 'buffer' (un archivo temporal) en la memoria RAM a partir de la Url
        image_buffer = create_qr_image(data)
        #Obtiene los bytes crudos de la imagen desde el buffer
        image_bytes = image_buffer.getvalue()
        #Codifica los bytes a Base64 (esto devuelve bytes)
        base64_bytes = base64.b64encode(image_bytes)
        #Decodifica los bytes de Base64 a un string UTF-8 (para JSON)
        base64_string = base64_bytes.decode('utf-8')
        #Devuelve un diccionario estándar
        return {
            "data_original": data,
            "qr_base64": base64_string,
            "media_type": "image/png"
        }

    except Exception as e:
        # Re-lanzar como HTTPException para que main.py lo maneje
        print(f"Error al codificar QR a Base64: {e}")
        raise HTTPException(status_code=500, detail=f"Error al codificar QR a Base64: {str(e)}")


def get_qr_download_response(data: str, filename: str) -> StreamingResponse:
    """
    Servicio para /DownloadQr/: Genera el QR,
    prepara las cabeceras (headers) y devuelve la respuesta StreamingResponse.
    """
    #Crea un 'buffer' (un archivo temporal) en la memoria RAM a partir de la Url
    image_buffer = create_qr_image(data)

    #Construir la cabecera 'Content-Disposition'
    #'attachment' le dice al navegador que descargue el archivo.
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    # 3. Devolver la respuesta completa desde el servicio
    return StreamingResponse(image_buffer, media_type="image/png", headers=headers)