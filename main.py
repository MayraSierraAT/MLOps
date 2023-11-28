"""
AQUI SE ENCUENTRAN LAS FUNCIONES CREADAS PARA EL PROYECTO INTEGRADOR 1 
MLOPS - STEAM GAMES - 

FUNCIONES PARA ALIMENTAR LA API
"""

#librerías
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity

#instanciar la aplicación

app = FastAPI()


#dataframes que se utilizan en las funciones de la API
funcion1= pd.read_parquet("data/PlayTimeGenre.parquet")
funcion2= pd.read_parquet("data/UserForGenre.parquet")
funcion3= pd.read_parquet("data/UsersRecommend.parquet")
funcion4r= pd.read_parquet("data/UsersWorstDeveloper.parquet")
funcion5= pd.read_parquet("data/sentimiento_analisis.parquet")
modelo= pd.read_parquet("data/modelo_render.parquet")



@app.get("/", response_class=HTMLResponse)
async def incio ():
    principal= """
    <!DOCTYPE html>
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas sobre juegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam donde se pueden hacer diferentes consultas sobre la plataforma de videojuegos.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=principal)


# Antes de la definición de la función
similitudes = cosine_similarity(modelo.iloc[:,3:])



#Primera función
@app.get("/playtimegenre/{genre}", name="PLAYTIMEGENRE")
async def PlayTimeGenre(genre: str):
    """
    Debe devolver año con mas horas jugadas para dicho género.
    
    Parametro: 
    Action, Adventure, RPG, Strategy, Simulation, Casual, etc.

    """
    # Filtramos por genero
    data_genres = funcion1[funcion1['genres'].str.contains(genre)]
    # Agrupamos por año y sumamos las horas jugadas
    data_genres = data_genres.groupby('release_year')['playtime_forever'].sum().reset_index()
    # Obtenemos el año con mayor horas jugadas
    year = int(data_genres[data_genres['playtime_forever'] == data_genres['playtime_forever'].max()]['release_year'].values[0])    
    return {'Año de lanzamiento con más horas jugadas para Género': genre, 'Año': year}



#Seguna Función
@app.get("/userforgenre/{genre}", name="USERFORGENRE")
async def UserForGenre(genre: str):
    # Filtramos por género
    data_genres = funcion2[funcion2['genres'].str.contains(genre)].copy()  # Copiamos el DataFrame para evitar la advertencia
    # Convertir minutos a horas y redondear a números enteros
    data_genres.loc[:, 'playtime_forever'] = (data_genres['playtime_forever'] / 60).round().astype(int)
    # Agrupamos por usuario y sumamos las horas jugadas
    data_playtime = data_genres.groupby('user_id')['playtime_forever'].sum().reset_index()
    # Obtenemos el usuario con más horas jugadas
    user = data_playtime.loc[data_playtime['playtime_forever'].idxmax()]['user_id']
    # Filtramos por usuario
    data_user = data_genres[data_genres['user_id'] == user]
    # Agrupamos por año y sumamos las horas jugadas
    data_year = data_user.groupby('release_year')['playtime_forever'].sum().reset_index()
    years = data_year.to_dict('records')
    # Obtenemos el año con más horas jugadas
    year = int(data_genres[data_genres['playtime_forever'] == data_genres['playtime_forever'].max()]['release_year'].values[0])
    
    return f"'Usuario con más horas jugadas para Género {genre}': {user}, 'Horas jugadas': {years}"



#Tercera funcion
@app.get("/usersrecommend/{year}", name = "USERSRECOMMEND")
async def UsersRecommend( year : int ):
    # Filtramos por año
    data_year = funcion3[funcion3['release_year'] == year]
    # Verifica que exista informacion del año solicitado
    if data_year.empty:
        # Devuelve un mensaje de error
        return {f"No hay datos para el año {year}"}
    # Agrupo por juego y sumo sentimientos
    games_group = funcion3.groupby(['app_name'])['sentiment_analisis'].sum()
    # Ordeno de mayor a menor
    rank = games_group.sort_values(ascending=False)    
    # Top 3
    top_3 = rank.head(3) 
    response = []
    i = 1
    for title, j in top_3.items():
        dic = {f'Puesto {i}':title}
        response.append(dic)
        i += 1
    return {'Top 3 de juegos MÁS recomendados por usuarios para el año': year, 'Top 3': response}




#Cuarta función
@app.get("/usersworstdeveloper/{year}", name = "USERSWORSTDEVELOPER")
async def UsersWorstDeveloper(year: int, funcion4: pd.DataFrame):
    # Verificamos si el año está dentro del rango esperado
    rango_aceptado = range(2010, 2018)
    if year not in rango_aceptado:
        return {"message": "Mi base de datos solo tiene registros entre 2010 y 2017"}

    # Filtramos por comentarios no recomendados y sentiment_analysis negativo
    df_filtered = funcion4[(funcion4['recommend'] == False) & (funcion4['sentiment_analisis'] == 0)]

    # Filtramos por el año deseado
    df_filtered_year = df_filtered[df_filtered['release_year'] == year]

    # Si no hay datos para el año, retornamos mensaje
    if not df_filtered_year.empty:
        # Obtener los top 3 desarrolladores con menos recomendaciones
        top_developers = df_filtered_year['developer'].value_counts().head(3).reset_index()
        top_developers = top_developers.rename(columns={'index': 'Puesto 1', 'developer': 'Desarrollador'})

        # Modificamos la estructura del resultado
        result = [{"Puesto {}".format(i + 1): desarrollador} for i, desarrollador in enumerate(top_developers['Desarrollador'])]
    else:
        result = {"No hay juegos no recomendados para el año {}".format(year)}

    return {'Top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año': year, 'Top 3': result}



#Quinta función
@app.get("/sentimentanalysis/{year}", name="SENTIMENTANALYSIS")
async def sentiment_analysis(year: int):
    # Filtramos por año
    data_year = funcion5[funcion5['release_year'] == year]
    # Agrupamos por sentimiento y contamos las reseñas
    data_year = data_year.groupby('sentiment_analisis')['review'].count().reset_index()
    # Obtenemos el top 3
    sentiment = data_year.to_dict('records')
    # Inicializar contadores
    negative_count = 0
    neutral_count = 0
    positive_count = 0
    # Contar el número de reseñas con cada sentimiento
    for s in sentiment:
        if s['sentiment_analisis'] == 0:
            negative_count += s['review']
        elif s['sentiment_analisis'] == 1:
            neutral_count += s['review']
        elif s['sentiment_analisis'] == 2:
            positive_count += s['review']
    # Crear el diccionario con los contadores
    sentiment = {'Negative': negative_count, 'Neutral': neutral_count, 'Positive': positive_count}
    return {'Según el año de lanzamiento': year, 'Sentimiento': sentiment}



#Modelo de recomendación item-item
@app.get("/recomendacion_juego/{id}", name= "RECOMENDACION_JUEGO")
async def recomendacion_juego(id: int):
    
    id = int(id)
    # Filtrar el juego e igualarlo a  su ID
    juego_seleccionado = modelo[modelo['item_id'] == id]
    # devolver error en caso de vacio
    if juego_seleccionado.empty:
        return "El juego con el ID especificado no existe en la base de datos."
    
    # Calcular la matriz de similitud coseno
    #similitudes = cosine_similarity(modelo_item.iloc[:,3:])
    
    # Calcula la similitud del juego que se ingresa con otros juegos del dataframe
    similarity_scores = similitudes[modelo[modelo['item_id'] == id].index[0]]
    
    # Calcula los índices de los juegos más similares (excluyendo el juego de entrada)
    indices_juegos_similares = similarity_scores.argsort()[::-1][1:6]
    
    # Obtener los nombres de los juegos 5 recomendados
    juegos_recomendados = modelo.iloc[indices_juegos_similares]['app_name']
    
    return juegos_recomendados