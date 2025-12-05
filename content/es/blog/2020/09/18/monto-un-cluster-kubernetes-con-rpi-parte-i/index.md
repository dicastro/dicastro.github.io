---
title: Monto un cluster Kubernetes con Raspberry Pi (parte I)
summary: Primera parte de una serie donde explico cómo he montado un cluster de Kubernetes utilizando Raspberry Pi. En esta entrega describo el hardware y la infraestructura física utilizada.
date: 2020-09-18
lastmod: 2025-12-03
tags:
  - kubernetes
  - cluster
  - raspberry
---

> [!WARNING]
> Esta serie quedó incompleta y por ahora no tengo previsto continuarla. Aun así, el contenido publicado puede ser útil.

Esta es la primera parte de una serie de posts en la que explico cómo he montado un cluster de Kubernetes utilizando Raspberry Pi. Aquí presento la configuración del hardware que lo compone.

| Parte                                                              | Título                     |
|--------------------------------------------------------------------|----------------------------|
| **P01**                                                            | **Hardware**               |
| [P02]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-ii" >}})  | Sistema Operativo y Docker |
| [P03]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-iii" >}}) | Cluster K3S                |
| [P04]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-iv" >}})  | Consumo eléctrico          |

## Introducción

Kubernetes es una tecnología de orquestación de contenedores que lleva varios años en el mercado y que cada vez se utiliza más en entornos profesionales. Sin embargo, hasta hace poco no había tenido la ocasión de trabajar directamente con él. Llevo años utilizando Docker de forma intensiva y, como evolución natural, tenía pendiente adentrarme en Kubernetes. Y como creo firmemente que la mejor manera de aprender es practicando, decidí montarme mi propio cluster desde cero.

Valoré la posibilidad de desplegarlo en la nube, pero la cantidad de servicios, peculiaridades y modelos de facturación de los diferentes proveedores me echaba para atrás. Mi objetivo era aprender Kubernetes, no aprender cómo cobran AWS, Google Cloud o Azure. Además, ya había tenido algún susto en el pasado con servicios supuestamente "gratuitos" que no lo eran tanto. Así que opté por montar un cluster *on premise*, aunque implicara un coste inicial más alto y algo más de trabajo manual.

Esta opción me permite centrarme en los conceptos fundamentales sin distraerme con servicios adicionales, y además me da total tranquilidad: si apago el cluster, no estoy generando ningún gasto inesperado.

## Componentes del cluster

El cluster está formado inicialmente por **5 Raspberry Pi 4B de 8 GB de RAM**. Esto se traduce en:

- **20 cores** a 1,5 GHz
- **40 GB de RAM** en total

Cada Raspberry utiliza una tarjeta microSD **Samsung EVO Plus de 32 GB**, que en un primer momento sirve tanto para el sistema operativo como para la persistencia de contenedores. Más adelante, cuando trabaje con volúmenes persistentes, incorporaré un sistema de almacenamiento dedicado.

Para simplificar el montaje y reducir el número de cables, he instalado módulos **HAT PoE** que permiten alimentar las Raspberry directamente mediante el propio cable Ethernet. Así elimino transformadores y cables USB adicionales.

La red está centralizada en un **switch PoE Netgear GS108PP**, con 8 puertos alimentados, lo que me permite conectar y alimentar hasta 7 Raspberry (uno de los puertos se utiliza para conectar el switch al resto de la red).

Todo el conjunto está montado en un **armario rack de 19" y 6U** (modelo Phasak PHP 2106). Su distribución es la siguiente:

- **1U** para una regleta con interruptor
- **1U** para el switch, montado sobre una bandeja
- **2U** para alojar hasta 12 Raspberry Pi
- **2U** libres para futuras ampliaciones

Para colocar las Raspberry de forma ordenada utilicé un proyecto impreso en 3D disponible en Thingiverse. Permite alojarlas en bandejas extraíbles dentro del rack, facilitando muchísimo el mantenimiento. La mayoría de soluciones que había visto en Internet apilan las Raspberry de forma que sustituir una implica desmontarlo todo. Esta, en cambio, resulta muy cómoda y modular.

Antes de dejar el cluster funcionando de forma permanente, quiero medir su consumo eléctrico. Mi idea es integrar la medición con **Home Assistant**, que uso para la domótica en casa, así que aún estoy comparando opciones de enchufes o medidores compatibles.

## Conclusión

La combinación de todos estos componentes da como resultado un cluster:

### Compacto
El armario de 19" ocupa muy poco espacio y se puede colocar prácticamente en cualquier sitio.

### Bien ventilado
El rack incluye dos grandes ventiladores superiores, y cada Raspberry tiene el suyo propio integrado en el HAT PoE. La refrigeración es más que suficiente para dejar el cluster encendido de manera continua sin preocuparme por la temperatura.

### Ordenado
Usar PoE reduce notablemente la cantidad de cables, dejando la instalación limpia y con más tomas libres en la regleta.

### Iluminado
El armario incorpora iluminación LED, lo que facilita las tareas de mantenimiento sin necesidad de iluminar el entorno.

### Extensible
Gracias al soporte impreso en 3D puedo alojar hasta 12 Raspberry Pi ocupando solo 2U. Las 2U libres me permiten:

- añadir más Raspberry Pi
- instalar un SAI
- añadir almacenamiento
- o cualquier otra ampliación futura

## BOM (Bill of Materials)

- 5× [Raspberry Pi 4B 8GB RAM](https://www.tiendatec.es/raspberry-pi/placas-base/1231-raspberry-pi-4-modelo-b-8gb-765756931199.html)
- 5× [Samsung EVO Plus 32GB](https://www.amazon.es/gp/product/B06XFSZGCC/ref=ppx_yo_dt_b_asin_title_o03_s00)
- 5× [HAT PoE](https://www.tiendatec.es/raspberry-pi/hats/757-raspberry-pi-hat-poe-r20-0652508442105.html)
- 1× [Netgear GS108PP](https://www.amazon.es/gp/product/B076BV421P/ref=ppx_yo_dt_b_asin_title_o04_s00)
- 1× [Phasak PHP 2106](https://www.amazon.es/gp/product/B00D5T3TDS/ref=ppx_yo_dt_b_asin_title_o04_s02)
- 1× [Regleta de 8 tomas con interruptor](https://www.amazon.es/gp/product/B00X44HTY4/ref=ppx_yo_dt_b_asin_title_o04_s01)
- 1× [Bandeja para rack](https://www.amazon.es/gp/product/B001PKPK1I/ref=ppx_yo_dt_b_asin_title_o04_s01)
- 1× [Cables de red de 25 cm](https://www.amazon.es/gp/product/B0046UCVFM/ref=ppx_yo_dt_b_asin_title_o03_s01)
- 1× [Tornillos y tuercas para rack](https://www.amazon.es/gp/product/B073WDSPS8/ref=ppx_yo_dt_b_asin_title_o03_s01)
- 1× [Tornillos M2.5 para Raspberry Pi](https://www.amazon.es/gp/product/B081JJ2LRT/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
- 2× Varillas roscadas M4 de 1 m (ferretería)
- 8× Tuercas M4 (ferretería)
