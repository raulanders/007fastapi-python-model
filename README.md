# 007-FastAPI-python-model
Implementación de FastAPI desde Python (Python BackEND)
# Crear FastAPI


## Flujo completo de un proyecto FastAPI con ML

1.  Crear y configurar el entorno (Conda)
2.  Activar el entorno
3.  Instalar dependencias
4.  Entender qué es FastAPI
5.  Crear una API mínima
6.  Ejecutar el servidor
7.  Probar el endpoint
8.  Agregar un modelo sencillo
9.  Exponer el modelo vía endpoint
10. Documentar para backend

### 1.  Crear el entorno virtual (CONCEPTO + PRÁCTICA)

#### ¿Qué es un entorno virtual?

Un entorno virtual es un espacio aislado donde:

- Instalamos librerías
- Definimos versión de Python (3.12 para nuestro caso, por la estabilidad)
- Evitamos conflictos con otros proyectos

Un proyecto = un entorno (FastAPI, ML, Python3.12 deben vivir juntos y aislados)

#### ¿Por qué usamos Conda?

- Maneja entornos
- Maneja versiones de Python
- Evita errores de dependencias (muy común en ML)
- No es obligatorio, pero es estándar en data / ML.

#### 1.1. Verificar que Conda funcione

Abrir PowerShell y ejecutar:
```
conda --version
```
Resultado:
```
conda 24.x.x
```
Qué significa esto
- Verifica que Conda esté instalado
- Verifica que esté en el PATH




#### 1.2. Crear el entorno y activar entorno

Ejecutar (PowerShell)
```
conda create -n projectfastapi python=3.12
```
- **conda create**    ->	crea un entorno
- **-n projectfastapi**	-> nombre del entorno
- **python=3.12**     ->	versión exacta de Python

Se pueden verificas los entornos con  

```
conda env list
```
o

```
conda info --envs
```
Para eliminar un entorno:

Desactivar el entorno
```
conda deactivate
```
Eliminar el entorno

```
conda env remove --name nombreDelEntorno
```

Para activar el entorno:
```
conda activate projectfastapi
```
El prompt cambiara a:
```
(projectfastapi) PS C:\...
```

### PASO 2. Instalar dependencias (CONCEPTO + PRÁCTICA)

Antes de ejecutar comandos, necesitas entender qué estás haciendo y por qué.

#### 2.1. ¿Qué son las dependencias?

Las dependencias son librerías externas que tu proyecto necesita para funcionar.

| Librería     | Para qué sirve              |
| ------------ | --------------------------- |
| fastapi      | Crear la API                |
| uvicorn      | Servidor que ejecuta la API |
| scikit-learn | Modelo de ML                |
| pandas       | Manejo de datos             |
| numpy        | Cálculo numérico            |


#### Instalar dependencias y verificar la instalación

Con el entorno activo (projectfastapi), ejecuta:

```
pip install fastapi uvicorn scikit-learn pandas numpy joblib
```
Qué hace este comando:
- Descarga librerías
- Las instala solo en este entorno
- No afecta otros proyectos

Ahora verificamos la instalación:
```
python -c "import fastapi, uvicorn, sklearn, pandas, numpy; print('OK')"
```
Respuesta:
OK

### PASO 3 — ¿Qué es FastAPI? + crear la API mínima

Este paso es conceptual y práctico a la vez.

Aquí entiendes qué es una API y cómo FastAPI la crea.

#### 3.1. ¿Qué es una API?

Una API es una interfaz para que otro sistema (por ejemplo backend Java) pueda:

- enviar datos
- recibir resultados
- sin conocer tu código interno

En nuestro caso: **Java envía texto → API procesa → devuelve sentimiento**

#### 3.2. ¿Qué es FastAPI?

FastAPI es un framework que:

- crea APIs REST
- valida datos automáticamente
- genera documentación (Swagger)
- es rápido y moderno

Idea clave: **FastAPI convierte funciones de Python en endpoints HTTP.**

#### 3.3. ¿Qué es un endpoint?

Un endpoint es:

- una ruta (/predict)
- con un método HTTP (POST)
- que ejecuta una función

Ejemplo mental:

```
POST /predict → ejecuta predict()
```



#### 3.4. Crear la estructura mínima del proyecto

Dentro de tu proyecto, crea una carpeta: `FastAPI/`

Dentro de esa carpeta crea un archivo: `main.py`

#### 3.5 Código mínimo de FastAPI

Abre `main.py` y escribe exactamente esto:


```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API funcionando"}
```
| Línea         | Explicación            |
| ------------- | ---------------------- |
| FastAPI()     | Crea la aplicación web |
| @app.get("/") | Define un endpoint GET |
| root()        | Función que se ejecuta |
| return {...}  | Respuesta JSON         |


app = FastAPI() crea la aplicación web.

Es el objeto central que:
- registra endpoints
- recibe requests HTTP
- devuelve responses HTTP
- conecta todo lo demás

Piensa en app como: “El servidor lógico de tu API”

Analogía

- FastAPI() → fábrica
- app → la API concreta que salió de esa fábrica

Sin ese objeto:

- no existen rutas
- no hay API
- Uvicorn no sabe qué ejecutar

Qué guarda internamente app:

- lista de endpoints (/, /predict, etc.)
- métodos permitidos (GET, POST)
- validaciones
- esquema OpenAPI (Swagger)

Por eso todo se escribe como:
```
@app.get("/")
@app.post("/predict")
```
Porque le estás diciendo a esa aplicación qué rutas tiene.

En este punto es importante tener en cuenta el entorno en que se ejecuta `main.py`
Para verificar esto `ctrl + shift + p` -> `Phyton:Select Interpreter` -> Selecionar el interprete del entorno

