---
title: Proces
parent: Modelleurs
---

# Proces

![Proces]({{ site.baseurl }}/assets/images/proces.drawio.svg)

## Versies

Versioneringspatroon `major`.`minor`:

- `major`: verhoog bij wijzigingen waardoor bestaande data niet eenduidig naar het nieuwe model kan worden gemigreerd, zoals een nieuwe verplichte eigenschap zonder duidelijke standaardwaarde.
- `minor`: verhoog bij alle andere wijzigingen met impact op de data.

De `patch` kennen wij dus niet: wijzigingen zonder impact op data leiden niet tot een nieuwe versie.
