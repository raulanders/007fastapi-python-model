from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field#librería de validación de datos y gestión de esquemas
import joblib

pipeline = joblib.load("models/sentiment_pipeline.joblib") #Cargar el pepeline real

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

# Reemplazo correcto de analyze_sentiment
def analyze_sentiment(text: str):
    # Predicción del modelo
    prediction = pipeline.predict([text])[0]              #Use pipeline.predict
    probabilities = pipeline.predict_proba([text])[0]     #Use pipeline.predict_proba
    confidence = float(max(probabilities))

    # Normalizar salida al Enum
    prediction = prediction.upper()

    if prediction == "POSITIVO":
        return Prevision.POSITIVO, confidence
    elif prediction == "NEGATIVO":
        return Prevision.NEGATIVO, confidence
    else:
        return Prevision.NEUTRO, confidence
