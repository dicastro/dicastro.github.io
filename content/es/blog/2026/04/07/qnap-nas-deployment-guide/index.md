---
slug: guia-tecnica-qnap-ts264-configuracion-blindada
title: "Guía Maestra: Configuración técnica y flujo de datos en mi QNAP TS-264"
summary: "Documentación exhaustiva sobre la capa de almacenamiento, seguridad perimetral invisible y estrategia de backup 3-2-1 para una infraestructura persistente."
date: 2026-04-07
tags:
  - QNAP
  - networking
  - sysadmin
  - backup
  - security
---

Este documento es una guía detallada de la configuración de mi nuevo **QNAP TS-264**. Tras una década con un TS-251, esta transición no es solo un cambio de hardware, sino una evolución hacia un sistema diseñado para la velocidad, la seguridad y la resiliencia. Escribo esto para "mi yo del futuro", asegurando que cada decisión técnica quede registrada y comprendida.

## 1. Escenario de Partida y Estrategia de Sincronización

Vengo de un TS-251 con 2x HDD de 2TB en RAID1 donde, tras 10 años, apenas ocupé unos 200GB. Mi flujo de trabajo actual se apoya en un PC con un **HDD de 1TB dedicado a Qsync**.

Este PC es vital por:

* **Copia física secundaria**: Cumple el primer paso del 3-2-1
* **Agilidad**: Trabajo con documentos y fotos pesadas (sesiones profesionales) localmente y se replican al NAS
* **Sincronización móvil**: El contenido de los smartphones llega al NAS vía **QFile** y de ahí se replica al PC

## 2. Capa de Almacenamiento: El "Efecto SSD"

El TS-264 permite discos NVMe SSD. Mi decisión fue **instalar el SO (QTS) y las aplicaciones en los SSD** para que las bases de datos (como las miniaturas y rostros de QuMagie) vuelen.

### Conceptos fundamentales

* **Storage Pool (Conjunto de almacenamiento)**: La base física donde agrupamos discos (RAID)
* **Volumen Thick (Grueso)**: Reserva el espacio de antemano. Evita la fragmentación y rinde mejor que el *Thin* (que crece bajo demanda), ideal para aplicaciones y bases de datos
* **Sobreaprovisionamiento (Over-provisioning)**: Espacio del SSD que se deja sin usar para que el controlador del disco gestione mejor el desgaste y mantenga el rendimiento cuando el disco se llena

> [!TIP]
> **Lección aprendida**: Para forzar al sistema a instalarse en los SSD, realicé el Wizard inicial **solo con los SSD instalados**, sin los HDD.

### Configuración Detallada

#### SSDSystem (RAID1 - Aplicaciones y SO)

* **Discos**: 2x 500GB (que el sistema ve como 465 GiB)
* **Sobreaprovisionamiento (10%)**: Reservo 45 GiB. El espacio disponible baja a **410 GiB**
* **Snapshots (20%)**: Reservo **82 GiB** (calculado sobre los 410 GiB)
* **Alerta de capacidad (80%)**: Se dispara a los **328 GiB**
* **Volumen Thick**: Asigné **220 GiB**
    * *Cálculo de seguridad*: 220 (Volumen) + 82 (Snapshots) = 302 GiB. Al estar por debajo de los 328 GiB, la alerta no salta de inicio

#### HDDData (RAID1 - Almacenamiento Masivo)

* **Discos**: 2x 4TB (que el sistema ve como 3.64 TiB). No aplica el sobreaprovisionamiento aquí
* **Capacidad Disponible**: 3.63 TiB
* **Snapshots (20%)**: Reservo **0.73 TiB**
* **Alerta de capacidad (80%)**: Se dispara a los **2.9 TiB**
* **Volumen Thick**: Asigné **2.1 TiB**
    * *Cálculo de seguridad*: 2.1 + 0.73 = 2.83 TiB (justo por debajo del umbral de alerta de 2.9 TiB)

## 3. Estructura de Carpetas Compartidas

He diseñado un esquema que separa el rendimiento de la persistencia:

