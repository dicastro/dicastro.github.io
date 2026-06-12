---
slug: de-la-resistencia-soldada-al-homelab-el-cambio-necesario
title: "De la resistencia soldada al Homelab: El fin de una era y el cambio de enfoque"
summary: "Crónica de una década de aprendizaje en privacidad y self-hosting: desde el hardware parcheado de un QNAP hasta la ambición de un Homelab virtualizado con Proxmox."
date: 2025-08-01
tags:
  - homelab
  - QNAP
  - privacy
  - self-hosting
  - proxmox
---

## El inicio: La búsqueda de la soberanía digital

Hace aproximadamente una década, mi relación con la tecnología dio un giro fundamental. Empecé a ser consciente de la fragilidad de la privacidad en la era de las grandes nubes y decidí que quería ser el **único propietario de mis datos**. El concepto era sencillo pero ambicioso: dejar de depender de terceros para mis necesidades digitales diarias.

Tras investigar las opciones del mercado, me decanté por el ecosistema de **QNAP**. En aquel momento, parecía la opción más madura: ofrecía aplicaciones multiplataforma, tanto para escritorio como para móvil, y demostraba una evolución constante. Mi objetivo era ambicioso:

* **Reemplazar a Dropbox y Google Drive**: Utilizando las herramientas de sincronización de QNAP
* **Reemplazar a Google Photos**: Con una aplicación capaz de identificar caras, crear líneas temporales, geoposicionar imágenes y reconocer objetos
* **Reemplazar a Google Keep**: Centralizando mis notas en un servidor bajo mi control

Para materializar esta visión, adquirí un QNAP **TS-251** con 2TB de almacenamiento en RAID1 y 2GB de RAM. Fue mi primera gran apuesta por el self-hosting.

> [!TIP]
> **Lección aprendida sobre redundancia**: Con el paso de los años, experimenté fallos en los discos duros en dos ocasiones. Mi política desde entonces fue tajante: si un disco falla y ambos fueron comprados a la vez, el segundo tiene una alta probabilidad de caer pronto. Por precaución, siempre cambio ambos discos simultáneamente.

## La llegada de HomeAssistant: Más allá del almacenamiento

Poco después, mi curiosidad me llevó a **HomeAssistant**. Me fascinó su filosofía: una solución de domótica que no te ataba a un fabricante concreto y respetaba escrupulosamente la privacidad.

Comencé con una Raspberry Pi (que con el tiempo evolucionó de una versión 3 a una **4B de 8GB** con SD de 32GB). Mi red domótica se convirtió en un crisol de tecnologías: bombillas IKEA Tradfri para el salón y un relé doble Z-Wave para la cocina. Incluso cedí un ápice en mi privacidad conectando un Google Home para dar instrucciones de voz, asumiendo ese *trade-off* por la comodidad.

Como parte de esta evolución a la Raspberry Pi 4B, me encontré con un obstáculo técnico: el dongle USB Z-Wave que utilizaba dejó de funcionar. Al parecer, existía un problema de compatibilidad entre el firmware del dongle y los puertos USB de la nueva RPI, que no llegaba a detectarlo. Tras investigar en foros, encontré a un usuario que había documentado una solución: soldar una pequeña resistencia en el propio dongle. Realicé la modificación y, efectivamente, el dispositivo volvió a la vida. Aunque no volvió a dar problemas, este incidente sembró en mí una primera semilla de incertidumbre sobre la fiabilidad de mi hardware "parcheado".

Sin embargo, pronto descubrí que HomeAssistant era mucho más que luces y relés. Se convirtió en mi navaja suiza de servicios:

* **VaultWarden**: Como gestor de contraseñas (reemplazando todas mis claves repetidas por contraseñas únicas y complejas)
* **WireGuard**: Para tener una VPN segura hacia mi red local
* **NGINX Proxy Manager**: Para gestionar un dominio con SSL
* **NUT**: Para gestionar el apagado controlado mediante un SAI

