from fastapi import FastAPI, Request
import pandas as pd
import numpy as np
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app= FastAPI()

# Configuro un index de muestra
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# sirve archivos en la carpeta "img"
app.mount("/static", StaticFiles(directory="static/img"), name="img")

# sirve archivos en la carpeta "js"
app.mount("/static", StaticFiles(directory="static/js"), name="js")

# sirve archivos en la carpeta "sass"
app.mount("/static", StaticFiles(directory="static/sass"), name="sass")

# sirve archivos en la carpeta "vendor"
app.mount("/static", StaticFiles(directory="static/vendor"), name="vendor")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Cargo los datos de manera global
@app.on_event('startup')
def startup():
    global DF
    DF = pd.read_csv(r'C:/Users/rocio/OneDrive/Escritorio/FastAPI/platforms_and_score')

# Cargando información para la API
@app.get('/about')
async def about():
    return 'API created with FastAPI and Uvicorn'

#API 1) Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type))
@app.get("/get_max_duration")
def get_max_duration_pd1(release_year: int = None, source: str = None, duration_type: str = None):
    # Filtrar el DataFrame
    if duration_type is not None:
        filtered_df = DF[DF['duration_type'] == duration_type]
    else:
        filtered_df = DF.copy()
    if release_year is not None:
        filtered_df = filtered_df[filtered_df['release_year'] == release_year]
    if source is not None:
        filtered_df = filtered_df[filtered_df['plataforma'] == source]

    # Ordenar el DataFrame y obtener la fila con la duración máxima
    sorted_df = filtered_df.sort_values(by='duration_int', ascending=False)
    max_duration = sorted_df.iloc[0][['title']]

    return max_duration
"""
El código anterior usa el método str.count() de las columnas del dataframe
para contar la cantidad de veces que aparece una palabra clave en los títulos.
La funcion nos pide como parametro un string para la 'keyword'y opcionalmente un string para la plataforma.
"""  

#API 2) Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))
@app.get("/get_score_count/{plataforma}/{ScoreMedio}/{release_year}")
def get_score_count(plataforma: str, ScoreMedio: int, release_year:int):
    # Contar el número de veces que se cumple la condición
    cantidad = np.count_nonzero(np.where((DF["plataforma"] == plataforma) & (df["ScoreMedio"] >=ScoreMedio) & (df["release_year"] == release_year), True, False))

    # Devolver la cantidad de veces que se cumple la condición
    return cantidad
"""
El código anterior se encarga de contar cuantas peliculas hay en una plataforma
específica con un puntaje mayor a un valor específico y en un año específico.
    Prueba unitaria: https://localhost/disney/2/2018
"""  

#API 3) Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
@app.get("/get_count_platform/{source}")
def get_count_platform(source:str):
    # Filtrar por plataforma
    filtered_df = DF[DF['source'] == source]

    # Contar la cantidad de películas por plataforma
    result = filtered_df.groupby('source').size().reset_index(name='count')

    return result.to_dict(orient='records')
"""
El código anterior ...
""" 

#API 4) Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))
@app.get("/get_actor({source}/{release_year}")
def get_actor(source:str, release_year:int):
    # Filtrar por año y plataforma
    filtered_df = DF[(DF['source'] == source) & (df['release_year'] == release_year)]

    # Contar la cantidad de veces que aparece cada actor en la columna 'cast'
    actor_count = filtered_df['cast'].str.split(',').explode().str.strip().value_counts()

    # Devolver el actor que más se repite
    if actor_count.empty:
        return None
    else:
        return actor_count.index[0]
"""
El código anterior ...
"""  