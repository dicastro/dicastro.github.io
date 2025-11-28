---
title: EnergyDatum
summary: Análisis y comparación de costes eléctricos basados en consumo real
date: 2022-05-26
lastmod: 2025-11-27
tags:
  - Python
  - PySpark
  - HTML
  - Plotly
---

EnergyDatum es una aplicación web diseñada para analizar, calcular y comparar el coste real de la electricidad en un hogar a partir de datos históricos de consumo. El sistema parte del fichero CSV proporcionado por la distribuidora eléctrica (con las lecturas horarias del contador inteligente) y lo combina con los precios horarios del mercado regulado publicados por [Red Eléctrica de España](https://api.esios.ree.es).

Durante el proceso de generación del sitio, EnergyDatum:

- Sintetiza los consumos y los agrupa por franjas
- Descarga y procesa los precios del mercado regulado
- Calcula el coste real de los últimos 12 meses en tarifa regulada
- (Opcional) Estima la producción de una instalación solar mediante una integración con [PVGIS](https://re.jrc.ec.europa.eu/pvg_tools) 

Una vez generada, la web se publica como **sitio estático** en [GitHub Pages](https://pages.github.com), pero funciona como una **aplicación dinámica en el navegador**: incluye gráficos interactivos, cálculos en tiempo real y la posibilidad de añadir tarifas personalizadas. El usuario puede introducir los precios de cualquier comercializadora y EnergyDatum calcula automáticamente el coste correspondiente, comparándolo con la tarifa regulada o con otras tarifas. Todas las tarifas añadidas se guardan localmente en el navegador.

Además, el sistema permite simular escenarios de autoconsumo: producción fotovoltaica, costes con paneles y estimación de amortización. Incluso es posible evaluar distintas configuraciones (orientación, inclinación, número de paneles) para encontrar la que mejor encaja con los hábitos de consumo reales.

EnergyDatum facilita que cualquier persona pueda evaluar opciones de tarifas eléctricas o autoconsumo de forma sencilla y basada en datos reales, evitando intuiciones o cálculos manuales difíciles de mantener.

{{< button url="/energydatum" new_tab="true" size="lg" align="center" icon="hero/sparkles" >}}Ver demo{{< /button >}}

{{< embed platform="github" resource="dicastro/energydatum" type="repo" >}}