---
title: HomeLab
summary: Infraestructura personal para gestión de datos, servicios y privacidad
date: 2025-03-07
lastmod: 2025-11-28
tags:
  - Proxmox
  - Docker
  - Ansible
  - Privacidad
---

> [!NOTE]
> Todavía en desarrollo

Homelab es mi infraestructura personal de servidores para gestionar servicios propios, automatizar despliegues y asegurar la privacidad de mis datos. Surge de mi experiencia con un NAS QNAP, que quedó limitado en recursos y velocidad, y de mi interés creciente por depender lo menos posible de servicios de grandes compañías de IT.

El sistema se basa en dos miniPC con Proxmox y Proxmox Backup Server:

- **MiniPC principal:** i9 con 20 cores, 64 GB RAM, 2 TB de almacenamiento. Aquí se ejecutan todas las máquinas virtuales necesarias según los servicios que quiero desplegar.
- **MiniPC secundario:** menos potente, dedicado a Proxmox Backup Server para optimizar el espacio y tener una segunda copia local de los backups.
- **Copia remota cifrada:** se mantiene en un cloud, siguiendo la estrategia 3-2-1 de backups (tres copias, dos medios, una ubicación externa).

Tanto la creación y configuración de las máquinas virtuales como el despliegue de todos los servicios (mediante contenedores Docker) está automatizada con Ansible.

**Servicios que utilizo actualmente**

| Servicio | Uso / para qué sirve |
|---------|------------------------|
| {{<icon name="custom/homer" inline="true">}} [Homer](https://github.com/bastienwirtz/homer) | Dashboard para acceder a todos los servicios del homelab |
| {{<icon name="custom/vaultwarden" inline="true">}} [VaultWarden](https://github.com/dani-garcia/vaultwarden) | Gestor de contraseñas autoalojado compatible con Bitwarden |
| {{<icon name="custom/adguardhome" inline="true">}} [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) | DNS interno con filtro de anuncios, malware y tracking |
| {{<icon name="custom/homeassistant" inline="true">}} [Home Assistant](https://www.home-assistant.io) | Plataforma domótica para integrar y automatizar dispositivos del hogar |
| {{<icon name="custom/zwave" inline="true">}} [ZWave](https://zwave-js.github.io/zwave-js-ui) | Control e integración de dispositivos IoT basados en el protocolo Z-Wave |
| {{<icon name="custom/peanut" inline="true">}} [PeaNut](https://github.com/Brandawg93/PeaNUT) | Monitorización del estado del SAI/UPS mediante interfaz web |
| {{<icon name="custom/owncloud" inline="true">}} [OwnCloud](https://owncloud.com) | Almacenamiento, sincronización y compartición de documentos |
| {{<icon name="custom/immich" inline="true">}} [Immich](https://immich.app) | Galería y almacenamiento privado de fotos con sincronización automática |
| {{<icon name="custom/memos" inline="true">}} [Memos](https://usememos.com) | Gestor ligero de notas y apuntes en texto |
| {{<icon name="custom/lubelogger" inline="true">}} [LubeLogger](https://lubelogger.com/) | Registro y seguimiento de mantenimiento y gastos de vehículos |
| {{<icon name="custom/tandoorrecipes" inline="true">}} [Tandoor Recipes](https://tandoor.dev) | Gestor de recetas, planificación de comidas y listas de compra |
| {{<icon name="custom/tailscale" inline="true">}} [Tailscale](https://tailscale.com) | VPN mesh para acceso remoto seguro sin abrir puertos |
| {{<icon name="custom/mailrise" inline="true">}} [MailRise](https://github.com/YoRyan/mailrise) | SMTP que convierte correos en notificaciones para múltiples plataformas |
| {{<icon name="custom/apprise" inline="true">}} [AppRise](https://github.com/caronc/apprise) | API REST para enviar notificaciones a más de 90 servicios distintos |
| {{<icon name="custom/mailpit" inline="true">}} [MailPit](https://github.com/axllent/mailpit) | Servidor SMTP simulado para pruebas, con visualización web de correos |
| {{<icon name="devicon/portainer" inline="true">}} [Portainer](https://www.portainer.io) | Interfaz gráfica para gestionar contenedores Docker y stacks |
| {{<icon name="custom/actualbudget" inline="true">}} [ActualBudget](https://actualbudget.org) | Gestor de finanzas personales basado en presupuestos |
| {{<icon name="custom/traefik" inline="true">}} [Traefik](https://traefik.io) | Proxy inverso y gestor de certificados TLS con Let's Encrypt |
| {{<icon name="devicon/prometheus" inline="true">}} [AlertManager](https://github.com/prometheus/alertmanager) | Gestión y envío de alertas basado en métricas |
| {{<icon name="devicon/prometheus" inline="true">}} [Prometheus](https://prometheus.io) | Monitorización y recopilación de métricas del sistema y servicios |

**Principales objetivos alcanzados:**

- Acceso remoto seguro a todos los servicios sin abrir puertos directamente en el router.
- Acceso a los servicios mediante DNS interno y generación y renovación automática de certificados TLS con Let's Encrypt, evitando IPs y puertos visibles.
- Organización de servicios según recursos hardware y criticidad de los datos, definiendo frecuencia y número de backups.
- Control total sobre mis datos, almacenamiento y aplicaciones, reemplazando servicios de terceros (como Dropbox, Google Docs, Google Fotos, Google Keep, etc).

{{< embed platform="github" resource="dicastro/homelab" type="repo" >}}