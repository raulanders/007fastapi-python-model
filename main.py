from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field #librería de validación de datos y gestión de esquemas
import joblib
from langdetect import detect_langs, LangDetectException
import re
from collections import Counter

pipeline_es = joblib.load("models/sentiment_pipeline_es.joblib")
pipeline_pt = joblib.load("models/sentiment_pipeline_pt.joblib")

# FastAPI usa esto para: -validar el request-generar Swagger-evitar errores
class TextInput(BaseModel):
    # text: str
    text: str = Field(...,min_length=1, description="Texto a analizar")

class Prevision(str, Enum):
    POSITIVO = "POSITIVO"
    NEGATIVO = "NEGATIVO"
    NEUTRO = "NEUTRO"

class PredictResponse(BaseModel):
    prevision: Prevision
    probabilidad: float = Field(..., ge=0.0, le=1.0)


#Crea la aplicación web
app = FastAPI(
    title="Sentiment DS API",
    version="1.0.0",
    description="Microservicio DS (mock) para análisis de sentimiento. Contrato estable para BE."
)                                 




@app.get("/")                                   #Define un endpoint GET
def root():                                     #Función que se ejecuta
    return {"message": "API funcionando"}       #Respuesta JSON

@app.get("/health")
def health():
    return {"status": "OK"}

#Crear el endpoint POST /predict + modifica tu endpoint /predict + simula el comportamiento de un modelo ML
@app.post("/predict", response_model=PredictResponse)
def predict(data: TextInput):
    prevision, score = analyze_sentiment(data.text)
    return {"prevision": prevision, "probabilidad": score}

# Validaciones de texto: filtrar ruido antes de llegar al modelo
def contiene_url(text: str) -> bool:
    return bool(re.search(r"(https?://|www\.)\S+", text, re.IGNORECASE))

def solo_simbolos(text: str) -> bool:
    return bool(re.fullmatch(r"[^\w\s]+", text))

def solo_risas(text: str) -> bool:
    # Risas comunes en español y portugués
    text = text.lower().strip()
    return bool(re.fullmatch(r"(ja|ha|je|jo|ju|kk|rs)+", text))

def muy_repetitivo(text: str, threshold: float = 0.7) -> bool:
    # Detecta textos del tipo: "bueno bueno bueno bueno"
    words = text.lower().split()
    if len(words) < 4:
        return False
    most_common_count = Counter(words).most_common(1)[0][1]
    return (most_common_count / len(words)) >= threshold

def validar_texto_input(text: str):
    # Lanza errores claros antes de cualquier inferencia
    if contiene_url(text):
        raise HTTPException(
            status_code=400,
            detail="El texto no debe contener URLs"
        )

    if solo_simbolos(text):
        raise HTTPException(
            status_code=400,
            detail="El texto contiene solo símbolos"
        )

    if solo_risas(text):
        raise HTTPException(
            status_code=400,
            detail="El texto contiene solo risas"
        )

    if muy_repetitivo(text):
        raise HTTPException(
            status_code=400,
            detail="El texto es excesivamente repetitivo"
        )

# NÚCLEO DE DECISIÓN
# - validación
# - detección de idioma
# - selección de modelo
# - predicción
# - normalización de salida
# Validaciones de texto: filtrar ruido antes de llegar al modelo
def contiene_url(text: str) -> bool:
    return bool(re.search(r"(https?://|www\.)\S+", text, re.IGNORECASE))

def solo_simbolos(text: str) -> bool:
    return bool(re.fullmatch(r"[^\w\s]+", text))

def solo_risas(text: str) -> bool:
    # Risas comunes en español y portugués
    text = text.lower().strip()
    return bool(re.fullmatch(r"(ja|ha|je|jo|ju|kk|rs)+", text))

def muy_repetitivo(text: str, threshold: float = 0.7) -> bool:
    # Detecta textos del tipo: "bueno bueno bueno bueno"
    words = text.lower().split()
    if len(words) < 4:
        return False
    most_common_count = Counter(words).most_common(1)[0][1]
    return (most_common_count / len(words)) >= threshold

def validar_texto_input(text: str):
    # Lanza errores claros antes de cualquier inferencia
    if contiene_url(text):
        raise HTTPException(
            status_code=400,
            detail="El texto no debe contener URLs"
        )

    if solo_simbolos(text):
        raise HTTPException(
            status_code=400,
            detail="El texto contiene solo símbolos"
        )

    if solo_risas(text):
        raise HTTPException(
            status_code=400,
            detail="El texto contiene solo risas"
        )

    if muy_repetitivo(text):
        raise HTTPException(
            status_code=400,
            detail="El texto es excesivamente repetitivo"
        )

# NÚCLEO DE DECISIÓN

def analyze_sentiment(text: str):
    # Validaciones de calidad del texto
    validar_texto_input(text)

    # Detección de idioma con probabilidad
    try:
        langs = detect_langs(text)
    except LangDetectException:
        raise HTTPException(
            status_code=400,
            detail="No se pudo detectar el idioma del texto"
        )

    language = langs[0].lang
    confidence_lang = langs[0].prob

    # Umbral mínimo de confianza para evitar falsos positivos
    if confidence_lang < 0.80:
        raise HTTPException(
            status_code=400,
            detail="No se pudo determinar el idioma con suficiente confianza"
        )

    # Selección explícita del modelo
    if language == "es":
        pipeline = pipeline_es
    elif language == "pt":
        pipeline = pipeline_pt
    else:
        raise HTTPException(
            status_code=400,
            detail="Idioma no soportado. Solo se admite español (es) y portugués (pt)."
        )

    # Inferencia
    prediction = pipeline.predict([text])[0]
    probabilities = pipeline.predict_proba([text])[0]
    confidence = float(max(probabilities))

    # Normalización al contrato de la API
    prediction = prediction.upper()

    if prediction == "POSITIVO":
        return Prevision.POSITIVO, confidence
    elif prediction == "NEGATIVO":
        return Prevision.NEGATIVO, confidence
    else:
        return Prevision.NEUTRO, confidence
