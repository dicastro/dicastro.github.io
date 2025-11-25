---
title: TimeHammer
summary: Sistema de automatización de fichajes
date: 2020-08-14
lastmod: 2020-09-05
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  theme: white
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

<img style="border: none; box-shadow: none; margin-bottom: 30px" data-src="./timehammer_title_revealjs.png" width="800">

### Sistema de automatización de fichajes

---

## Objetivo

El principal objetivo es **simplificar el proceso de fichajes** de una empresa

<small>Un objetivo secundario es el de utilizar tecnologías para **seguir creciendo como profesional de la Informática**.</small>

---

<section data-markdown>
  <script type="text/template">
    ## Contexto
    - Recordar cada una de las acciones a realizar <!-- .element: class="fragment" -->
    - Para ciertas acciones hay que escribir un texto adicional <!-- .element: class="fragment" -->
    - Login requerido para realizar cada una de las acciones <!-- .element: class="fragment" -->
    - Intranet no adaptada al uso desde el móvil <!-- .element: class="fragment" -->
  </script>
</section>

---

<section data-markdown>
  <script type="text/template">
    ## Requisitos
    - Fichaje lo más fiel posible a la realidad <!-- .element: class="fragment" -->
    - El usuario no tiene que recordar realizar ninguna acción <!-- .element: class="fragment" -->
    - Las acciones manuales por parte del usuario serán muy sencillas <!-- .element: class="fragment" -->
    - Se tendrán en cuenta los fichajes realizados directamente en la intranet <!-- .element: class="fragment" -->
  </script>
</section>

---

## Solución

La solución desarrollada es un **chatbot de telegram**:

**TimeHammerBot**

https://t.me/TimeHammerBot

<small>Lo único necesario para poder utilizarla será disponer de un smartphone y tener instalada la aplicación de mensajería *Telegram*. También compatible con la versión web de *Telegram*</small>

---

<section data-markdown>
  <script type="text/template">
    ## Funcionamiento
    #### Trabajador
    1. Registro en el chatbot <!-- .element: class="fragment" -->
      - Hora de inicio y final de la jornada <!-- .element: class="fragment" -->
      - Hora de inicio y final de la comida <!-- .element: class="fragment" -->
      - Lugar de trabajo <!-- .element: class="fragment" -->
    1. Se olvida de volver a fichar <!-- .element: class="fragment" -->
  </script>
</section>

---

<section data-markdown>
  <script type="text/template">
    ## Funcionamiento
    #### Chatbot
    1. Llegada la hora de una determinada acción <!-- .element: class="fragment" -->
      - Comprueba el estado del trabajador <!-- .element: class="fragment" -->
      - Si procede, notifica al trabajador <!-- .element: class="fragment" -->
    1. El trabajador recibe la notificación <!-- .element: class="fragment" -->
      - Confirma/Postpone/Cancela la acción <!-- .element: class="fragment" -->
    2. El chatbot recibe la respuesta <!-- .element: class="fragment" -->
      - Ejecuta la acción en la intranet <!-- .element: class="fragment" -->
      - Se queda a la espera <!-- .element: class="fragment" -->
      - Ignora la acción hasta el día siguiente <!-- .element: class="fragment" -->
  </script>
</section>

---

<section data-markdown>
  <script type="text/template">
    ## Ejemplo 1
    Trabajador >> lunes | comienzo jornada | 8:00
    - A las 8:00 recibirá un mensaje preguntándole si ya ha comenzado a trabajar <!-- .element: class="fragment" -->
    - Debajo del mensaje aparecerán una serie de botones: Sí, +5m, +10m, +15m, +20m, No <!-- .element: class="fragment" -->
    - Con solo pulsar un botón el chatbot actuará en consecuencia <!-- .element: class="fragment" -->
  </script>
</section>

---

<section data-markdown>
  <script type="text/template">
    ## Ejemplo 2
    Trabajador >> vienes | comienzo jornada | 8:00
    - Comienza a trabajar antes de lo normal <!-- .element: class="fragment" -->
    - Fichaje manual en la intranet a las 7:30 <!-- .element: class="fragment" -->
    - A las 8:00 el chatbot comprobará el estado y verá que no tiene nada que notificar <!-- .element: class="fragment" -->
  </script>
