---
title: EnergyDatum
summary: Analysis and comparison of electricity costs based on actual consumption
date: 2022-05-26
lastmod: 2025-11-27
tags:
  - Python
  - PySpark
  - HTML
  - Plotly
---

EnergyDatum is a web application designed to analyze, calculate, and compare the real cost of electricity in a household using historical consumption data. The system starts from the CSV file provided by the electricity distributor (with hourly smart meter readings) and combines it with hourly regulated market prices published by [Red Eléctrica de España](https://api.esios.ree.es).

During site generation, EnergyDatum:

- Summarizes consumption and groups it by time slots
- Downloads and processes regulated market prices
- Calculates the actual cost for the last 12 months under the regulated tariff
- (Optional) Estimates solar production using an integration with [PVGIS](https://re.jrc.ec.europa.eu/pvg_tools)

Once generated, the website is published as a **static site** on [GitHub Pages](https://pages.github.com), but functions as a **dynamic application in the browser**: it includes interactive charts, real-time calculations, and the possibility to add custom tariffs. Users can enter prices from any electricity provider, and EnergyDatum automatically calculates the corresponding cost, comparing it with the regulated tariff or other tariffs. All added tariffs are stored locally in the browser.

Additionally, the system allows simulating self-consumption scenarios: photovoltaic production, costs with panels, and amortization estimates. It is even possible to evaluate different configurations (orientation, tilt, number of panels) to find the one that best fits actual consumption habits.

EnergyDatum makes it easy for anyone to evaluate electricity tariffs or self-consumption options based on real data, avoiding guesswork or difficult manual calculations.

{{< button url="/energydatum" new_tab="true" size="lg" align="center" icon="hero/sparkles" >}}View demo{{< /button >}}

{{< embed platform="github" resource="dicastro/energydatum" type="repo" >}}