---
title: TimeHammer
summary: Sistema de automatización de fichajes
date: 2020-08-13
lastmod: 2025-11-25
links:
  - type: code
    url: https://github.com/kronostools/timehammer
  - type: slides
    url: slides/timehammer
tags:
  - Java
  - Quarkus
  - EDA
  - Kafka
  - Docker
---

Este es un proyecto personal en el que estuve trabajando la primera mitad del 2020. Su objetivo es **recordar y simplificar proceso de fichaje** en una empresa.

El sistema, llamado [TimeHammerBot](https://t.me/TimeHammerBot), es un [chatbot de Telegram](https://telegram.org/blog/bot-revolution) en el que los empleados se registran indicando su ubicación y horario habitual. Una vez configurado, **el bot envía recordatorios en los momentos adecuados y ofrece botones integrados** para realizar el fichaje directamente desde el mensaje, sin necesidad de acceder a orta aplicación.

La arquitectura está basada en un modelo orientado a eventos ([Event-Driven Architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)). El proyecto se divide en varios módulos independientes, cada uno con una responsabilidad clara, que se comunican mediante el envío de mensajes que representan los distintos eventos del sistema.

Para el desarrollo se utilizó [Quarkus](https://quarkus.io/), un *stack* java que permite compilar a código nativo. Quarkus soporta tanto la programación imperativa como la [reactiva](https://en.wikipedia.org/wiki/Reactive_programming); para este proyecto se optó por un enfoque totalmente reactivo.

El intercambio de mensajes se gestionó con [Kafka](https://kafka.apache.org/), cuya [integración con Quarkus](https://quarkus.io/guides/kafka) es especialmente sencilla.

En cuanto a la ejecución en producción, el sistema se ejecuta en contenedores [Docker](https://www.docker.com), con una imagen por cada módulo. Actualmente el despliegue se realiza mediante *docker-compose*, aunque el siguiente paso previsto es migrar la solución a un entorno orquestado con *Kubernetes*.

> El proyecto fue descontinuado después de presentarlo en la empresa en la que trabajaba entonces. A pesar de la propuesta de sustituir el sistema de fichajes existente, finalmente decidieron no adoptarlo.