---
title: Proces
parent: Modelleurs
---

# Proces

![Proces]({{ site.baseurl }}/assets/images/proces.drawio.svg)

## Opmerkingen per stap

* **Voer desk research uit**. Dit houdt in:
  * Inlezen op bestaande modellen en relevante regelgeving en standaarden
  * Eerste vragen aan domeinexperts voorbereiden

* **Dien usecase in en verfijn**: Productmanager levert waar mogelijk aan:
  * waarde en noodzaak van de usecase
  * contactgegevens van domeinexperts
  * gewenste opleverdatum

* **Maak en review model**: Er moet minimaal een peerreview zijn geweest binnen Team Semantiek voordat het model ter beoordeling wordt voorgelegd aan anderen.

* **Publiceer model**: Zodra de productmanager het model bouwklaar acht, wordt deze gepubliceerd. De beoordelingen door data-eigenaren mogen eventueel parallel plaatsvinden (op risico van de productmanager) en worden achteraf vermeld bij het model (met enkel organisatie, afdeling en functietitel, dus zonder persoonsnaam).

* **Beoordeel model**: De data-eigenaren worden per netbeheerder benoemd door de betreffende Chief Data Officer (CDO) en zijn vindbaar via het Data Office of vergelijkbare afdeling. Team Semantiek kan faciliteren bij de communicatie met data-eigenaren.

## Versies

Versioneringspatroon `major`.`minor`:

* `major`: verhoog bij wijzigingen waardoor bestaande data niet eenduidig naar het nieuwe model kan worden gemigreerd, zoals een nieuwe verplichte eigenschap zonder duidelijke standaardwaarde.
* `minor`: verhoog bij alle andere wijzigingen met impact op de data.

De `patch` kennen wij dus niet: wijzigingen zonder impact op data leiden niet tot een nieuwe versie.
