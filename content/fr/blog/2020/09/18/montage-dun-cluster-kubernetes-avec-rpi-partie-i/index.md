---
title: Montage d'un cluster Kubernetes avec Raspberry Pi (partie I)
summary: Première partie d'une série où j'explique comment j'ai monté un cluster Kubernetes en utilisant des Raspberry Pi. Dans cet article, je décris le matériel et l'infrastructure physique utilisés.
date: 2020-09-18
lastmod: 2025-12-03
tags:
  - kubernetes
  - cluster
  - raspberry
---

> [!WARNING]
> Cette série est restée incomplète et je n'ai pour l'instant pas prévu de la poursuivre. Malgré tout, le contenu publié peut être utile.

Ceci est la première partie d'une série d'articles dans laquelle j'explique comment j'ai monté un cluster Kubernetes en utilisant des Raspberry Pi. Ici, je présente la configuration matérielle qui le compose.

| Partie                                                                  | Titre                      |
|-------------------------------------------------------------------------|----------------------------|
| **P01**                                                                 | **Matériel**               |
| [P02]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-ii" >}})  | Système d'exploitation et Docker |
| [P03]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-iii" >}}) | Cluster K3S                |
| [P04]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-iv" >}})  | Consommation électrique    |

## Introduction

Kubernetes est une technologie d'orchestration de conteneurs présente sur le marché depuis plusieurs années et de plus en plus utilisée dans les environnements professionnels. Toutefois, jusqu'à récemment, je n'avais pas encore eu l'occasion de travailler directement avec elle. J'utilise Docker de manière intensive depuis des années et, comme évolution naturelle, je souhaitais me plonger dans Kubernetes. Et puisque je crois fermement que la meilleure manière d'apprendre est de pratiquer, j'ai décidé de monter mon propre cluster depuis zéro.

J'ai envisagé de le déployer dans le cloud, mais la multitude de services, de particularités et de modèles de facturation proposés par les différents fournisseurs m'a découragé. Mon objectif était d'apprendre Kubernetes, pas d'apprendre comment AWS, Google Cloud ou Azure facturent leurs services. De plus, j'avais déjà eu quelques mauvaises surprises avec des services soi-disant "gratuits" qui ne l'étaient pas vraiment. J'ai donc choisi de monter un cluster *on-premise*, même si cela impliquait un coût initial plus élevé et un peu plus de travail manuel.

Cette option me permet de me concentrer sur les concepts fondamentaux sans être distrait par des services supplémentaires, et elle m'offre une tranquillité d'esprit totale : si j'éteins le cluster, je ne génère aucune dépense imprévue.

## Composants du cluster

Le cluster est initialement composé de **5 Raspberry Pi 4B avec 8 Go de RAM** chacun. Cela représente :

- **20 cœurs** à 1,5 GHz
- **40 Go de RAM** au total

Chaque Raspberry utilise une carte microSD **Samsung EVO Plus de 32 Go**, qui sert dans un premier temps à la fois pour le système d'exploitation et pour la persistance des conteneurs. Plus tard, lorsque je travaillerai avec des volumes persistants, j'ajouterai un système de stockage dédié.

Pour simplifier le montage et réduire le nombre de câbles, j'ai installé des modules **PoE HAT**, qui permettent d'alimenter les Raspberry directement via le câble Ethernet. Cela permet d'éliminer les adaptateurs et câbles USB supplémentaires.

Le réseau est centralisé autour d'un **switch PoE Netgear GS108PP**, doté de 8 ports alimentés, ce qui me permet de connecter et d'alimenter jusqu'à 7 Raspberry Pi (un des ports sert à relier le switch au reste du réseau).

L'ensemble est monté dans une **baie rack 19" de 6U** (modèle Phasak PHP 2106). Sa répartition est la suivante :

- **1U** pour une multiprise avec interrupteur
- **1U** pour le switch, monté sur une étagère
- **2U** pour accueillir jusqu'à 12 Raspberry Pi
- **2U** libres pour de futures extensions

Pour organiser proprement les Raspberry, j'ai utilisé un projet imprimé en 3D disponible sur Thingiverse. Il permet de les installer sur des plateaux amovibles à l'intérieur du rack, ce qui facilite énormément la maintenance. La plupart des solutions que j'avais vues sur Internet empilent les Raspberry d'une manière qui oblige à tout démonter pour en remplacer une. Celle-ci, au contraire, est confortable et modulaire.

Avant de laisser le cluster fonctionner en continu, je souhaite mesurer sa consommation électrique. Mon intention est d'intégrer cette mesure dans **Home Assistant**, que j'utilise pour la domotique à la maison. Je compare donc encore différentes prises ou compteurs compatibles.

## Conclusion

La combinaison de tous ces composants donne un cluster :

### Compact
La baie 19" occupe très peu d'espace et peut être placée pratiquement n'importe où.

### Bien ventilé
Le rack inclut deux grands ventilateurs supérieurs, et chaque Raspberry possède son propre ventilateur intégré au PoE HAT. Le refroidissement est largement suffisant pour laisser le cluster fonctionner en continu sans me soucier de la température.

### Ordonné
L'utilisation du PoE réduit considérablement la quantité de câbles, offrant une installation propre avec davantage de prises disponibles sur la multiprise.

### Éclairé
La baie intègre un éclairage LED, ce qui facilite les tâches de maintenance sans devoir éclairer toute la pièce.

### Extensible
Grâce au support imprimé en 3D, je peux accueillir jusqu'à 12 Raspberry Pi en n'utilisant que 2U. Les 2U restants me permettent de :

- ajouter d'autres Raspberry Pi
- installer un onduleur (UPS)
- ajouter du stockage
- ou toute autre extension future

## BOM (Bill of Materials)

- 5× [Raspberry Pi 4B 8GB RAM](https://www.tiendatec.es/raspberry-pi/placas-base/1231-raspberry-pi-4-modelo-b-8gb-765756931199.html)
- 5× [Samsung EVO Plus 32GB](https://www.amazon.es/gp/product/B06XFSZGCC/ref=ppx_yo_dt_b_asin_title_o03_s00)
- 5× [PoE HAT](https://www.tiendatec.es/raspberry-pi/hats/757-raspberry-pi-hat-poe-r20-0652508442105.html)
- 1× [Netgear GS108PP](https://www.amazon.es/gp/product/B076BV421P/ref=ppx_yo_dt_b_asin_title_o04_s00)
- 1× [Phasak PHP 2106](https://www.amazon.es/gp/product/B00D5T3TDS/ref=ppx_yo_dt_b_asin_title_o04_s02)
- 1× [Multiprise 8 prises avec interrupteur](https://www.amazon.es/gp/product/B00X44HTY4/ref=ppx_yo_dt_b_asin_title_o04_s01)
- 1× [Étagère pour rack](https://www.amazon.es/gp/product/B001PKPK1I/ref=ppx_yo_dt_b_asin_title_o04_s01)
- 1× [Câbles réseau 25 cm](https://www.amazon.es/gp/product/B0046UCVFM/ref=ppx_yo_dt_b_asin_title_o03_s01)
- 1× [Vis et écrous pour rack](https://www.amazon.es/gp/product/B073WDSPS8/ref=ppx_yo_dt_b_asin_title_o03_s01)
- 1× [Vis M2.5 pour Raspberry Pi](https://www.amazon.es/gp/product/B081JJ2LRT/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
- 2× Tiges filetées M4 de 1 m (quincaillerie)
- 8× Écrous M4 (quincaillerie)  
