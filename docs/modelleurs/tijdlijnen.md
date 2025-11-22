---
title: Tijdlijnen
parent: Modelleurs
---

# Tijdlijnen

Een conceptueel informatiemodel beschrijft de toestand van de wereld op abstract niveau: welke objecttypen er zijn, met welke eigenschappen en relaties. Het model representeert de wereld zoals die bedoeld of waargenomen wordt, maar bevat geen informatie over veranderingen in de tijd, versies of individuele voorkomens.

Toch is tijd vaak wél een essentieel onderdeel van de betekenis van objecten. Denk aan geldigheid, registratie of bestaansduur. Daarom nemen we in het conceptueel model expliciete tijdlijnmarkeringen op. Die geven aan welke soorten temporele informatie op een entiteit van toepassing zijn. In het logisch model worden deze tijdlijnen vervolgens uitgewerkt in attributen en versiestructuren. We volgen hierbij [NEN 3610](https://www.geonovum.nl/geo-standaarden/nen-3610-basismodel-voor-informatiemodellen) §8.3, waarin drie tijdlijnen worden onderscheiden. Wij voegen daar onze eigen `tijdlijn effectuering` aan toe (zie [artikel 2.1.8 van de Informatiecode elektriciteit en gas](https://wetten.overheid.nl/jci1.3:c:BWBR0037934&hoofdstuk=2&paragraaf=2.1&artikel=2.1.8&z=2025-01-01&g=2025-01-01)).

Tijdlijnmarkeringen zijn alleen van toepassing op *enduranten*: entiteiten die op meerdere tijdstippen kunnen bestaan en daarbij hun identiteit behouden (zoals een gebouw of organisatie). *Perduranten* (zoals gebeurtenissen of processen) bestaan uit meerdere fasen in de tijd en zijn niet als geheel aanwezig op één moment. Bij perduranten maakt tijd deel uit van de definitie van het objecttype zelf (bijvoorbeeld via `tijdstip`, `begintijd`, of `duur`). Tijdseigenschappen horen bij dit type entiteiten dus wel thuis in het conceptueel model.

De markering gebeurt als volgt:

- In draw.io: `⏲ tijdlijn <type>` (of `⏲ levensduur`) na de lijst met eigenschappen.
- In LinkML: `tijdlijn_<type>: true` (of `levensduur: true`) binnen `annotations`.

Deze markeringen maken de temporele semantiek van een entiteit expliciet, al in de conceptuele fase. Dat helpt om consistentie te waarborgen in latere uitwerkingen, bijvoorbeeld versiemodellering in het gegevensmodel:

![Tijdlijnen in een gegevensmodel]({{ site.baseurl }}/assets/images/tijdlijnen.drawio.svg)

## Tijdlijn geldigheid

Dit betreft veranderingen in de (doorgaans fysieke) werkelijkheid. De gemarkeerde entiteit krijgt versies in het logisch model, met de eigenschappen:

- `begin geldigheid`
- `eind geldigheid`
- `versie` (optioneel)

## Tijdlijn registratie

Dit betreft veranderingen in het informatiesysteem (wanneer iets is geregistreerd of verwijderd). De gemarkeerde entiteit krijgt versies in het logisch model, met de eigenschappen:

- `tijdstip registratie`
- `eind registratie`
- `versie` (optioneel)

Registratietijd is het moment waarop informatie in een systeem bekend is, en kan verschillen van de feitelijke geldigheid in de werkelijkheid.

## Tijdlijn effectuering

Dit betreft momenten waarop informatie formeel van kracht wordt (bijvoorbeeld in de energiemarkt). De gemarkeerde entiteit krijgt versies in het logisch model, met de eigenschappen:

- `tijdstip effectuering`  
- `eind effectuering`  
- `versie` (optioneel)

## Levensduur

Dit betreft het moment van ontstaan en vergaan in de (doorgaans fysieke) werkelijkheid. Standaard eigenschappen in het logisch model:

- `object begintijd`  
- `object eindtijd`  

Aan de markering mogen aliassen worden toegevoegd, voor gebruik in logische modellen. Bijvoorbeeld `Mens` mag in draw.io worden gemarkeerd met `⏲ levensduur (moment van geboorte, moment van overlijden)`.

Als een entiteit ook is gemarkeerd met `tijdlijn geldigheid`, dan zijn `object begintijd` en `object eindtijd` doorgaans gelijk aan respectievelijk de eerste `begin geldigheid` en de laatste `eind geldigheid`.
