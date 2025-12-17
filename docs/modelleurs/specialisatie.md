---
title: Specialisatie
parent: Modelleurs
---

Een specialisatie geeft aan dat een specifieke entiteit (zoals `gasnet`) een bijzonder type is van een generieke entiteit (zoals `energienet`). Het subtype erft hierbij alle eigenschappen en relaties van het supertype. In onze diagrammen geven we dit weer door subtypen te *nesten* binnen het supertype. In LinkML gebruiken we `is_a`. We hanteren hierbij twee strikte modelleerregels:

1. **Volledig en exclusief**: Elke instantie van het supertype behoort tot precies één subtype. Er is dus geen overlap en er zijn geen instanties die 'buiten' de gedefinieerde subtypen vallen.
2. **Rigide (statisch)**: Een instantie kan gedurende zijn levenscyclus niet van subtype veranderen. Als dat wel zo is, gebruiken we geen specialisatie maar kennen we een veranderlijke eigenschap toe zoals `soort`.

Samen zorgen deze regels voor een eenduidige identificatie van instanties.
