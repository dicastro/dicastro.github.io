---
slug: repositorio-propio-home-assistant
title: Home Assistant Applications Repository
summary: Repositorio personalizado de aplicaciones (Add-ons) para Home Assistant OS, optimizado para la persistencia de datos, la automatización de actualizaciones y el desacoplamiento técnico
date: 2026-03-01
tags:
  - HomeAssistant
---

Este proyecto consiste en un **Custom Repository** diseñado específicamente para el ecosistema de **Home Assistant**. Su objetivo es centralizar y facilitar el despliegue de servicios esenciales que no se encuentran disponibles en los repositorios oficiales o que requieren una configuración más ajustada a un entorno de alto rendimiento y privacidad.

El repositorio ha sido desarrollado bajo principios de ingeniería de software que priorizan el **desacoplamiento**. Cada aplicación utiliza una imagen "wrapper" con scripts de inicio agnósticos, lo que permite que los servicios se mantengan actualizados automáticamente sin intervención manual y con total compatibilidad con el sistema de backups nativo de Home Assistant.

## Aplicaciones Incluidas

Actualmente, el repositorio ofrece las siguientes aplicaciones (Applications):

* **Actual Budgets**: Herramienta de gestión financiera personal basada en la privacidad
* **Tandoor Recipes**: Gestor integral de recetas, planificación de comidas y listas de la compra
* **Mailpit**: Servidor SMTP de pruebas y API para la inspección y depuración de correos electrónicos
* **Heimdall**: Dashboard de navegación para centralizar el acceso a todos los servicios de la red local
* **CouchDB**: Servidor de base de datos NoSQL, configurado específicamente para habilitar la sincronización de notas de Obsidian entre dispositivos

## Características Principales

* **Persistencia Garantizada**: Todas las aplicaciones están configuradas para que sus bases de datos y archivos críticos se almacenen en la partición de datos de Home Assistant, asegurando que se incluyan en las copias de seguridad globales
* **Actualizaciones en un Clic**: Gracias a un flujo de trabajo de CI/CD con GitHub Actions y Skopeo, el repositorio ofrece siempre las últimas versiones estables, permitiendo actualizaciones seguras con rollback automático
* **Arquitectura Agnóstica**: Los contenedores están diseñados para ser independientes del sistema operativo base de la imagen original, minimizando fallos por cambios en dependencias externas

{{< embed platform="github" resource="dicastro/homeassistant-apps" type="repo" >}}

## Artículos relacionados

* [La ingeniería detrás de mi Custom Repository para Home Assistant: Desacoplamiento y Automatización]({{< ref "engineering-home-assistant-custom-repository" >}})