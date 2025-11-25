---
title: TimeHammer
summary: Système d’automatisation de pointage
date: 2020-08-13
lastmod: 2025-11-25
links:
  - type: code
    url: https://github.com/kronostools/timehammer
tags:
  - Java
  - Quarkus
  - EDA
  - Kafka
  - Docker
---

Il s’agit d’un projet personnel sur lequel j’ai travaillé durant la première moitié de l’année 2020. Son objectif est de **rappeler aux employés de pointer et de simplifier le processus de pointage** au sein d’une entreprise.

Le système, appelé [TimeHammerBot](https://t.me/TimeHammerBot), est un [chatbot Telegram](https://telegram.org/blog/bot-revolution) dans lequel les employés s’enregistrent en indiquant leur localisation et leurs horaires habituels. Une fois configuré, **le bot envoie des rappels au bon moment et fournit des boutons intégrés** permettant d’effectuer le pointage directement depuis le message, sans avoir à ouvrir une autre application.

L’architecture est basée sur un modèle orienté événements ([Event-Driven Architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)). Le projet est divisé en plusieurs modules indépendants, chacun avec une responsabilité claire, qui communiquent entre eux via l’envoi de messages représentant les différents événements du système.

Le développement a été réalisé avec [Quarkus](https://quarkus.io/), une pile Java permettant la compilation en code natif. Quarkus supporte la programmation impérative ainsi que la programmation [réactive](https://en.wikipedia.org/wiki/Reactive_programming) ; pour ce projet, une approche totalement réactive a été retenue.

L’échange de messages a été géré avec [Kafka](https://kafka.apache.org/), dont [l’intégration avec Quarkus](https://quarkus.io/guides/kafka) est particulièrement simple.

En production, le système s’exécute dans des conteneurs [Docker](https://www.docker.com), avec une image par module. Le déploiement se fait actuellement via *docker-compose*, bien que la prochaine étape prévue soit une migration vers un environnement orchestré avec Kubernetes.

> Le projet a été abandonné après avoir été présenté à l’entreprise dans laquelle je travaillais à l’époque. Bien qu’il ait été proposé comme remplacement du système de pointage en place, l’entreprise a finalement décidé de ne pas l’adopter.