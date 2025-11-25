---
title: Automatic Pothole Detection System from Road Surface Images
summary: Master's Thesis for the Data Science & Big Data program at U-TAD
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

This project was completed as the **master’s thesis for the Data Science & Big Data program** at [U-TAD](https://www.u-tad.com).

The work carried out for the project includes:

- A study of the state of the art in object detection
- Development of a Python implementation of *YOLO V3* and *YOLO V3 Lite*
- Collection and preparation of a dataset of road images
- Training several *YOLO* models with different configurations and conducting a comparative evaluation of their results
- Conversion of the trained model for deployment on a mobile device
- Development of an Android application to run the model

The project is organized into the following repositories:

| Repository | Description                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| [tfm](https://github.com/dicastro/tfm) | Contains a Python implementation of YOLO V3 and YOLO V3 Lite                                                                |
| [tfm-android](https://github.com/dicastro/tfm-android) | Contains an Android mobile application that runs the trained model using [TensorFlow Lite](https://www.tensorflow.org/lite) |
| [tfm-doc](https://github.com/dicastro/tfm-doc) | Contains the [thesis document [ES]](https://github.com/dicastro/tfm-doc/raw/master/memoria.pdf)                             |

References:

- The images used to train the models were obtained from [Kaggle](https://www.kaggle.com/felipemuller5/nienaber-potholes-2-complex)
- The mobile application is based on a [TensorFlow Lite example](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/android)
- The YOLO V3 implementation is a fork of [this repository](https://github.com/experiencor/keras-yolo3), and the YOLO V3 Lite implementation is based on [this one](https://github.com/qqwweee/keras-yolo3). Both implementations were unified into a single codebase, additional model configuration options were added, and support for more image label formats was included  
