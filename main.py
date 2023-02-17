from fastapi import FastAPI, Request, Form
import pandas as pd
import numpy as np
from flask import Flask, request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

app = FastAPI()


df= pd.read_csv('platforms_and_score' , sep=",")

# Configuro un index de muestra
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Cargando información para la API
@app.get('/about')
async def about():
    return 'API created with FastAPI and Uvicorn'

#API 1) Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type))
@app.get("/get_max_duration")
def get_max_duration_pd(year: int = None, platform: str = None, duration_type: str = None):
    global df   
    # Filtrar el DataFrame
    if duration_type is not None:
        filtered_df = df[df['duration_type'] == duration_type]
    else:
        filtered_df = df.copy()
    if year is not None:
        filtered_df = filtered_df[filtered_df['year'] == year]
    if platform is not None:
        filtered_df = filtered_df[filtered_df['platform'] == platform]

    # Ordenar el DataFrame y obtener la fila con la duración máxima
    sorted_df = filtered_df.sort_values(by='duration_int', ascending=False)
    max_duration = sorted_df.iloc[0][['title']]

    return max_duration
"""
El código anterior usa 
"""  

#API 2) Cantidad de películas por plataforma con un puntaje mayor a XX 
#en determinado año (la función debe llamarse get_score_count(platform, 
# scored, year))
@app.get("/get_score_count/")
def get_score_count(platform: str, scored: int, year:int):
    # Filtrar los datos según las condiciones
    df_filtered = df[(df["platform"] == platform) & (df["scored"] >= scored) & (df["year"] == year)]

    # Contar el número de filas que cumplen las condiciones
    cantidad = len(df_filtered)

    # Devolver la cantidad de veces que se cumple la condición
    return cantidad

"""
El código anterior .
"""  

#API 3) Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
@app.get('/get_count_platform')
def get_count_platform(platform=None):
    # si se proporciona una plataforma, filtrar el dataframe por esa plataforma
    if platform:
        df_filtered = df[df['platform'] == platform]
    else:
        df_filtered = df
    
    # contar la cantidad de películas por plataforma
    count_by_platform = df_filtered['platform'].value_counts()
    
    # si la plataforma existe en el dataframe, devolver la cantidad como un entero
    if platform in count_by_platform.index:
        return int(count_by_platform[platform])
    
    # si no se proporcionó una plataforma, devolver la suma de todas las películas en el dataframe
    elif platform is None:
        return int(count_by_platform.sum())
    
    # si la plataforma no existe en el dataframe, devolver 0
    else:
        return 0
"""
El código anterior 
""" 
#API 4)Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))
@app.get('/get_actor')
def get_actor(platform:str, year:int):
    global df
    # Filtrar por año y plataforma
    filtered_df = df[(df['platform'] == platform) & (df['year'] == year)]

    # Contar la cantidad de veces que aparece cada actor en la columna 'cast'
    actor_count = filtered_df['cast'].str.split(',').explode().str.strip().value_counts()

    # Devolver el actor que más se repite
    if actor_count.empty:
        return None
    else:
        return actor_count.index[0]
"""
El código anterior 
"""  