| Carpeta                  | Pool      | Propósito                                                | ¿Backup Cloud? |
|:-------------------------|:----------|:---------------------------------------------------------|:---------------|
| **Documents**            | HDDData   | Documentos en general (facturas, contratos, excels, etc) | Si             |
| **Downloads**            | SSDSystem | Descargas temporales QGet (ahorra estrés al HDD)         | No             |
| **HomeAssistantBackups** | HDDData   | Full backups de HomeAssistant                            | Si             |
| **ManualBackups**        | HDDData   | Backups manuales y del sistema QTS                       | Si             |
| **MediaArchive**         | HDDData   | Multimedia RAW o de terceros (No indexado)               | Si             |
| **MediaGallery**         | HDDData   | Multimedia procesado para consumo (Indexado)             | Si             |
| **MediaLibrary**         | HDDData   | Almacén a largo plazo de descargas (QGet).               | No             |
| **MediaMobile**          | HDDData   | Fotos/Vídeos de móviles vía **QFile** (Indexado)         | Si             |
| **Music**                | HDDData   | Mi colección histórica de música.                        | Si             |

### Multimedia Console e Indexación

He configurado como fuentes de contenido en **Multimedia Console** únicamente las carpetas `MediaMobile` y `MediaGallery`. Esto significa que las miniaturas y el reconocimiento de IA de QuMagie solo trabajarán sobre estas carpetas, ignorando el "archivo muerto" de `MediaArchive`.

## 4. Usuarios y Acceso Seguro

* **Administración**: El usuario `admin` está desactivado. Uso un usuario administrador personal con inicio de sesión **sin contraseña** vía **QNAP Authenticator**
* **Usuarios de Servicio**:
    * `homeassistantbackups`: Acceso exclusivo a su carpeta
    * `homeassistantmonitor`: Permisos delegados de "Monitorización del sistema" para integrar el estado del NAS en HomeAssistant

## 5. Red y Seguridad: El Perímetro Invisible

* **Acceso Externo**: Únicamente vía **Tailscale** (VPN)
* **Proxy y DNS**: Uso **AdGuard Home** y **Nginx Proxy Manager (NPM)** para tener un DNS local y certificados SSL
* **El dilema HTTP**: La conexión interna Proxy -> NAS va por HTTP. Dado que no hay nada expuesto a internet y uso VPN, el riesgo es ínfimo comparado con la complejidad de gestionar certificados Let's Encrypt internos en el NAS sin MyQNAPCloud

> [!WARNING]
> **Problema identificado con Qsync**: Al usar el nombre DNS del Proxy, sufría desconexiones. **Solución**: He configurado Qsync en el PC por **IP directa** del NAS (que es estática por MAC). En el móvil, el DNS funciona perfectamente.

### El caso MyQNAPCloud

He decidido **no utilizarlo** para notificaciones ni acceso. La única excepción es la app **Authenticator**, ya que es un requisito técnico de QNAP para el login sin contraseña. Para la monitorización, uso la integración de HomeAssistant con el usuario `homeassistantmonitor` para enviarme alertas al móvil si algo va mal.

## 6. Instantáneas (Snapshots) y Backups

### Snapshots: El seguro de vida

Son incrementales a nivel de bloque. El primero ocupa el tamaño de los datos, los siguientes solo los cambios. Si nada cambia, no consumen espacio extra.

* **SSDSystem**: Diaria (04:00) - 7 versiones
* **HDDData**: Diaria (04:15) - 30 versiones
* Útiles contra borrados accidentales o ataques de malware

### Backup del Sistema e HBS3

1. **Backup QTS**: Diario (00:30) cifrado en `ManualBackups`
2. **Backup Cloud**: Diario (05:00) cifrado en OneDrive vía HBS3
    * **QuDedup**: Tecnología que elimina duplicados antes de la subida, ahorrando ancho de banda y espacio
    * **Cifrado**: AES-256 en origen (mi clave es la única llave)
    * **Verificación**: Domingos a las 07:00 (rápida) y día 1 de cada mes a las 08:00 (contenido completo)

## 7. Carga Inicial y Plan de Desastre

Cargué los datos usando **Qsync desde el PC**, pausando la sincronización con el NAS viejo, configurando y pausando la sincronización con el NAS nuevo, moviendo el contenido localmente a las nuevas carpetas sincronizadas del TS-264 y finalmente reanudando la sincronización con el NAS nuevo carpeta a carpeta.

### El Kit de Emergencia (Indispensable)

Me di cuenta de un fallo crítico: si perdía el NAS y el gestor de contraseñas (que está en el HomeAssistant), no podría descifrar los backups de OneDrive. Para evitar el bloqueo total, he creado un **ZIP cifrado con clave AES-256 (que si memorizo)** en la raíz de OneDrive y mi PC que contiene:

* Clave de cifrado de HBS3 (OneDrive)
* Clave de cifrado del backup del sistema QTS
* Clave de cifrado del backup de HomeAssistant

Este ZIP es mi "llave maestra" en caso de catástrofe total.