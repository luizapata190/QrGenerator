from fastapi.testclient import TestClient
from app.main import app
from app.services import qr_service
import io

client = TestClient(app)

def test_generate_qr_image_service():
    data = "test"
    result = qr_service.generate_qr_image(data)
    assert isinstance(result, io.BytesIO)
    result.seek(0)
    assert result.read(8) == b'\x89PNG\r\n\x1a\n' # PNG signature

def test_generate_qr_base64_service():
    data = "test"
    result = qr_service.generate_qr_base64(data)
    assert isinstance(result, str)
    assert len(result) > 0

def test_endpoint_generate_qr():
    response = client.get("/GenerateQr/?data=test")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_endpoint_generate_qr_base64():
    response = client.get("/GenerateQrBase64/?data=test")
    assert response.status_code == 200
    json_resp = response.json()
    assert "qr_base64" in json_resp
    assert json_resp["data_original"] == "test"

def test_endpoint_download_qr():
    response = client.get("/DownloadQr/?data=test&filename=test.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert 'attachment; filename="test.png"' in response.headers["content-disposition"]
