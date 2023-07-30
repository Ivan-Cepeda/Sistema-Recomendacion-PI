from fastapi import FastAPI
import pandas as pd
import numpy as np
import pickle

app = FastAPI()

movies = pd.read_csv('movies.csv')

with open('similarity.pkl', 'rb') as f:
    recomienda = pickle.load(f)

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):
    
      # Definir un diccionario para mapear los nombres de los meses en español a números de mes
    meses = {'enero': 1,'febrero': 2,'marzo': 3,'abril': 4,'mayo': 5,'junio': 6,'julio': 7,'agosto': 8,'septiembre': 9,'octubre': 10,'noviembre': 11,'diciembre': 12}

    # Obtener el número de mes correspondiente al nombre ingresado en español
    num_mes = meses.get(mes.lower())

    if num_mes is None:
        raise ValueError('Nombre de mes inválido')

    # Filtrar las filmaciones por el mes especificado
    movies['release_date'] = pd.to_datetime(movies['release_date'])
    filmaciones_mes = movies[movies['release_date'].dt.month == num_mes]

    # Calcular la cantidad de filmaciones en el mes
    cantidad= len(filmaciones_mes)
    
    cantidad
    return {'mes':mes, 'cantidad':cantidad}

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    retorno_total_director = movies

    # Definir un diccionario para mapear los nombres de los días en español a números de día
    dias = {'lunes': 0,'martes': 1,'miercoles': 2,'jueves': 3,'viernes': 4,'sabado': 5,'domingo': 6}

    # Obtener el número de día correspondiente al nombre ingresado en español
    num_dia = dias.get(dia.lower())

    if num_dia is None:
        raise ValueError('Nombre de día inválido')

    # Convertir la columna 'release_date' a tipo datetime
    retorno_total_director['release_date'] = pd.to_datetime(retorno_total_director['release_date'])
    # Filtrar las filmaciones por el día de la semana
    filmaciones_dia = retorno_total_director[retorno_total_director['release_date'].dt.weekday == num_dia]

    # Calcular la cantidad de filmaciones en el día
    cantidad_filmaciones = len(filmaciones_dia)


    return {'dia':dia, 'cantidad':cantidad_filmaciones}


@app.get('/score_titulo/{titulo_de_la_filmacion}')
def score_titulo(titulo_de_la_filmacion:str):
            
    titulo = titulo_de_la_filmacion.title()
    
    # Buscar el título
    match = movies[movies['title'] == titulo]

    if not match.empty:
        titulo1 = match['title'].values[0]
        anio = match['release_year'].values[0]
        popularidad = match['popularity'].values[0]

        popularidad = round(popularidad, 2)

        return {'titulo':titulo1, 'anio':anio, 'popularidad':popularidad}

    return "No se encontró la película especificada."


@app.get('/votos_titulo/{titulo_de_la_filmación}')
def votos_titulo(titulo_de_la_filmación):
    
    movies['title'] = movies['title'].str.title() # Realizo el cambio de todos los valores de la columna title a mayuscula inicial
    titulo = titulo_de_la_filmación.title()

    if (movies['title'] == titulo).any():
        if movies[movies['title'] == titulo]['vote_count'].item() < 2000:
            return "La película no cuenta con al menos 2000 valoraciones."
        else:
            titulo1 = titulo
            anio = movies[movies['title'] == titulo]['release_year'].item()
            votos = movies[movies['title'] == titulo]['vote_count'].item()
            promedio = movies[movies['title'] == titulo]['vote_average'].item()

            votos= int(votos)

            return {'titulo':titulo1, 'anio':anio, 'voto_total':votos, 'voto_promedio':promedio}
    else:
        return "La película no se encontró."

@app.get('/get_actor/{nombre_actor}')    
def get_actor(nombre_actor:str):
    data = movies
    nombre_a = str(nombre_actor).title()

    if any(isinstance(nombres, str) and nombre_a in nombres for nombres in data['actor']):
        c_filmaciones = data[data['actor'].apply(lambda x: isinstance(x, str) and nombre_a in x)]['title'].count()
        retorno = data[data['actor'].apply(lambda x: isinstance(x, str) and nombre_a in x)]['return'].sum()
        promedio = data[data['actor'].apply(lambda x: isinstance(x, str) and nombre_a in x)]['return'].mean()

        retorno = round(retorno, 2)
        promedio = round(promedio, 2)

        return {'actor':nombre_a, 'cantidad_filmaciones':c_filmaciones, 'retorno_total':retorno, 'retorno_promedio':promedio}

    else:
        return f"El actor {nombre_a} no se encuentra en la base de datos."


def director(df, nombre_director):
        director = df[df['director'] == nombre_director]

        if len(director) == 0:
            return None

        retorno_total_director = director['return'].sum()
        peliculas_director = director[['title', 'release_year', 'return', 'budget','revenue']]
        dir = nombre_director

        return dir, retorno_total_director, peliculas_director

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    resultado = director(movies, nombre_director)
    if resultado is None:
        return {"mensaje": "El director no se encuentra en el dataset."}
    else:
        dir, retorno_total_director, peliculas_director = resultado
        return {
            "director": dir,
            "exito_director": retorno_total_director,
            "peliculas_director": peliculas_director.to_dict(orient='records')}

    
@app.get('/recomendacion/{movie}')
def recomendacion(movie:str):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = recomienda[movie_index]
    movie_list = distances.argsort()[-6:-1]

    te_recomiendo = [(movies.iloc[i].title) for i in movie_list]
    return {'lista': te_recomiendo}