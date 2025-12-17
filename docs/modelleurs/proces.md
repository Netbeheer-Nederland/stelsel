---
title: Proces
parent: Modelleurs
---

*Deze pagina is een placeholder.

# Proces

Werkwijze en kwaliteitsborging in het modelleerteam. [WRSPM](https://www.se-trends.de/en/wrspm-how-please-or-what-is-between-the-world-and-the-system/).

## Rollen

Wie modelleert, wie reviewt?

## Reviewcriteria

Wanneer is iets 'klaar'?

## Overleg en besluitvorming

Synchroon/asynchroon overleg

## Versies

Versioneringspatroon `major`.`minor`:

- `major`: verhoog bij wijzigingen waardoor bestaande data niet eenduidig naar het nieuwe model kan worden gemigreerd, zoals een nieuwe verplichte eigenschap zonder duidelijke standaardwaarde.
- `minor`: verhoog bij alle andere wijzigingen met impact op de data.

De `patch` kennen wij dus niet: wijzigingen zonder impact op data, leiden niet tot een nieuwe versie.
