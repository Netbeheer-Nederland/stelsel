# Stelsel van energieregisters

## Installatie op Windows zonder admin-rechten (portable modus)

1. Maak een map genaamd `tools` in deze map.
2. **Python**: Download [WinPython](https://winpython.github.io/) (de 'dot' versie is genoeg). Pak het uit, zoek de map waar `python.exe` in staat, en kopieer die map naar `tools/python`.
3. **Ruby**: Download [Ruby+Devkit](https://rubyinstaller.org/). Pak het uit en kopieer de map naar `tools/ruby`.
4. Dubbelklik op `run.cmd`.

## Werken met een Dev Container

### Installatie

#### Benodigdheden

* Visual Studio Code
  * Dev Container-extensie
* Docker

#### Instructies

1. Maak een kopie van `.devcontainer.example.json` in dezelfde map en noem dit bestand `.devcontainer.json`. 
2. Navigeer naar de regel met sleutel `postCreateCommand`, en vervang daar `'Your Name'` en `'your@email-address.com'` door je volledige naam en e-mailadres zoals deze op GitHub zichtbaar (moeten) zijn.

_Let op_: Als je zowel lokaal als in de container werkt kan dit problemen veroorzaken. Na een installatie wordt een `Gemfile.lock` gegenereerd en deze is platformspecifiek. Bij een volgende installatie wordt echter specifiek naar dit bestand gekeken voor exacte versies van afhankelijkheden, maar evt. dus voor het verkeerde platform. Verder kunnen er ook issues optreden met owernship en permissions.

### Gebruik

1. Start Visual Studio Code.
2. Open deze repository met _Open folder_.
3. Rechtsonderin het scherm vraagt VS Code je nu als het goed is om de Dev Container te starten en het project erin te openen. Bevestig door te klikken op _Reopen in Container_. In het geval deze vraag niet komt, klik dan linksonderin het scherm op het icoon dat een pallet opent om met remotes te verbinden. Kies daar _Open Folder in Container_.
4. Nadat de Dev Container is opgestart, start je een terminal (`Ctrl` + `~`).
5. Draai in de terminal: `./run.sh`.
