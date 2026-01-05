---
title: Legenda
nav_order: 4
---

# Legenda
{: .no_toc }

## Inhoud
{: .no_toc .text-delta }
1. TOC
{:toc}

De conceptuele informatiemodellen op deze website gebruiken eenvoudige diagrammen om te laten zien _welke begrippen er zijn_ en _hoe die met elkaar samenhangen_. Hieronder leggen we de belangrijkste elementen uit.

## Entiteiten

Een **entiteit** is iets uit de werkelijkheid waarover we informatie vastleggen, bijvoorbeeld een aansluiting, een meter of een klant. In het diagram zie je entiteiten als **rechthoeken** met een naam erin.

![Entiteit]({{ site.baseurl }}/assets/images/legenda1.drawio.svg)

## Eigenschappen

Elke entiteit heeft eigenschappen: kenmerken die beschrijven wat iets is of hoe het zich gedraagt. Die staan in het model onder de entiteitsnaam. Voorbeeld: een `Aansluiting` heeft een `EAN-code` en een `energiedrager` (elektriciteit, gas of waterstof).

![Eigenschappen]({{ site.baseurl }}/assets/images/legenda2.drawio.svg)

Elke eigenschap begint met een symbool:

- `#` identificerend
- `●` altijd bekend
- `○` niet altijd bekend

Hieruit kun je aflezen dat aansluitingen van elkaar worden onderscheiden middels hun `EAN-code`; dat een aansluiting zonder `energiedrager` geen aansluiting is; terwijl een aansluiting zonder `weekmax` nog steeds een aansluiting kan zijn (want deze eigenschap komt alleen voor bij grote elektriciteitsaansluitingen).

Als een eigenschap begint met `/` dan is deze afleidbaar uit een ander gegeven in het model. In dit geval is de `grootte` van de aansluiting afleidbaar uit de `aansluitcapaciteit` van het gerelateerde `Overdrachtspunt` (niet afgebeeld).

Een doorgestreepte eigenschap, zoals `weekmax`, zal in een toekomstige versie vervallen.

Een eigenschap die eindigt met `[n]` kan meerdere waarden bevatten.

## Relaties

Entiteiten hangen vaak met elkaar samen. Zo liggen `Aansluitingen` in een `Netgebied`. Dat zie je als een lijn tussen twee entiteiten, met een naam erbij.

![Relaties]({{ site.baseurl }}/assets/images/legenda3.drawio.svg)

De positie van het label laat de richting van de relatie zien: een `Aansluiting` is `deel van` een `Netgebied`.

## Multipliciteit

De kraaienpootnotatie gebruikt symbolen om aan te geven hoeveel elementen aan elke kant van de relatie voorkomen. Daarbij staat een cirkel voor 0, een streep voor 1 en een driepoot voor veel. In paren geven zij het minimum en maximum aan:

- Elke `Aansluiting` kan deel zijn van één `Netgebied`
- Elk `Netgebeid` kan een groepering zijn van één of meer `Aansluitingen`
- Elke `Overdrachtspunt` moet deel zijn van exact één `Aansluiting`
- Elke `Aansluiting` moet de groepering zijn van één of meer `Overdrachtspunten`

## OF-bogen

Een boog met daarop het woord `OF` geeft aan dat óf de ene óf de andere relatie geldt, maar nooit beide. Zo is een `Overdrachtspunt` óf deel van een `Aansluiting` óf deel van een `Netkoppeling` maar nooit deel van beide.

![OF-bogen]({{ site.baseurl }}/assets/images/legenda4.drawio.svg)

## Overerving

Een entiteit die wordt omsloten door een andere entiteit is daarvan een specialisatie en overerft daarom alle eigenschappen en relaties. `Spanningsmeettransformator` en `Stroommeettransformator` zijn beide voorbeelden van `Meettransformator` en overerven daarom beide de eigenschappen `serienummer` en `fabrikant`. Maar de eigenschappen `thermisch grensvermogen` en `overstroomfactor` zijn dan weer uniek per type meettransformator.

![Overerving]({{ site.baseurl }}/assets/images/legenda5.drawio.svg)

## Tijdsaspecten

Sommige gegevens veranderen in de tijd. Denk aan een verzwaring van de aansluiting of adreswijziging. Als het van belang is om het verleden te reconstrueren of op de toekomst te anticiperen, dan zie je annotaties als:

- `⏲ tijdlijn geldigheid`
- `⏲ tijdlijn registratie`
- `⏲ tijdlijn effectuering`
- `⏲ levensduur`

Deze geven aan in welke periode een feit geldig was in de werkelijkheid (`tijdlijn geldigheid`), wanneer deze bekend was in het systeem (`tijdlijn registratie`) en wanneer deze van kracht was voor de energiemarkt (`tijdlijn effectuering`). De `levensduur` geeft het moment van ontstaan en vergaan van een object aan.

Voor meer informatie, zie de pagina over [Tijdlijnen](modelleurs/tijdlijnen).

## Kleuren

Elke entiteit heeft een kleur die de relatie naar [NBility](https://nbility-model.github.io/) weergeeft.

Zo behoort de `Aangeslotene` bij **Klant**, de `Aansluiting` en het `Overdrachtspunt` bij **Aansluiting** (binnen de **Energiemarkt**) en het `Primair deel meetinrichting` bij **Netcomponent** (binnen het **Energienet**).

![Kleuren]({{ site.baseurl }}/assets/images/legenda6.drawio.svg)
