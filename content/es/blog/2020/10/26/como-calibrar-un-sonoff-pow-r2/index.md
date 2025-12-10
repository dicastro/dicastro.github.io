---
title: Cómo calibrar un Sonoff Pow R2
summary: En este post explico cómo calibrar un Sonoff Pow R2 para que sea más preciso en sus mediciones
date: 2020-10-26
lastmod: 2025-12-09
tags:
  - cluster
  - sonoff
  - esphome
---

En [otro post]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-iv" >}}#cómo-medir-el-consumo-eléctrico) ya expliqué cómo medía el consumo de un cluster de Raspberry Pi mediante el uso de un Sonoff Pow R2. Es importante calibrar este dispositivo antes de utilizarlo para que sus mediciones sean lo más precisas posibles.

En este post voy a explicar cómo calibrarlo. Para ello será necesario disponer de un medidor de corriente. Yo he utilizado un [ZHURUI PR10-C EU16A](https://www.amazon.es/gp/product/B06VWMS7QS/ref=ppx_yo_dt_b_asin_title_o03_s00) que no es muy caro y funciona bastante bien. Este dispositivo permite visualizar al mismo tiempo el voltaje, la corriente y la potencia consumidas. Esto último puede parecer una nimiedad, pero más adelante se mostrará cómo este detalle facilita mucho el proceso de calibración.

Para realizar la calibración se conecta el Zhurui a una toma de corriente y el Sonoff al primero. Este proceso consiste en ir conectado al Sonoff diversos dispositivos con diferentes consumos e ir anotando tanto las mediciones del Zhurui como las del Sonoff.

En mi caso he utilizado los siguientes dispositivos:

- Un flexo con un halógeno (11W)
- Un flexo con una bombilla incandescente (60W)
- Una aspiradora (máximo 800W)
- Una plancha (2000W)

He ido conectando uno a uno cada uno de los dispositivos anteriores al Sonoff, que a su vez está conectado al medidor de consumo, y he ido anotando las mediciones de ambos. Para tomar las medidas del Sonoff, he utilizado un portátil desde el cual he accedido a la consola del ESPHome. Este portátil lo he colocado junto a la toma de corriente donde se encuentra el Zhurui, de tal forma que mediante una fotografía puedo capturar las lecturas de ambos dispositivos.

En este paso es donde se agradece que el medidor de corriente muestre en pantalla al mismo tiempo todos los valores interesantes, ya que con una única instantánea se obtiene toda la información necesaria. Aquí se puede ver un ejemplo de las lecturas obtenidas al conectar la bombilla incandescente:

![Ejemplo de captura de consumo de una bombilla incandescente de 60W](./resources/measure_capture_sample.jpg)

Una vez se ha realizado una captura para cada uno de los dispositivos se dispone de toda la información necesaria para calibrar el Sonoff. Por cómo está diseñado ESPHome este paso es muy sencillo. Simplemente hay que configurar unos filtros en los que se anota la medida del medidor de corriente junto con la del sonoff.

Donde antes había algo como lo siguiente:

```yaml
# Current sensor
current:
  name: "RPI Cluster Current"
  icon: mdi:current-ac
  unit_of_measurement: A
  accuracy_decimals: 3
```

Ahora habrá algo parecido a esto:

```yaml
# Current sensor
current:
  name: "RPI Cluster Current"
  icon: mdi:current-ac
  unit_of_measurement: A
  accuracy_decimals: 3
  filters:
    # Map from sensor -> measured value
    - calibrate_linear:
        - 0.0 -> 0.010
        - 0.15855 -> 0.153
        - 0.25773 -> 0.265
        - 2.45250 -> 2.519
        - 3.02082 -> 3.066
        - 3.41044 -> 3.464
        - 8.73604 -> 8.837
    # Make everything below 0.01A appear as just 0A.
    # Furthermore it corrects 0.01A for the power usage of the sonoff plus the led of the multi-socket.
    - lambda: if (x < (0.01 - 0.01)) return 0; else return (x - 0.01);
```

> En [este post]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-iv" >}}#cómo-obtenemos-el-binario-con-el-código-a-flashear) se puede ver el código completo del Sonoff

Y algo parecido para el sensor de potencia:

```yaml
# Power sensor
power:
  name: "RPI Cluster Power"
  icon: mdi:gauge
  unit_of_measurement: W
  accuracy_decimals: 0
  id: rpiclusterpower
  filters:
    # Map from sensor -> measured value
    - calibrate_linear:
        - 0.0 -> 1.19
        - 15.33994 -> 16.98
        - 57.21655 -> 59.42
        - 261.44540 -> 272.0
        - 459.74557 -> 471.6
        - 741.94073 -> 761.0
        - 1905.09253 -> 1957.0
    # Make everything below 2W appear as just 0W.
    # Furthermore it corrects 1.19W for the power usage of the sonoff plus the led of the multi-socket.
    - lambda: if (x < (2 + 1.19)) return 0; else return (x - 1.19);
```

Y para el de voltaje:

```yaml
# Voltage sensor
voltage:
  name: "RPI Cluster Voltage"
  icon: mdi:flash
  unit_of_measurement: V
  accuracy_decimals: 1
  filters:
    # Map from sensor -> measured value
    - calibrate_linear:
        - 0.0 -> 0.0
        - 226.84409 -> 225.6
        - 225.37788 -> 224.9
        - 225.54657 -> 224.6
        - 224.83321 -> 224.5
        - 224.59578 -> 224.0
        - 224.23352 -> 223.9
```

ESPHome realiza una regresión lineal en base a los valores anteriores (utilizando una función de ajuste de mínimos cuadrados) para "corregir" las mediciones realizadas por el Sonoff.

> No lo he mencionado hasta ahora, pero también hay que realizar una captura de las medidas sin ningún dispositivo conectado al Sonoff.

## Conclusión

Como se puede ver la calibración de un dispositivo Sonoff es muy sencilla. Cuanto más preciso sea el medidor de corriente externo utilizado, mejor será la calibración del Sonoff. Es importante utilizar dispositivos con consumos diversos que cubran todo el espectro para que la calibración se ajuste lo máximo a la realidad. En el caso de adquirir varios Sonoff, cada uno debería ser calibrado de forma independiente.