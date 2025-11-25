# Guía de Seguridad - Gestión de Credenciales

##  Problema de Seguridad

**NUNCA** subas credenciales reales a GitHub. Esto incluye:
- Contraseñas de bases de datos
- Claves API
- Tokens de acceso
- Emails y usuarios administrativos

##  Solución Implementada

### 1. Archivo .env (Local, NO se sube a Git)

Este archivo contiene tus credenciales **reales** y está bloqueado por .gitignore.

### 2. Archivo .env.example (Plantilla, SÍ se sube a Git)

Este archivo es una **plantilla** con valores de ejemplo que SÍ puedes subir a GitHub.

### 3. docker-compose.yml (Usa variables, SÍ se sube a Git)

Ahora usa variables de entorno en lugar de valores hardcodeados.

##  Checklist Antes de Subir a GitHub

- [ ] Verificar que .env está en .gitignore
- [ ] Crear .env.example con valores de ejemplo (NO reales)
- [ ] Actualizar docker-compose.yml para usar variables
- [ ] Ejecutar git status y confirmar que .env NO aparece

##  Mejores Prácticas

### Para Desarrollo Local:
1. Copia .env.example a .env
2. Edita .env con tus credenciales reales
3. **Nunca** hagas git add .env

### Para Producción:
1. Usa **variables de entorno del servidor** (no archivos .env)
2. Usa servicios de gestión de secretos (AWS Secrets Manager, Azure Key Vault, etc.)
3. Rota contraseñas regularmente