</section>

---

## Extra I

El chatbot busca **molestar lo menos posible**

- Fines de semana
- Festivos
  - Ciudad de trabajo
- Vacaciones

---

## Extra II

**No se persiste la contraseña** de los usuarios, se guardan en memoria.

<small>Si se reinicia el contenedor que tiene en memoria las contraseñas, se enviará un mensaje a los trabajadores para que vuelvan a introducir su contraseña.</small>

---

# DEMO

---

<section data-markdown>
  <script type="text/template">
    ## Objetivos cumplidos
    - Todos los fichajes requieren de una confirmación y son fieles a la realidad <!-- .element: class="fragment" -->
    - El usuario ya no tiene que recordar realizar una determinada acción <!-- .element: class="fragment" -->
    - La única acción manual del usuario consiste en pulsar un botón<!-- .element: class="fragment" -->
    - El usuario ya no tiene que conectarse a una intranet <!-- .element: class="fragment" -->
    - Al recuperar siempre el estado del usuario de la intranet, se posibilita combinar el uso de ambos sistemas para situaciones excepcionales <!-- .element: class="fragment" -->
  </script>
</section>

---

## Stack tecnológico

<ul>
<li>Java</li>
<li>Quarkus</li>
<li>Docker</li>
<li>Telegram Bots</li>
<li>Kafka</li>
<li>PostgreSQL</li>
</ul>

---

## Event Driven Architecture I

<img style="border: none; box-shadow: none; margin-bottom: 30px" data-src="./timehammer_event_driven-architecture_01_slide.png" title="Flujo de actualización de estado de trabajadores">

---

## Event Driven Architecture II

<img style="border: none; box-shadow: none; margin-bottom: 30px" data-src="./timehammer_event_driven-architecture_02_slide.png" title="Flujo de procesamiento de un comando">

---

## Roadmap I

#### Reducción de llamadas a Comunytek

En la versión actual se realizan:

<small>30 * 12 + 6 * 12 + 4 = 436 llamadas/usuario/día</small>

Con la versión mejorada se realizarían:

<small>3 llamadas/acción * 4 acciones/día/usuario = 12 llamadas/usuario/día</small>

---

## Roadmap II

#### Kubernetes I

<img style="border: none; box-shadow: none;" data-src="./kubernetes_cluster_01.jpg" title="Caja cluster" width="60%">

---

## Roadmap II

#### Kubernetes II

<img style="border: none; box-shadow: none;" data-src="./kubernetes_cluster_02.jpg" title="Raspberry Pi y PoE Hat" width="60%">

---

## Roadmap II

#### Kubernetes III

<img style="border: none; box-shadow: none;" data-src="./kubernetes_cluster_03.jpg" title="Bandeja Raspberry Pi" width="60%">

---

## Roadmap III

- Anular el registro
- Modificar la configuración
- Mejorar validaciones en el registro
- Añadir tests
- Tunear configuración Kafka
- Añadir monitorización de módulos
- NLP
- Modulo de administración

---

<section data-markdown>
  <script type="text/template">
    ## Chatbots I
    - Los chatbots son una herramienta mucho potencial que permite aplicar un nuevo enfoque para resolver ciertos problemas <!-- .element: class="fragment" -->
    - Los usuarios están cada vez más acostumbrados a las aplicaciones de mensajería <!-- .element: class="fragment" -->
    - Tienen peor fama de la que se merecen porque muchos de los que se hacen llamar chatbots, hacen un mal (o nulo) procesamiento del lenguaje natural y realmente se trata de una sucesión de condiciones lógicas que ejecutan ciertas acciones <!-- .element: class="fragment" -->
  </script>
</section>

---

<section data-markdown>
  <script type="text/template">
    ## Chatbots II
    - Con este proyecto se muestra un **enfoque diferente** de chatbot, basado en el uso de **comandos**. Que mediante el uso de diferentes **teclados** que se **adaptan** al tipo de respuesta que esperas del usuario, **mejora** mucho la **usabilidad**
  </script>
</section>

---

## Caso de Uso

Nuevo canal de comunicación para la realización de guardias