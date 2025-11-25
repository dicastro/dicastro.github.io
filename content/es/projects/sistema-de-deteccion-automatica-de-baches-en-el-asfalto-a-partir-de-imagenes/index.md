---
title: Sistema de detección automática de baches en el asfalto a partir de imágenes
summary: TFM del máster en Data Science & Big Data de la U-TAD
date: 2019-09-29
links:
  - type: code
    url: https://github.com/dicastro/tfm
  - type: pdf
    url: /uploads/sistema-de-deteccion-automatica-de-baches-en-el-asfalto-a-partir-de-imagenes.pdf
  - type: video
    url: https://youtu.be/pXQZSrGgzFQ
tags:
  - Data Science
  - Deep Learning
  - YOLO
---

Este proyecto ha sido realizado como **trabajo final del máster en Data Science & Big Data** de la [U-TAD](https://www.u-tad.com).

Para el desarrollo del proyecto se han realizado las siguientes tareas:

- Estudio del estado del arte en lo que a la detección de objetos se refiere
- Desarrollo de una implementación de *YOLO V3* y de *YOLO V3 Lite* en python
- Búsqueda y preparación de un conjunto de imágenes
- Entrenamiento de varios modelos *YOLO* con distintas configuraciones y realización de estudio comparativo de los resultados obtenidos
- Transformación del modelo entrenado para ser explotado en un dispositivo móvil
- Desarrollo de aplicación android para la explotación del modelo

El proyecto se compone de los siguientes repositorios:

| Repositorio | Descripción |
|-------------|-------------|
| [tfm](https://github.com/dicastro/tfm) | Contiene una implementación en python de YOLO V3 y YOLO V3 Lite |
| [tfm-android](https://github.com/dicastro/tfm-android) | Contiene una aplicación móvil android para la explotación del modelo entrenado mediante el uso de [Tensor Flow Lite](https://www.tensorflow.org/lite) |
| [tfm-doc](https://github.com/dicastro/tfm-doc) | Contiene la [memoria del TFM](https://github.com/dicastro/tfm-doc/raw/master/memoria.pdf) |

Referencias:

- Las imágenes utilizadas para entrenar los modelos han sido obtenidas de [kaggle](https://www.kaggle.com/felipemuller5/nienaber-potholes-2-complex)
- La aplicación móvil se basa en un [ejemplo de tensorflow lite](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/android)
- La implementación de YOLO V3 es un fork de [este repositorio](https://github.com/experiencor/keras-yolo3) y la implementación de YOLO V3 Lite está basada en [este repositorio](https://github.com/qqwweee/keras-yolo3). Se han unificado ambas implementaciones en una única, se han añadido más opciones de configuración de los modelos y se soportan más formatos de etiquetas de las imágenes