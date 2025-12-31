from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field#librería de validación de datos y gestión de esquemas

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

#simula el comportamiento de un modelo ML
#Esta función:-no sabe nada de FastAPI-podría vivir en otro archivo-simula el comportamiento de un modelo ML
def analyze_sentiment(text: str):
    positive_words = ["bueno", "excelente", "feliz", "genial"]
    negative_words = ["malo", "terrible", "horrible", "triste"]

    text_lower = text.lower()

    for word in positive_words:
        if word in text_lower:
            return Prevision.POSITIVO, 0.9

    for word in negative_words:
        if word in text_lower:
            return Prevision.NEGATIVO, 0.9

    return Prevision.NEUTRO, 0.5
