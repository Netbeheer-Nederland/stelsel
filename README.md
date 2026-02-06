# Stelsel van energieregisters

## Installatie op Windows zonder admin-rechten (portable modus)

1. Maak een map genaamd `tools` in deze map.
2. **Python**: Download [WinPython](https://winpython.github.io/) (de 'dot' versie is genoeg). Pak het uit, zoek de map waar `python.exe` in staat, en kopieer die map naar `tools/python`.
3. **Ruby**: Download [Ruby+Devkit](https://rubyinstaller.org/). Pak het uit en kopieer de map naar `tools/ruby`.
4. Dubbelklik op `run.cmd`.

## Werken met VS Code en een Dev Container

### Installatie

#### Benodigdheden

* Visual Studio Code
  * Dev Container-extensie
* Docker
* Git

#### Instructies

1. Clone deze repository en open de map in Visual Studio Code.
2. Maak een kopie van `.devcontainer.example.json` in dezelfde map en noem dit bestand `.devcontainer.json`. 
3. Navigeer naar de regel met sleutel `postCreateCommand`, en vervang daar `'Your Name'` en `'your@email-address.com'` door je volledige naam en e-mailadres zoals deze op GitHub zichtbaar (moeten) zijn.

> [!caution]
Het aanmaken van nieuwe bestanden in deze map buiten de Dev Container veroorzaakt dat deze bestanden enkel gelezen en niet bewerkt kunnen worden in de container.[^1] Dit is overigens te verhelpen, maar het liefst vermeden.

Het is daarom raadzaam zoveel binnen VS Code in de container te werken.

### Gebruik

1. Start Visual Studio Code.
2. Open deze repository met _Open folder_.
3. Rechtsonderin het scherm vraagt VS Code je nu als het goed is om de Dev Container te starten en het project erin te openen. Bevestig door te klikken op _Reopen in Container_. In het geval deze vraag niet komt, klik dan linksonderin het scherm op het icoon dat een pallet opent om met remotes te verbinden. Kies daar _Open Folder in Container_.
4. Nadat de Dev Container is opgestart, dien je een terminal op te starten.
5. Draai in de terminal: `./run.sh`.

[^1]: Het technisch volledigere verhaal is dat deze bestanden in de container de eigenaar `root` krijgen.
