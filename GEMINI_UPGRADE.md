# 🚀 Guía de Actualización a Gemini 2.5 Flash

## 📋 Modelos de Gemini Disponibles

### Modelos Actuales (Todos con Capa Gratuita)

| Modelo | Estado | Velocidad | Calidad | Uso Recomendado |
|--------|--------|-----------|---------|-----------------|
| **gemini-1.5-flash** | ✅ Actual | Rápido | Alta | Producción (actual) |
| **gemini-2.0-flash-exp** | 🧪 Experimental | Muy rápido | Muy alta | Testing |
| **gemini-2.5-flash** | 🔜 Futuro | Ultra rápido | Ultra alta | Cuando esté disponible |

### Límites de la Capa Gratuita

- **Requests por minuto**: 15 RPM
- **Requests por día**: 1,500 RPD
- **Tokens por minuto**: 1 millón TPM
- **Tokens por día**: Sin límite diario

---

## 🔄 Cómo Cambiar de Modelo

### Opción 1: Cambiar en `.env` (Recomendado)

```bash
# Editar .env
nano .env

# Cambiar esta línea:
GEMINI_MODEL=gemini-1.5-flash

# Por una de estas opciones:
GEMINI_MODEL=gemini-2.0-flash-exp  # Experimental (disponible ahora)
GEMINI_MODEL=gemini-2.5-flash      # Futuro (cuando esté disponible)
```

### Opción 2: Cambiar en el Código

```python
# backend/app/core/config.py
class Settings(BaseSettings):
    GEMINI_MODEL: str = "gemini-2.5-flash"  # Cambiar aquí
```

### Opción 3: Variable de Entorno Temporal

```bash
# Solo para esta sesión
export GEMINI_MODEL=gemini-2.0-flash-exp

# Levantar servicios
./scripts/dev.sh
```

---

## ✅ Verificar que Funciona

### 1. Verificar Configuración

```bash
# Ver qué modelo está configurado
grep GEMINI_MODEL .env
```

### 2. Probar con curl

```bash
# Obtener tu API key
API_KEY=$(grep GEMINI_API_KEY .env | cut -d'=' -f2)

# Probar gemini-2.0-flash-exp
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Hola, ¿funcionas?"
      }]
    }]
  }'
```

### 3. Probar en la Aplicación

1. Levantar servicios: `./scripts/dev.sh`
2. Abrir frontend: http://localhost:8502
3. Pegar código de ejemplo
4. Click en "Analizar Código"
5. Verificar que funciona

---

## 🆕 Diferencias entre Modelos

### gemini-1.5-flash (Actual)
```
✅ Estable y confiable
✅ Bien documentado
✅ Ampliamente probado
⚡ Velocidad: ~2-3 segundos
💰 Gratis: 15 RPM
```

### gemini-2.0-flash-exp (Experimental)
```
🧪 Experimental (puede cambiar)
✅ Más rápido que 1.5
✅ Mejor calidad de respuestas
⚡ Velocidad: ~1-2 segundos
💰 Gratis: 15 RPM
⚠️  Puede tener cambios sin aviso
```

### gemini-2.5-flash (Futuro)
```
🔜 Aún no disponible
🚀 Se espera que sea el más rápido
🎯 Mejor calidad de análisis
⚡ Velocidad: ~0.5-1 segundo (estimado)
💰 Gratis: 15 RPM (estimado)
```

---

## 🔧 Configuración Actual del Proyecto

### URL de la API

```python
# backend/app/infrastructure/gemini_client.py
base_url = "https://generativelanguage.googleapis.com/v1beta"
```

### Formato de Request

```python
url = f"{base_url}/models/{model}:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{
            "text": prompt
        }]
    }],
    "generationConfig": {
        "temperature": 0.3,      # Más determinístico
        "maxOutputTokens": 2048, # Máximo de tokens
        "topP": 0.8,             # Nucleus sampling
        "topK": 10               # Top-K sampling
    }
}
```

---

## 📊 Comparación de Rendimiento

### Tiempo de Respuesta (Estimado)

```
Código pequeño (< 50 líneas):
- gemini-1.5-flash:     2-3 segundos
- gemini-2.0-flash-exp: 1-2 segundos
- gemini-2.5-flash:     0.5-1 segundo (estimado)

Código mediano (50-200 líneas):
- gemini-1.5-flash:     4-6 segundos
- gemini-2.0-flash-exp: 2-4 segundos
- gemini-2.5-flash:     1-2 segundos (estimado)

Código grande (200-500 líneas):
- gemini-1.5-flash:     8-12 segundos
- gemini-2.0-flash-exp: 4-8 segundos
- gemini-2.5-flash:     2-4 segundos (estimado)
```

---

## 🚨 Troubleshooting

### Error: "Model not found"

```bash
# Verificar que el modelo existe
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$API_KEY"

# Si gemini-2.5-flash no existe aún, usar:
GEMINI_MODEL=gemini-2.0-flash-exp
```

### Error: "Quota exceeded"

```bash
# Has excedido los 15 RPM
# Esperar 1 minuto o implementar rate limiting

# Ver uso actual en:
# https://aistudio.google.com/app/apikey
```

### Error: "Invalid API key"

```bash
# Verificar API key
grep GEMINI_API_KEY .env

# Obtener nueva API key en:
# https://aistudio.google.com/app/apikey
```

---

## 🎯 Recomendaciones

### Para Desarrollo
```bash
GEMINI_MODEL=gemini-2.0-flash-exp  # Más rápido para iterar
```

### Para Producción
```bash
GEMINI_MODEL=gemini-1.5-flash  # Más estable
```

### Para Testing
```bash
GEMINI_MODEL=gemini-2.0-flash-exp  # Probar nuevas features
```

### Cuando esté disponible
```bash
GEMINI_MODEL=gemini-2.5-flash  # Migrar cuando sea estable
```

---

## 📚 Referencias

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Gemini Models](https://ai.google.dev/gemini-api/docs/models/gemini)
- [API Pricing](https://ai.google.dev/pricing)
- [API Limits](https://ai.google.dev/gemini-api/docs/quota)

---

## ✅ Checklist de Migración

Cuando gemini-2.5-flash esté disponible:

- [ ] Verificar que el modelo existe en la API
- [ ] Probar con curl
- [ ] Actualizar `.env` con `GEMINI_MODEL=gemini-2.5-flash`
- [ ] Reiniciar servicios
- [ ] Probar análisis de código
- [ ] Verificar calidad de respuestas
- [ ] Monitorear rendimiento
- [ ] Actualizar documentación
- [ ] Commit cambios: `git commit -m "feat: migrar a gemini-2.5-flash"`

---

**Última actualización:** Enero 2025  
**Modelo actual:** gemini-1.5-flash  
**Próximo modelo:** gemini-2.5-flash (cuando esté disponible)
