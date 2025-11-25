import secrets
import string

def generate_api_key(length=32):
    """Genera una API Key segura y aleatoria."""
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for i in range(length))
    return api_key

if __name__ == "__main__":
    key = generate_api_key()
    print("\n" + "="*50)
    print("🔑 TU NUEVA API KEY GENERADA:")
    print("="*50)
    print(f"\n{key}\n")
    print("="*50)
    print("Instrucciones:")
    print("1. Copia esta clave.")
    print("2. Pégala en tu archivo .env: API_KEY=tu-clave-copiada")
    print("3. Úsala en el header 'X-API-Key' de tus peticiones.")
    print("="*50 + "\n")
