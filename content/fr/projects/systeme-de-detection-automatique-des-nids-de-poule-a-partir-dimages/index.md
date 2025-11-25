---
title: Système de détection automatique des nids-de-poule sur l'asphalte à partir d'images
summary: Mémoire de fin de master en Data Science & Big Data à l'U-TAD
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

Ce projet a été réalisé comme **travail de fin de master en Data Science & Big Data** à l'[U-TAD](https://www.u-tad.com).

Pour le développement du projet, les tâches suivantes ont été effectuées :

- Étude de l'état de l'art en matière de détection d'objets
- Développement d'une implémentation de *YOLO V3* et *YOLO V3 Lite* en Python
- Recherche et préparation d'un ensemble d'images
- Entraînement de plusieurs modèles *YOLO* avec différentes configurations et réalisation d'une étude comparative des résultats obtenus
- Conversion du modèle entraîné pour son exploitation sur un dispositif mobile
- Développement d'une application Android permettant l'exploitation du modèle

Le projet se compose des dépôts suivants :

| Dépôt | Description                                                                                                                                     |
|-------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| [tfm](https://github.com/dicastro/tfm) | Contient une implémentation en Python de YOLO V3 et YOLO V3 Lite                                                                                |
| [tfm-android](https://github.com/dicastro/tfm-android) | Contient une application mobile Android permettant l'exploitation du modèle entraîné grâce à [TensorFlow Lite](https://www.tensorflow.org/lite) |
| [tfm-doc](https://github.com/dicastro/tfm-doc) | Contient la [mémoire du TFM [ES]](https://github.com/dicastro/tfm-doc/raw/master/memoria.pdf)                                                   |

Références :

- Les images utilisées pour entraîner les modèles proviennent de [Kaggle](https://www.kaggle.com/felipemuller5/nienaber-potholes-2-complex)
- L'application mobile est basée sur un [exemple TensorFlow Lite](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/android)
- L'implémentation de YOLO V3 est un fork de [ce dépôt](https://github.com/experiencor/keras-yolo3) et celle de YOLO V3 Lite est basée sur [ce dépôt](https://github.com/qqwweee/keras-yolo3). Les deux implémentations ont été unifiées en une seule, davantage d'options de configuration ont été ajoutées et davantage de formats d'annotations d'images sont désormais supportés.
