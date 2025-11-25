import sys
import os

# Agregar directorio actual al path
sys.path.append(os.getcwd())

print("Starting debug...")
try:
    print("Importing settings...")
    from app.core.config import settings
    print(f"Settings loaded successfully.")
    print(f"API_KEY prefix: {settings.API_KEY[:5]}...")
except Exception as e:
    print(f"Error loading settings: {e}")
print("Done.")
