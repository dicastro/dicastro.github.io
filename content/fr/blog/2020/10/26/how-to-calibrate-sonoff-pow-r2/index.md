---
slug: comment-calibrer-un-sonoff-pow-r2
title: Comment calibrer un Sonoff Pow R2
summary: Dans cet article j'explique comment calibrer un Sonoff Pow R2 afin d'améliorer la précision de ses mesures
date: 2020-10-26
tags:
  - cluster
  - sonoff
  - esphome
---

Dans [un autre article]({{< ref "building-kubernetes-cluster-with-rpi-part-iv" >}}#comment-mesurer-la-consommation-électrique), j'ai déjà expliqué comment je mesurais la consommation d'un cluster de Raspberry Pi en utilisant un Sonoff Pow R2. Il est important de calibrer cet appareil avant de l'utiliser afin que ses mesures soient les plus précises possible.

Dans ce post, je vais expliquer comment le calibrer. Pour cela, il est nécessaire de disposer d'un wattmètre. J'ai utilisé un [ZHURUI PR10-C EU16A](https://www.amazon.es/gp/product/B06VWMS7QS/ref=ppx_yo_dt_b_asin_title_o03_s00), qui n'est pas très cher et fonctionne assez bien. Cet appareil permet d'afficher simultanément la tension, le courant et la puissance consommée. Ce dernier point peut sembler anodin, mais plus loin vous verrez comment ce détail facilite grandement le processus de calibration.

Pour effectuer la calibration, il suffit de connecter le Zhurui à une prise de courant et le Sonoff au Zhurui. Le processus consiste à brancher sur le Sonoff différents appareils ayant des consommations variées et à noter à la fois les mesures du Zhurui et celles du Sonoff.

Dans mon cas, j'ai utilisé les appareils suivants :

- Une lampe de bureau avec une ampoule halogène (11W)
- Une lampe de bureau avec une ampoule incandescente (60W)
- Un aspirateur (jusqu'à 800W)
- Un fer à repasser (2000W)

J'ai connecté chaque appareil un à un sur le Sonoff, lui-même relié au wattmètre, et j'ai noté les mesures des deux appareils. Pour relever les mesures du Sonoff, j'ai utilisé un ordinateur portable depuis lequel j'ai accédé à la console d'ESPHome. J'ai placé l'ordinateur à côté de la prise où se trouvait le Zhurui, afin qu'une seule photo puisse capturer les lectures des deux appareils.

C'est à cette étape que l'on apprécie que le wattmètre affiche simultanément toutes les valeurs intéressantes, car une seule photo fournit toutes les informations nécessaires. Voici un exemple des mesures obtenues en connectant l'ampoule incandescente :

![Exemple de capture de consommation d'une ampoule incandescente de 60W](./resources/measure_capture_sample.jpg)

Une fois qu'une capture a été réalisée pour chacun des appareils, vous disposez de toutes les informations nécessaires pour calibrer le Sonoff. Grâce à la conception d'ESPHome, cette étape est très simple. Il suffit de configurer quelques filtres dans lesquels on note la mesure du wattmètre ainsi que celle du Sonoff.

Là où vous aviez auparavant quelque chose comme ceci :

```yaml
# Current sensor
current:
  name: "RPI Cluster Current"
  icon: mdi:current-ac
  unit_of_measurement: A
  accuracy_decimals: 3
```

Vous aurez maintenant quelque chose comme ceci :

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

> Dans [cet article]({{< ref "building-kubernetes-cluster-with-rpi-part-iv" >}}#comment-générer-le-firmware), vous pouvez voir le code complet du Sonoff

Et quelque chose de similaire pour le capteur de puissance :

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

Et pour le capteur de tension :

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

ESPHome effectue une régression linéaire à partir des valeurs précédentes (en utilisant une fonction d'ajustement aux moindres carrés) pour « corriger » les mesures effectuées par le Sonoff.

> Je ne l'ai pas mentionné jusqu'à présent, mais il faut également effectuer une capture des mesures sans aucun appareil connecté au Sonoff.

## Conclusion

Comme vous pouvez le voir, la calibration d'un appareil Sonoff est très simple. Plus le wattmètre externe utilisé est précis, meilleure sera la calibration du Sonoff. Il est important d'utiliser des appareils ayant des consommations variées couvrant l'ensemble de la plage, afin que la calibration soit la plus fidèle possible à la réalité. Si vous achetez plusieurs appareils Sonoff, chacun doit être calibré individuellement.