# <h1 align="center"> Proyecto Integrador #01 <br> MLOps Juegos Steam - Modelo de recomendación </h1>
![Alt text](src/image.png)
## Presentación del problema - Contexto
En este proyecto se emprendió la labor de desarrollar un sistema de recomendación de videojuegos para la plataforma de Steam desde cero. Se logró ofrecer una solución integral que abarcó desde la gestión de datos hasta la implementación de una API utilizando la librería FastAPI. El propósito principal de este proyecto consistió en brindar a los usuarios una herramienta eficaz para descubrir nuevos juegos, basándose en un análisis de sentimiento, datos de los desarrolladores, interacciones de los usuarios y un modelo de aprendizaje automático.

## Rol a desarrollar

El proyecto se llevó a cabo en la función de un `Ingeniero de datos` y `Científico de Datos`. Fue necesario presentar un Producto Mínimo Viable (MVP) que cumpliera con los criterios de evaluación definidos:

- Transformaciones de datos
- Creación de una API de desarrollo
- Implementación
- Realización de un Análisis Exploratorio de Datos (EDA)
- Desarrollo de un sistema de recomendación
- Documentación en formato de video.

## Desarrollo del Proyecto:

El sistema se estructura en dos etapas principales:

### 1. Ingeniería de Datos y Creación de la API

- `ETL y Feature Engineering` - Extracción, Transformación y Carga : En primer lugar, se llevó a cabo la limpieza y formateo inicial del conjunto de datos para asegurar su correcta interpretación. Posteriormente, se aplicó un análisis de sentimiento mediante procesamiento del lenguaje natural (NLP) para generar la columna 'opinión', lo que permitió mejorar el rendimiento de la API y facilitar el entrenamiento de los modelos de aprendizaje automático.

- `API` con FastAPI: Se ideó y desarrolló una interfaz de programación de aplicaciones (API) utilizando FastAPI, la cual ofrece diversas consultas a los datos disponibles. Esto posibilita obtener información acerca de los desarrolladores, usuarios, géneros y juegos.

- `Deployment` La API se encuentra desplegada y disponible para su acceso en línea, utilizando el servicio Render y siguiendo el tutorial disponible en el repositorio.

### 2. Análisis Exploratorio de Datos (EDA) y Desarrollo de Modelos de Aprendizaje Automático

- `Exploración de datos` Se llevó a cabo un análisis en profundidad de los datos con el propósito de comprender mejor las relaciones entre las variables en el conjunto de datos. Esto incluyó la identificación de valores atípicos, anomalías y patrones de interés que servirían como base para un análisis más detallado.

- `Modelos de Recomendación` Se pusieron en práctica al menos uno de dos tipos de sistemas de recomendación: el basado en elementos (ítem-ítem) y el basado en usuarios (usuario-ítem). Estos modelos posibilitan la recomendación de juegos similares, ya sea en función de la similitud entre los elementos o de los usuarios.

### Documentación

`Deploy` https://mayra.onrender.com/docs

`Vídeo de presentación del proyecto`

`Fuente de Datos` https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj

## Autora:

[<img src="https://avatars.githubusercontent.com/u/123905946?v=4" width=115><br><sub>Mayra Sierra Torres</sub>](https://github.com/MayraSierraAT)


[![Linkedin: mayrasierraat](https://img.shields.io/badge/-mayrasierraat-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/mayrasierraat/)](https://www.linkedin.com/in/mayrasierraat/)
[![Gmail: mayrasierraat@gmail.com](https://img.shields.io/badge/Gmail-mayrasierraat@gmail.com-red)](mailto:mayrasierraat@gmail.com)
