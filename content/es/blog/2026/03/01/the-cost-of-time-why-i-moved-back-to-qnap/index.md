---
slug: el-coste-del-tiempo-por-que-he-vuelto-a-qnap
title: "El coste del tiempo: Por qué he decidido cerrar mi Homelab y volver a QNAP"
summary: "Reflexión técnica y personal sobre el paso de una infraestructura virtualizada compleja a un sistema equilibrado basado en la eficiencia y la simplicidad."
date: 2026-03-01
tags:
  - QNAP
  - productividad
  - HomeAssistant
  - self-hosting
  - homelab
---

## El "fracaso" que fue un éxito técnico

Hace unos meses inicié el proyecto de [Homelab Personal]({{< ref "personal-homelab" >}}). Hoy, al anunciar su discontinuación, quiero empezar entrecomillando la palabra "fracaso". Desde un punto de vista técnico, el proyecto ha sido un éxito rotundo. Logré alcanzar un **MVC (Producto Mínimo Viable)** plenamente funcional que resolvía todas las debilidades de mi etapa anterior: acceso exterior seguro sin puertos expuestos, virtualización total y una infraestructura replicable.

Sin embargo, alcanzar este hito me obligó a superar baches técnicos constantes y a dominar un abanico de tecnologías que han supuesto un aprendizaje incalculable:

* **Automatización profesional**: Dominio de Ansible, incluyendo el uso de roles para reutilizar lógica y el desarrollo de scripts complejos
* **Infraestructura como Código**: Despliegue de máquinas virtuales en Proxmox mediante su API y el uso de Ubuntu con cloud-init (claves SSH, red y software preinstalado) para que estuvieran operativas desde el primer segundo
* **Redes y Seguridad**: Configuración de Traefik con Let's Encrypt, Tailscale para el acceso remoto invisible y AdGuard Home como DNS local para eliminar la dependencia de IPs y ficheros hosts
* **Estandarización**: Uso de Portainer gestionado vía API para centralizar los contenedores Docker

> [!TIP]
> **Lección aprendida**: El sistema era elegante, auditable y robusto. No dependía de terceros (salvo Tailscale) y tenía un control absoluto sobre cada bit de mi red. Técnicamente, era la solución "idónea".

## La dura realidad: El mantenimiento como segundo trabajo

A pesar del éxito del MVC, el paso del tiempo me hizo replantearme la solución. El esfuerzo para llegar hasta aquí había sido inmenso, y lo que quedaba por delante no era menor.

Identifiqué tres problemas críticos que empañaban el futuro del Homelab:

* **Pendientes de alta complejidad**: Para tener un sistema de backups serio, necesitaba adquirir un segundo MiniPC para ejecutar Proxmox Backup Server y configurar las tareas de las VMs
* **La trampa de las actualizaciones**: Descubrí que automatizar la detección de nuevas versiones de cada servicio y asegurar un proceso de "un click" con rollback garantizado era una tarea titánica. En el tiempo que tardé en montar el MVC, varios servicios ya se habían quedado obsoletos
* **Pérdida de funcionalidades**: Al instalar HomeAssistant vía Docker para seguir la filosofía del Homelab, perdí la gestión nativa de backups y actualizaciones automáticas del ecosistema OS

## El factor humano: El tiempo como recurso escaso

Siendo padre de una criatura de 4 años, mi tiempo es un recurso extremadamente limitado. He llegado a una conclusión de madurez tecnológica: **este sistema no es el fin, es un medio**.

Mi objetivo no es dedicar mis horas libres a ser un Administrador de Sistemas de mi propia casa. Mi objetivo es tener una ristra de servicios operativos que garanticen mi **privacidad**. El trastear y aprender es gratificante, pero en esta fase de mi vida, quiero una solución que simplemente funcione y me permita dedicar mi escaso tiempo a lo que realmente me satisface.

> [!WARNING]
> **Problema identificado**: El coste de mantenimiento de una solución 100% manual e independiente era demasiado alto. Estaba dedicando más tiempo a "arreglar el servidor" que a "usar los servicios".

## El cambio de perspectiva: El potencial de HomeAssistant

Llevaba años usando HomeAssistant casi por inercia, hasta que profundicé en los **Custom Repos**. Esto cambió mi visión por completo:

* **Soporte oficial**: HA ya incluye de forma nativa herramientas que yo había seleccionado para el Homelab, como **Tailscale** y **AdGuard Home**
* **Gestión simplificada**: Los repositorios personalizados permiten instalar aplicaciones basadas en Docker que se integran en los backups nativos, se actualizan con un clic y permiten un rollback sencillo si algo falla
* **Automatización con GitHub Actions**: Es posible automatizar la detección de versiones en el repositorio para que el propio HA nos sugiera la actualización

## La solución definitiva: QNAP + HomeAssistant (Versión 2026)

He decidido volver a una versión mejorada y profesional de lo que ya me funcionó en el pasado, pero con hardware renovado y una configuración consciente:

**El Hardware**

* **QNAP TS-264**: Un salto cualitativo desde el TS-251. Cuenta con 8GB de RAM de serie. He instalado **2x SSD NVMe de 500GB (RAID1)** para el sistema operativo QTS y aplicaciones (fluidez máxima) y **2x HDD de 4TB (RAID1)** para datos masivos
* **Raspberry Pi 5 (8GB)**: Con un **SSD NVMe de 500GB** montado en una caja **Argon One V5**, garantizando una disipación pasiva excelente y eliminando para siempre el riesgo de las tarjetas SD
* **Ecosistema Oficial de HomeAssistant**: He aprovechado para integrar el hardware oficial (ZBE2 para Zigbee, ZWA2 para Z-Wave y HomeAssistant Voice). Esto me ha permitido:
    * Prescindir de hubs de terceros (como el de IKEA Tradfri)
    * Jubilar el viejo dongle Z-Wave que tenía una resistencia soldada
    * Eliminar Google Home para ganar en privacidad real
    * Ganar orden visual: todos estos dispositivos se alimentan por USB desde la propia RPI 5, reduciendo drásticamente el número de transformadores. Además, es mi forma de apoyar directamente el proyecto (sumado a mi suscripción de Nabu Casa)

**El [Home Assistant Applications Repository]({{< ref "home-assistant-apps-repository" >}})**

He desplegado mi propio repositorio para incluir los servicios que necesito:

* **ActualBudget** y **Tandoor Recipes**
* **Mailpit**: Para capturar correos de sistema sin configurar servidores externos.
* **Heimdall**: Como panel de inicio (sustituyendo a Homer por su facilidad de edición vía UI).
* **CouchDB para Obsidian**: Tras probar Memos y Logseq, me he decantado por **Obsidian**. Su aplicación nativa y el plugin de sincronización vía CouchDB (alojado en mi HA) garantizan una privacidad total y una experiencia móvil impecable.

## Conclusión: Madurez sobre idealismo

Esta solución "simplemente funciona". QNAP y HomeAssistant son sistemas mantenidos que se actualizan sin esfuerzo. Ahora puedo automatizar backups hacia el NAS y tener algo operativo sin sacrificar mis fines de semana.

Es cierto que, idealmente, HomeAssistant debería limitarse a la domótica. Pero la realidad es que su ecosistema es la forma más eficiente de gestionar servicios Docker para alguien que valora su tiempo. Esta vez, he aplicado todo lo aprendido: **cero puertos expuestos, nada de MyQNAPCloud y uso estricto de Tailscale**.

> **Aceptar una solución menos "purista" no es rendirse, es optimizar el recurso más valioso que tenemos: el tiempo.**