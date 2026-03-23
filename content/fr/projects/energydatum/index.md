---
title: EnergyDatum
summary: Analyse et comparaison des coûts électriques basés sur la consommation réelle
date: 2022-05-26
lastmod: 2025-11-27
tags:
  - Python
  - PySpark
  - HTML
  - Plotly
---

EnergyDatum est une application web conçue pour analyser, calculer et comparer le coût réel de l’électricité dans un foyer à partir des données de consommation historiques. Le système part du fichier CSV fourni par le distributeur d’électricité (avec les relevés horaires du compteur intelligent) et le combine avec les prix horaires du marché régulé publiés par [Red Eléctrica de España](https://api.esios.ree.es).

Lors de la génération du site, EnergyDatum :

- Synthétise les consommations et les regroupe par plages horaires
- Télécharge et traite les prix du marché régulé
- Calcule le coût réel des 12 derniers mois avec le tarif régulé
- (Optionnel) Estime la production solaire à l’aide d’une intégration avec [PVGIS](https://re.jrc.ec.europa.eu/pvg_tools)

Une fois généré, le site est publié comme **site statique** sur [GitHub Pages](https://pages.github.com), mais fonctionne comme une **application dynamique dans le navigateur** : il inclut des graphiques interactifs, des calculs en temps réel et la possibilité d’ajouter des tarifs personnalisés. L’utilisateur peut entrer les prix de n’importe quel fournisseur, et EnergyDatum calcule automatiquement le coût correspondant, en le comparant au tarif régulé ou à d’autres tarifs. Tous les tarifs ajoutés sont enregistrés localement dans le navigateur.

De plus, le système permet de simuler des scénarios d’autoconsommation : production photovoltaïque, coûts avec panneaux et estimation de l’amortissement. Il est même possible d’évaluer différentes configurations (orientation, inclinaison, nombre de panneaux) pour trouver celle qui correspond le mieux aux habitudes de consommation réelles.

EnergyDatum facilite l’évaluation des options de tarifs électriques ou d’autoconsommation pour tous, de manière simple et basée sur des données réelles, en évitant les intuitions ou calculs manuels compliqués.

{{< button url="/energydatum" new_tab="true" size="lg" align="center" icon="hero/sparkles" >}}Voir la démo{{< /button >}}

{{< embed platform="github" resource="dicastro/energydatum" type="repo" >}}