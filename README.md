# KiCAD 6 Goodies
[![CC BY 4.0][cc-by-shield]][cc-by]

KiCAD 6 libraries used by PiFactory board designs. 

## Content
### Footprints

* PCB coils, including Python script to generate PCB coil shapes
  
### Symbols

* Regulator Linear Goodies:
  * MCP1811A, MCP1812A - 150mA/300mA 1.8V LDO, SOT-23
  * MCP1811B, MCP1812B - 150mA/300mA 1.8V LDO with shutdown, SOT-23-5
* Sensor Proximity Goodies:
  * Inductive Proximity Sensor
  * LDC2112 - Inductive Touch Solution, 2-channel, TSSOP-16

### Templates

* AISLER Simple 2 layers design rules
* AISLER Complex 2 layers design rules
* AISLER 4 layers design rules

## How to use

1. Clone this repo on your disk.
2. Define `KICAD6_GOODIES` path variable in KiCAD: `Preferences` / `Configure Paths...`
3. Optional: define full path to templates in `KICAD_USER_TEMPLATE_DIR` - you will be able to start new projects with design rules and settings specific to a PCB-shop of your choice.
4. Profit!

You can add libraries either globally or per-project. I do it per project.


---
This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg