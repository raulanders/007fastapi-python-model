from fastapi import FastAPI
from pydantic import BaseModel #librería de validación de datos y gestión de esquemas

# FastAPI usa esto para: -validar el request-generar Swagger-evitar errores
class TextInput(BaseModel):
    text: str

app = FastAPI()                                 #Crea la aplicación web

@app.get("/")                                   #Define un endpoint GET
def root():                                     #Función que se ejecuta
    return {"message": "API funcionando"}       #Respuesta JSON

#Crear el endpoint POST /predict
'''
@app.post("/predict")                   #Define un endpoint POST
def predict(data: TextInput):           #FastAPI convierte el JSON en un objeto
    return {
        "received_text": data.text      #Accedes al valor enviado
    }                                   #Respuesta JSON
'''
#Crear el endpoint POST /predict + modifica tu endpoint /predict + simula el comportamiento de un modelo ML
@app.post("/predict")
def predict(data: TextInput):
    sentiment, score = analyze_sentiment(data.text)

    return {
        "prevision": sentiment,
        "probabilidad": score,
        #"text": data.text
    }

#simula el comportamiento de un modelo ML
#Esta función:-no sabe nada de FastAPI-podría vivir en otro archivo-simula el comportamiento de un modelo ML
def analyze_sentiment(text: str):
    positive_words = ["bueno", "excelente", "feliz", "genial"]
    negative_words = ["malo", "terrible", "horrible", "triste"]

    text_lower = text.lower()

    for word in positive_words:
        if word in text_lower:
            return "positivo", 0.9

    for word in negative_words:
        if word in text_lower:
            return "negativo", 0.9

    return "neutro", 0.5
