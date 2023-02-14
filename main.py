#Cargo las librerias
from fastapi import FastAPI
import pandas as pd

#Creo la aplicacion
app = FastAPI()

# Cargando datos
@app.on_event('startup')
def startup():
    global DF
    DF = pd.read_csv('Datasets\movies_and_series.csv')

# Cargando información
@app.get('/')
async def index():
    return {'Individual Proyect of Hector Herrera Espinola, Data Science Bootcamp in SoyHenry'}

# Cargando información para la API
@app.get('/about')
async def about():
    return 'API created with FastAPI and Uvicorn'


# URL para hacer las consultas localhost:8000/get_max_duration(2018,'Hulu','min')
@app.get('/get_max_duration({year},{platform},{min_or_seasson})')
async def get_max_duration(
                            year:int,
                            platform:str,
                            tipo:str):
    platform = platform.replace("'","")
    platform = platform.capitalize()
    tipo = tipo.replace("'","")
    tipo = tipo.lower()
    if tipo == 'min': tipo = 'Movie'    # Determinamos si es pelicula o serie de acuerdo al parámetro
    elif tipo == 'Season': tipo = 'TV Show'
    
    DF1=DF[(DF['RELEASE_YEAR']== year) & (DF['PLATFORM']== platform)] #filtro por año y plataforma
    DF2 =DF1.MOVIE_DURATION.max()
    Titulo = DF1[DF1.MOVIE_DURATION==DF2]['TITLE'].to_list()
    return Titulo[0]



    

#@app.get('/get_max_duration({year},{platform},{min_or_seasson})')
#async   def get_max_duration(
#                            year:int,
#                            platform:str,
#                            min_or_seasson:str):
#   DF2=DF[(DF['RELEASE_YEAR']==year) & (DF['PLATFORM']==platform)]
#    if min_or_seasson == 'min':
#        a=DF2.MOVIE_DURATION.max()
#        title=DF2[DF2.MOVIE_DURATION==a] ['TITLE']
#        title=title.to_list()
#        title=title[0]
#    else:
#        a=DF2.SEASONS.max()
#        title=DF2[DF2.SEASONS==a] ['TITLE']
#        title=title.to_list()
 
#       title=title[0]
#   return title



# URL para hacer las consultas localhost:8000/get_count_plataform('Netflix')
@app.get('/get_count_plataform({platform})')
async def get_count_plataform(platform:str):
    platform = platform.replace("'","")
    platform = platform.capitalize()
    Count_platform = DF[(DF.PLATFORM == platform)]  # Aplicamos una máscara de acuerdo al parámetro
    movies = int(Count_platform[Count_platform.TYPE == 'Movie'].TYPE.value_counts()[0]) # Contamos la cantidad de ocurrencias
    series = int(Count_platform[Count_platform.TYPE == 'TV Show'].TYPE.value_counts()[0])
    # Retornamos el valor en formato str para poder aclarar a qué corresponde cada cantidad
    return platform, f'Movie: {movies}', f'TV Show: {series}'


# URL para realizar la consulta localhost:8000/get_actor('Netflix',2018)
@app.get('/get_actor({Platform},{Year})')
async def get_actor(platform:str,year:int):
    platform = platform.replace("'","")
    platform = platform.capitalize()
    actores, repeticiones = list(), list()  # Creamos dos listas vacías para colocar cada actor y la cantidad de veces
    # Aplicamos máscara para obtener una lista de listas de actores, que no tengan nulos
    Cast_list = list(DF[(DF.PLATFORM == platform) & (DF.RELEASE_YEAR == year)].CAST.fillna(''))

    for each in Cast_list:  # Iteramos cada elemento, que es a su vez una lista de actores
        if not(each == '' or each is None):    # Validamos que tenga datos
            list1 = each.split(",") # Separamos por comas, para obtener una lista nueva cuyos elementos sean los actores
            for elem in list1:  # Iteramos sobre esta nueva lista de actores
                elem = elem.strip() # Limpiamos los espacios vacíos
                # Si el actor ya se encuentra en 'actores', entonces sumará 1 en 'apariciones' con el mismo índice
                if elem in actores: 
                    repeticiones[actores.index(elem)] += 1
                # De lo contrario, agregará el actor en 'actores' y 1 en 'apariciones'
                else:    
                    actores.append(elem)
                    repeticiones.append(1)
    if actores == []: return 'No hay datos' # Para el caso de que ambas listas queden vacías, que no retorne error
    # Retornamos la plataforma, el actor que más se repite en esa plataforma y ese año, y cuántas veces lo hace
    return (platform, max(repeticiones), actores[repeticiones.index(max(repeticiones))])