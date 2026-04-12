---
title: Basistypen
parent: Modelleurs
---

## Basistypen

In dit stelsel wordt gewerkt met een eigen set conceptuele basistypen. Deze basistypen beschrijven *wat informatie betekent* en maken deel uit van het conceptuele informatiemodel (_Requirements_‑laag, R, volgens het WRSPM‑model).

De basistypen doen uitdrukkelijk geen uitspraken over technische realisatie. Zij leggen niet vast dat iets een `string`, `float`, `double` of ander technisch datatype moet zijn. Dergelijke keuzes horen thuis in de
_System Specification_‑laag (S) en kunnen per toepassing verschillen.

Door betekenis en techniek te scheiden:

- blijft het conceptuele model stabiel en technologie‑onafhankelijk;
- kunnen dezelfde begrippen in verschillende systemen verschillend worden geïmplementeerd;
- ontstaat ruimte voor preciezere technische keuzes zonder het model aan te passen.

### Voorbeeld

Het basistype **Reëel getal** beschrijft een *continue, fysiek meetbare hoeveelheid*. In een concrete implementatie kan dit bijvoorbeeld worden gerepresenteerd als:

- een `float`,
- een `double`,
- een `integer` als benadering omwille van prestatieoptimalisatie onder geaccepteerd verlies van precisie.

Het basistype **Tijdsduur** beschrijft de *lengte van een tijdsinterval*. Afhankelijk van de toepassing kan dit technisch worden vastgelegd als:

- een tekenreeks conform een ISO‑standaard (bijv. `PT15M` voor 15 minuten),
- een geheel getal dat een aantal seconden, milliseconden of microseconden telt,
- of een gespecialiseerd tijdsduurtype in een programmeertaal of databank.

Al deze representaties zijn technisch gelijkwaardig, zolang zij dezelfde conceptuele betekenis correct uitdrukken.

## Overzicht van de basistypen

### Tekst

Aanduiding bedoeld voor mensen, zonder vaste structuur of betekenis.

Gebruik voor:

- namen
- omschrijvingen
- toelichtingen
- vrije invoer in natuurlijke taal

### Code

Symbolische aanduiding met een vastgelegde betekenis.

Gebruik voor:

- identificaties (bijv. EAN-code, registratienummer)
- adresserende waarden (telefoonnummer, e-mailadres)
- type- en modelaanduidingen
- classificaties die niet als waardelijsten zijn vastgelegd

Een code is niet-talige informatie: de betekenis ligt vast door afspraak en is niet afhankelijk van interpretatie.

### Geheel getal

Telbare hoeveelheid zonder decimalen.

Gebruik voor:

- aantallen
- ordinalen
- tellingen

### Reëel getal

Continue, fysiek meetbare hoeveelheid.

Gebruik voor:

- vermogen
- spanning
- lengte
- volume
- snelheid

### Decimaal getal

Exact afgesproken numerieke waarde.

Gebruik voor:

- geldbedragen
- tarieven
- contractuele percentages

Dit type wordt gebruikt wanneer afronding of benadering niet is toegestaan.

### Waarheidswaarde

Anduiding die één van twee elkaar uitsluitende waarden kan aannemen.

Gebruik voor:

- ja/nee-indicatoren
- flags
- binaire eigenschappen

### Datum

Kalenderdatum zonder tijdsaanduiding.

Gebruik voor:

- ingangsdatum
- geboortedatum
- registratiedatum

### Tijdstip

Exacte aanduiding van datum en tijd.

Gebruik voor:

- meetmomenten
- logtijdstippen
- gebeurtenissen

### Tijdsduur

Lengte van een tijdsinterval.

Gebruik voor:

- looptijden
- geldigheidsduren
- vertragingen