> [!WARNING]
> **Problema identificado**: Durante años, HomeAssistant y QNAP permitían actualizaciones con un solo clic. Sin embargo, en las fases iniciales de HomeAssistant, los breaking changes eran frecuentes. Invertí incontables horas investigando cómo arreglar configuraciones que el sistema simplemente dejaba de soportar tras una actualización.

## La acumulación de debilidades: Un sistema al límite

A medida que pasaba el tiempo, mi lista mental de "cosas que no van bien" no dejaba de crecer. El sistema que un día pareció robusto empezaba a mostrar grietas preocupantes:

1. **Hardware insuficiente**: El TS-251 era exasperantemente lento, especialmente con las aplicaciones de notas y fotos. Incluso ampliando la RAM a 4GB, el rendimiento era pobre y ya no había margen de mejora física
1. **Riesgo en el almacenamiento**: Aunque nunca perdí datos, vivía con el miedo constante al fallo de la tarjeta SD de la Raspberry Pi, un problema documentado por miles de usuarios
1. **Dependencias mal entendidas**: No me sentía cómodo con que HomeAssistant albergara servicios tan críticos como mi gestor de contraseñas o mi proxy inverso. Para mí, HA debía ser domótica, el resto de servicios necesitaban su propia independencia
1. **Agujeros de seguridad por desconocimiento**: Por aquel entonces, el volumen de información y opciones me abrumaba. Cometí errores de manual:
   * Expuse puertos del QNAP y de HomeAssistant directamente en el router
   * Activé UPnP para facilitar la apertura de puertos
   * No entendí herramientas como MyQNAPCloud, configurando cosas "a ciegas" sin saber si eran necesarias
   * **Consecuencia**: Cada día recibía intentos de login fallidos en el QNAP, lo que me obligaba a gestionar listas negras constantemente

> [!NOTE]
> **Solución no entendida en su momento**: Tenía un dominio apuntando constantemente a la IP de mi casa (actualizada vía DNS dinámico), algo que me generaba una incomodidad creciente pero que no sabía cómo evitar si quería acceso exterior.

## El detonante: La cirugía de la resistencia

El punto de no retorno llegó el día que el QNAP TS-251 dejó de arrancar. Tras comprobar que los discos estaban sanos, encontré en un foro el diagnóstico: un **fallo del reloj del procesador Intel Celeron**.

Un usuario había documentado magistralmente cómo soldar una resistencia de 100 ohmios en la placa base para "engañar" al sistema y resucitarlo. Sin nada que perder, hice la cirugía. **Funcionó**. Pero la incertidumbre era total. Aquello era un parche, una cuenta atrás. Necesitaba una solución nueva antes de que el parche fallara definitivamente.

## El cambio de enfoque: El proyecto Homelab

Este incidente fue el catalizador para replantearlo todo. No quería simplemente comprar otro NAS y repetir errores. Decidí dar el salto a un **MiniPC con Proxmox**.

Este cambio de paradigma me ofrecía:

* **Potencia real**: Procesador moderno, mucha más RAM y escalabilidad
* **Virtualización y Docker**: Estandarizar la instalación de software y separar HomeAssistant de servicios críticos como **VaultWarden**
* **Seguridad Invisible**: Sustituir la apertura de puertos por **Tailscale**. Aunque dependa de un tercero (cuya parte open-source me permite auditarlo), me permite eliminar toda exposición en el router
* **Independencia de QNAP**: Sustituir sus apps nativas por **OwnCloud** (ficheros) e **Immich** (fotos/vídeos)
* **Infraestructura como Código**: Usar **Ansible** para automatizar toda la instalación, asegurando que en caso de catástrofe el sistema fuera replicable sin manualidades
* **Nuevos Horizontes**: Poder correr por fin servicios que antes me daban problemas, como ActualBudget, Tandoor Recipes o PiHole

Así es como surge el proyecto [Homelab Personal]({{< ref "personal-homelab" >}}). No se trata solo de hardware nuevo, es un manifiesto de cómo entiendo hoy la privacidad, el mantenimiento y el control total sobre mis servicios. El viaje del "parche" a la infraestructura profesional acaba de empezar.