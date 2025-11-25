---
title: TimeHammer
summary: Automated time-tracking system
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

This is a personal project I worked on during the first half of 2020. Its goal is to **remind employees and simplify the time-tracking process** within a company.

The system, called [TimeHammerBot](https://t.me/TimeHammerBot), is a [Telegram chatbot](https://telegram.org/blog/bot-revolution) where employees register by providing their location and usual working schedule. Once configured, **the bot sends reminders at the right moment and provides integrated buttons** to clock in and out directly from the message, without needing to open another application.

The architecture follows an event-driven model ([Event-Driven Architecture](https://en.wikipedia.org/wiki/Event-driven_architecture)). The project is divided into several independent modules, each with a clear responsibility, which communicate by sending messages representing the different events in the system.

The development was done using [Quarkus](https://quarkus.io/), a Java stack that supports compilation to native code. Quarkus supports both imperative and [reactive](https://en.wikipedia.org/wiki/Reactive_programming) programming; for this project, a fully reactive approach was chosen.

Message exchange was handled using [Kafka](https://kafka.apache.org/), whose [Quarkus integration](https://quarkus.io/guides/kafka) is particularly straightforward.

For production, the system runs in [Docker](https://www.docker.com) containers, with one image per module. Deployment currently uses *docker-compose*, although the next planned step is to migrate the solution to a Kubernetes-orchestrated environment.

> The project was discontinued after being presented to the company I was working for at the time. Although it was proposed as a replacement for their existing time-tracking system, they ultimately decided not to adopt it.