#### 3.6. Ejecutar la API

Desde la carpeta FastAPI, con el entorno activo, ejecutar:
```
uvicorn main:app --reload
```
| Parte    | Significado        |
| -------- | ------------------ |
| uvicorn  | servidor           |
| main     | archivo main.py    |
| app      | variable FastAPI   |
| --reload | recarga automática |



Cuando se ejecuta:` uvicorn main:app`

le estás diciendo a Uvicorn dos cosas exactas:

`main` es el archivo `main.py`, sin la extensión `.py`

`app` es el nombre de la variable que contiene el objeto `FastAPI`

Uvicorn traduce esto como: “Importa `main.py` y busca una variable llamada app que sea una aplicación ASGI”

`--reload` le dice a Uvicorn:

“Vigila los archivos del proyecto y reinicia el servidor automáticamente cuando algo cambia.”

#### 3.7. Probar que funciona

Abre el navegador y ve a:
```
http://127.0.0.1:8000
```
resultado
```
{
  "message": "API funcionando"
}
```



#### 3.8. Ver Swagger (clave)

Ve a:
```
http://127.0.0.1:8000/docs
```
Aquí FastAPI:
- muestra los endpoints
- permite probarlos
- documenta automáticamente

**“La API expone documentación automática vía Swagger en /docs.”**

### PASO 4. Crear el endpoint POST /predict (PRÁCTICA + CONCEPTO)

Hasta ahora se tiene:
- un entorno activo
- FastAPI funcionando
- Swagger visible

Ahora vamos a recibir datos, procesarlos y responder JSON.

¿Qué problema vamos a resolver ahora?

Queremos que otro sistema pueda hacer esto:

-> “Te envío un texto y dime algo sobre él”

Eso implica:
- recibir datos desde el request
- validarlos
- devolver una respuesta estructurada

#### 4.1 ¿Cómo se recibe un JSON en FastAPI?

FastAPI usa `Pydantic`, una librería de validación.

**Concepto clave**

No recibes JSON “crudo”, recibes objetos validados.

Para eso defines un modelo de entrada.

#### 4.2 Crear el modelo de entrada (`Pydantic`)

En `main.py`, agrega debajo de los imports:
```
from pydantic import BaseModel
```
Ahora define el modelo:
```
class TextInput(BaseModel):
    text: str
```




Qué significa esto:
- TextInput describe el formato del request
- text: str dice:
  - el campo se llama text
  - debe ser un string
  - es obligatorio

FastAPI usa esto para:
- validar el request
- generar Swagger
- evitar errores

#### 4.4. Crear el endpoint POST /predict

Debajo del endpoint /, agrega:

```
@app.post("/predict")
def predict(data: TextInput):
    return {
        "received_text": data.text
    }
```
Qué está pasando aquí
| Parte                 | Explicación                            |
| --------------------- | -------------------------------------- |
| @app.post("/predict") | Define un endpoint POST                |
| data: TextInput       | FastAPI convierte el JSON en un objeto |
| data.text             | Accedes al valor enviado               |
| return {...}          | Respuesta JSON                         |




FastAPI:
- recibe JSON
- lo convierte a TextInput
- valida automáticamente

Reiniciar y probar:
```
uvicorn main:app --reload
```
Probar en Swagger:
```
http://127.0.0.1:8000/docs
```





### PASO 5. Lógica de negocio: análisis de sentimiento (concepto + práctica)

Ahora tu API ya recibe datos.

El siguiente paso es que haga algo con ellos.

Aquí es donde entra el concepto clave de backend y ML: **La API no “piensa”, la API orquesta lógica**

#### 5.1. ¿Qué vamos a construir ahora?

Un clasificador de sentimiento muy simple, sin modelo .pkl.

Dado un texto:
- devuelve positivo, negativo o neutro
- con un score simple

Esto es suficiente para:
- pruebas
- integración con backend Java
- definir el contrato real


#### 5.2. Separación mental importante

Aunque esté en el mismo archivo, conceptualmente tenemos:
- Entrada (request)
- Lógica (procesamiento)
- Salida (response)

Esto es exactamente lo que haría un modelo ML más adelante.

#### 5.3. Lógica de sentimiento simple (reglas)

Vamos a usar reglas básicas:
- Si contiene palabras positivas → positivo
- Si contiene palabras negativas → negativo
- Si no → neutro

Ejemplo de palabras:
```
Positivas: bueno, excelente, feliz, genial
Negativas: malo, terrible, horrible, triste
```




#### 5.4. Implementar la lógica

Debajo de tus endpoints, agrega esta función:

```
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
```



Concepto importante

Esta función:
- no sabe nada de FastAPI
- podría vivir en otro archivo
- simula el comportamiento de un modelo ML

#### 5.5. Conectar la lógica al endpoint

Ahora modificar el `endpoint /predict`:
```
@app.post("/predict")
def predict(data: TextInput):
    sentiment, score = analyze_sentiment(data.text)

    return {
        "prevision": sentiment,
        "probabilidad": score,
        # "text": data.text
    }
```
->>> "text": data.text, esto se muestra comentado ya que no es necesario dentro del contrato.

#### 5.6. Probar en Swagger

Prueba estos textos:

Caso positivo
```
{
  "text": "El servicio fue excelente"
}
```
Caso negativo
```
{
  "text": "El producto es horrible"
}
```
Caso neutro
```
{
  "text": "El producto llegó ayer"
}
```




#### 5.8. Cómo se ve esto desde backend Java

backend Java ve esto:

- URL: /predict
- Método: POST
- Body:
```
{ "text": "..." }
```
- Response:
```
{
  "sentiment": "positivo",
  "score": 0.9,
  "text": "..."
}
```
Eso es todo lo que necesitan para integrar.
