---
title: Naamgeving
parent: Modelleurs
---

# Naamgeving

Over het algemeen geldt: we gebruiken de Nederlandse spellingsregels en vermijden Engels taalgebruik. Dus geen PascalCase of snake_case, maar gewoon spaties, leestekens en bijzondere karakters.

In het marktdomein zijn we energiedrageragnostisch (`elektriciteit`, `gas` zijn variabelen). Waar mogelijk zijn we netvlakagnostisch (`middenspanning`, `laagspanning` zijn variabelen).

## Entiteiten

Het eerste woord krijgt een hoofdletter. Entiteiten worden aangeduid in het enkelvoud, maar moeten daarnaast een meervoudsvorm hebben volgens het woordenboek. Met andere woorden, het moet om telbare dingen gaan. Dus geen `Suiker`, maar wel `Suikerklontje`.

## Eigenschappen

Eigenschappen beginnen met een kleine letter (tenzij de spellingsregels anders voorschrijven).

## Relaties

Voor relatienamen gebruiken we het patroon zoals beschreven door David Hay in zijn artikel [Relationships Are Not Verbs](https://tdan.com/relationships-are-not-verbs-part-one/26996):

> Elke `entiteitnaam`  
> \[ is | kan zijn ] `relatienaam`  
> \[ één | één of meer \] `gerelateerde entiteit`

Voorbeelden:

* Elke `aansluiting` kan `deel` zijn `van` één `netgebied`.
* Elk `overdrachtspunt` is `in` één `aansluitlocatie`.
* Elke `contractloze zaak` is de `behandeling van` één of meer `contractloze situaties`.

Door enkel het werkwoord _zijn_ te gebruiken, ontstaat de discipline om te beschrijven wat _is_ (in tegenstelling tot wat iets _doet_, zoals in procesmodellen).
