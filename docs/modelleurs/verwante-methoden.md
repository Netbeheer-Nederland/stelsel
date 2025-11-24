---
title: Verwante methoden
parent: Modelleurs
---

{: .note }
Kijk gerust rond! Aan deze website wordt momenteel nog gewerkt.

# Verwante methoden

Conceptueel informatiemodelleren richt zich op het gestructureerd beschrijven van betekenisvolle objecten, relaties en regels uit de werkelijkheid. Deze modellen vormen geen blauwdruk van de data zelf, maar van de concepten waarover informatie wordt (of kan worden) vastgelegd.

Toch zijn er vragen die conceptuele modellen vaak niet volledig beantwoorden: Waarom zijn bepaalde concepten relevant? Welke regels bepalen geldigheid of consistentie? Wie is waarvoor verantwoordelijk? Voor zulke vragen bestaan er aanvullende methoden, formeel of semi-formeel van aard. Conceptueel informatiemodelleren wordt sterker als het wordt ondersteund door methoden die doelen, regels of verantwoordelijkheden expliciteren. KAOS en i\* maken doelen en afhankelijkheden zichtbaar, Ampersand borgt consistentie via regels, ontologieën bieden semantische precisie, en BPMN/DMN verbinden informatie aan proces en besluitvorming. Afhankelijk van je modelleervraag kan het zinvol zijn een van deze methoden nader te verkennen.

Deze methoden vormen geen vervanging van informatiemodellering, maar bieden aanvullende perspectieven.

## KAOS

**KAOS** is een formele methode binnen het domein van Goal-Oriented Requirements Engineering (GORE). Ze ondersteunt het modelleren van doelen en het afleiden van systeemvereisten via hiërarchieën van doelen, obstakels en agenten.

Doelen zijn doorgaans geformuleerd als toestanden van objecten of relaties die gewenst zijn in de werkelijkheid, bijvoorbeeld uitgedrukt in temporele logica. Het objectmodel in KAOS (feitelijk een conceptueel informatiemodel) specificeert de semantische context waarin deze doelen betekenis krijgen.

- **Relevantie voor informatiemodellering**: Verbindt informatiemodellen expliciet aan doelen; verklaart de aanwezigheid van objecten en attributen op grond van functionele noodzaak.
- **Toepassing**: Vroege fasen van systeemontwikkeling, beleidsmatige contexten, traceerbaarheid van vereisten.
- **Tooling**: [Objectiver Studio](https://www.objectiver.com/)
- **Meer info**: [KAOS overview paper](https://www.researchgate.net/publication/220869153_A_Goal-Oriented_Requirements_Engineering_Framework)

## iStar

**iStar** (i\*) is eveneens een GORE-methodiek, maar focust op actoren, hun doelen en afhankelijkheden. Actoren kunnen verantwoordelijk zijn voor taken, middelen leveren, of ondersteuning nodig hebben van anderen.

Voor conceptueel informatiemodelleren biedt iStar een manier om verantwoordelijkheden te koppelen aan delen van het informatiemodel. Zo kan worden vastgelegd wie eigenaar is van bepaalde gegevens, of wie de verplichting heeft om een bepaalde toestand te realiseren of handhaven.

- **Relevantie voor informatiemodellering**: Maakt afhankelijkheden tussen actoren expliciet die het informatiemodel impliciet veronderstelt.
- **Toepassing**: Analyse van ketens, informatieverantwoordelijkheid, governance.
- **Meer info**: [istarwiki.org](https://istarwiki.org)

## Ampersand

**Ampersand** is een formalisatie- en verificatiemethode voor informatiemodellen waarin bedrijfsregels centraal staan. Op basis van relationele algebra specificeer je welke feiten gelden. Ampersand ondersteunt zelfs de gegenereerde uitvoering van het informatiemodel inclusief regels, als proof-of-concept of prototyping-instrument.

Het informatiemodel in Ampersand bestaat uit concepten en relaties, een conceptueel informatiemodel dus, en wordt aangevuld met regels die over die relaties moeten gelden.

- **Relevantie voor informatiemodellering**: Helpt bij het formaliseren, verifiëren en afdwingbaar maken van beperkingen die vaak impliciet blijven in diagrammen.
- **Toepassing**: Domeinen met strikte consistentie-eisen of regelgedreven logica.
- **Meer info**: [Ampersand](https://ampersandtarski.github.io/)

## Ontologische benaderingen (BFO, UFO, DOLCE)

Deze methoden hanteren formele filosofische kaders om te bepalen welke soorten entiteiten (objecten, gebeurtenissen, rollen, kwaliteiten) onderscheiden moeten worden in een model. Ontologieën bieden daarmee een semantische grondlaag voor conceptueel modelleren.

Ze helpen voorkomen dat fundamenteel verschillende concepten (zoals processen en toestanden, of objecten en attributen) onterecht als gelijksoortig gemodelleerd worden. Ze geven ook houvast bij het categoriseren van concepten in domeinoverschrijdende modellen.

- **Relevantie voor informatiemodellering**: Bieden terminologische helderheid en conceptuele consistentie op fundamenteel niveau.
- **Toepassing**: Wetenschap, semantisch web, interoperabiliteit, kennismanagement.
- **Meer info**:
  - [Basic Formal Ontology (BFO)](https://basic-formal-ontology.org/)
  - [UFO](https://nemo.inf.ufes.br/projects/ufo/)
  - [DOLCE](http://www.loa.istc.cnr.it/index.php/DOLCE)

## ORM en Fact-Based Modeling

**Object-Role Modeling (ORM)** en aanverwante technieken modelleren feiten uit de werkelijkheid in natuurlijke taal, zonder technische tussenlaag. In plaats van 'klassen met attributen' worden feiten vastgelegd als rolcombinaties tussen objecten.

Dit leidt tot modellen die semantisch rijk en controleerbaar zijn, met de mogelijkheid om formele beperkingen op natuurlijke wijze toe te voegen.

- **Relevantie voor informatiemodellering**: Alternatief voor traditionele notaties met betere ondersteuning voor modellering van beperkingen en validatie door domeinexperts.
- **Toepassing**: Domeinen met taalgevoeligheid, juridische contexten, formele eisen.
- **Tooling**: [NORMA ORM tool](https://www.orm.net/)
- **Meer info**: [Fact-Based Modeling site](https://www.factbasedmodeling.org/)

## DMN & BPMN

**DMN** (Decision Model and Notation) en **BPMN** (Business Process Model and Notation) zijn gestandaardiseerde notaties voor respectievelijk beslislogica en processen.

Conceptuele informatiemodellen kunnen niet altijd zelfstandig de betekenis of werking van gegevens verklaren; DMN en BPMN kunnen dan context leveren over *waarom* bepaalde informatie nodig is, *wanneer* ze wordt gegenereerd, of *hoe* beslissingen en processen eraan gekoppeld zijn.

- **Relevantie voor informatiemodellering**: Biedt context en traceerbaarheid voor informatiebehoeften via proces- of beslismodellen.
- **Toepassing**: Koppeling met werkstromen, bedrijfsregels en informatieanalyse.
- **Meer info**:
  - [DMN bij OMG](https://www.omg.org/dmn/)
  - [BPMN bij OMG](https://www.omg.org/spec/BPMN/)
