---
slug: ingenieria-custom-repository-home-assistant
title: "La ingeniería detrás de mi Custom Repository para Home Assistant: Desacoplamiento y Automatización"
summary: "Reflexiones técnicas y decisiones de diseño para crear un repositorio de aplicaciones actualizable, agnóstico y eficiente bajo Home Assistant OS."
date: 2026-03-15
tags:
  - HomeAssistant
  - Docker
  - CI/CD
  - DevOps
  - Self-hosting
---

Tras meses de desarrollo y más de un año evolucionando y gestionando una infraestructura compleja basadas en Proxmox, clústeres de Docker y automatizaciones extensas con Ansible, uno alcanza un punto de madurez técnica donde empieza a valorar la eficiencia sobre la complejidad. Mi transición de vuelta a una [Raspberry Pi 5 con Home Assistant OS y un NAS QNAP]({{< ref "the-cost-of-time-why-i-moved-back-to-qnap" >}}) no fue una rendición, sino una optimización. Sin embargo, pronto me encontré con una limitación: las aplicaciones disponibles en los repositorios oficiales y comunitarios no siempre cubren mis necesidades específicas.

La solución fue desarrollar mi propio [Custom Repository]({{< ref "home-assistant-apps-repository" >}}). Centralizar ahí mis servicios me permite aprovechar la sencillez de la RPi5, la robustez de los backups integrados de Home Assistant y la facilidad de actualizar versiones con un solo clic, incluyendo el valioso backup automático previo al upgrade.

## El stack de aplicaciones

Mi objetivo era ejecutar un conjunto de servicios críticos para mi día a día, manteniendo la integridad del sistema:

* **ActualBudgets**: Gestión financiera personal
* **Tandoor Recipes**: Mi gestor de recetas y planificación de comidas
* **Mailpit**: Herramienta de pruebas SMTP para el desarrollo y notificaciones internas
* **Heimdall**: Un dashboard elegante para centralizar el acceso a mis servicios
* **CouchDB**: Implementado no por el servicio en sí, sino como pieza necesaria para la sincronización de notas en Obsidian entre mis dispositivos

> [!NOTE]
> **Cambio de concepto**: Es importante notar que Home Assistant ha evolucionado su nomenclatura; lo que antes conocíamos como "Add-ons" ahora se denominan oficialmente **"Applications"**.

## El reto de la configuración dinámica

La mayoría de estas aplicaciones se configuran mediante variables de entorno. Mi planteamiento inicial fue utilizar el bloque `environment` nativo de Home Assistant.

> [!CAUTION]
> **Problema identificado**: Perdí un tiempo muy valioso intentando que los valores en el bloque `environment` fuesen dinámicos. Tras múltiples intentos, descubrí que la documentación no es clara al respecto: Home Assistant **no permite** que estas variables referencien valores introducidos por el usuario en la interfaz (UI).

Para superar esta limitación sin sacrificar la experiencia de usuario, opté por crear una **imagen Docker "wrapper"**. Esta imagen actúa como un envoltorio que ejecuta un script de `entrypoint` personalizado. Este script tiene acceso al fichero JSON de configuración del usuario en tiempo de ejecución, permitiendo exportar las variables de entorno dinámicamente antes de lanzar el servicio original.

## Filosofía de diseño: Desacoplamiento total

Crear un *wrapper* introduce una capa de complejidad: el riesgo de acoplarse demasiado a la imagen base. Para evitar que el mantenimiento se volviera inmanejable, establecí unos principios de diseño estrictos:

### 1. Independencia del Sistema Operativo
Para que el repositorio sea agnóstico y resistente al tiempo, mi script de `entrypoint` debe saber lo menos posible de la imagen base.
* **Lenguaje universal**: Prefiero `sh` sobre `bash` o `zsh`, ya que está presente en prácticamente cualquier imagen (especialmente en las basadas en Alpine).
* **Herramientas estándar**: Solo utilizo herramientas universales como `sed`, `grep` y `awk`.

> [!IMPORTANT]
> **Lección aprendida**: Es tentador usar `jq` para parsear el JSON de configuración de Home Assistant. Sin embargo, `jq` casi nunca viene preinstalado. Instalarlo implica conocer el gestor de paquetes de la imagen base (`apk`, `apt`, `yum`), lo que te acopla directamente al SO. He preferido complicar el script con `sed` y `awk` antes que perder esta independencia.

### 2. Excepciones justificadas
Solo me he desviado de esta norma cuando el coste de no hacerlo era mayor. Por ejemplo, he instalado `curl` en casos donde era necesario ejecutar un script de inicialización de un tercero que contenía lógica de negocio compleja. Es preferible acoplarse a la presencia de `curl` que intentar replicar una lógica de inicialización que el desarrollador original podría cambiar, rompiendo mi integración.

### 3. Persistencia y permisos
He prestado especial atención a la ubicación de los datos. En ocasiones, he tenido que manipular variables de entorno de forma creativa para forzar que las bases de datos se guarden en rutas mapeadas por Home Assistant para asegurar su inclusión en los backups automáticos. Asimismo, defino explícitamente `PUID` y `GUID` para evitar conflictos de permisos si el usuario por defecto de la imagen base cambiase en un futuro.

### 4. Valores explícitos
Incluso si una aplicación tiene valores por defecto, prefiero establecerlos explícitamente en el script. Si el desarrollador decide cambiar un puerto o una ruta por defecto en una versión futura, mi configuración estática evitará que la aplicación deje de funcionar tras la actualización.

## Workflow de actualización: CI/CD sin fricciones

Para garantizar que el repositorio se mantenga al día sin intervención manual constante, he diseñado un flujo de trabajo basado en **GitHub Actions**:

1.  **Fichero `upgrade.yaml`**: Un componente propio donde defino la versión actual y la fuente (GitHub Releases o Docker Hub Tags).
2.  **Automatización semanal**: Cada lunes, un workflow comprueba si existen nuevas versiones.
3.  **Inspección con Skopeo**: Al detectar una versión nueva, el workflow usa `skopeo` para inspeccionar los metadatos de la imagen original. Obtiene los valores de `ENTRYPOINT` y `CMD` y los guarda en el `build.yaml` de Home Assistant.

> [!TIP]
> **Solución de desacoplamiento**: Gracias a esta inspección, mi script wrapper puede arrancar el servicio original sin necesidad de que yo mire el código para saber cómo se arranca. Esto hace que el repositorio sea verdaderamente independiente de las aplicaciones que contiene.

### Robustez en el filtrado de versiones
El workflow no se limita a coger el último tag:
* Utiliza **Regex** (definidas en el `upgrade.yaml`) para filtrar y asegurar que solo descargamos versiones finales, ignorando versiones de desarrollo o inestables.
* **Paginación inteligente**: Si un servicio publica muchos tags en Docker Hub, el workflow pagina los resultados recuperándolos por orden inverso de creación hasta encontrar el tag correcto.

Finalmente, el workflow actualiza automáticamente la documentación para que sea coherente con la nueva versión. El resultado es un sistema donde Home Assistant me notifica de una actualización y, con un solo clic, el sistema se actualiza de forma segura.

---

Este enfoque me ha permitido recuperar el control total sobre mi ecosistema doméstico, aplicando principios de ingeniería de software para conseguir una solución que, aunque compleja en su construcción, es extremadamente sencilla y eficiente en su operación diaria.