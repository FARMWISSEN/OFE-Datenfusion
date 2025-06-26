# I-Plugin – Interpolation für QGIS

## Übersicht
Das I-Plugin erweitert QGIS um leistungsstarke Interpolationsverfahren (z.B. Ordinary Kriging) für Raster- und Punktdaten. Es bietet dir eine interaktive Variogramm-Analyse, automatische UTM-Konvertierung und eine deutschsprachige Benutzeroberfläche.

## Hauptfunktionen
- Raster- und Punktinterpolation mittels Ordinary Kriging
- Automatische UTM-Koordinatensystem-Konvertierung
- Interaktive Variogramm-Analyse und -Optimierung

## Features
### Interpolation
- Ordinary Kriging für Rasterdaten und Punktdaten
- Flexible Rasterauflösung
- Punktinterpolation zur Datensatzanreicherung 
- Automatische Variogramm-Parameter-Optimierung

### Datenverarbeitung
- Automatische UTM-Zonenerkennung und -Konvertierung
- Validierung von Eingabedaten und Geometrien
- Unterstützung von Begrenzungspolygonen
- Behandlung von Multi-Part-Geometrien

### Analyse
- Experimentelles und theoretisches Variogramm
- Verschiedene Variogramm-Modelle verfügbar
- RMSE- und R²-Berechnung für Modellvalidierung

### Benutzerfreundlichkeit
- Interaktive Benutzeroberfläche
- Automatische Koordinatensystem-Konvertierung
- Ausführliche Fehlerbehandlung und Logging
- Deutsche Benutzerführung

## Installation

**Wichtig:** Für den aktuellen Entwicklungsstand musst du vor der Installation des Plugins in QGIS zunächst das Python-Package `pykrige` installieren.

1. Öffne die **OSGeo4W Shell**.
2. Gib folgenden Befehl ein und führe ihn aus:
   ```
   python -m pip install pykrige
   ```

Anschließend kannst du das Plugin wie gewohnt in QGIS installieren und testen.

- **Manuell:**
   - Kopiere dieses Repository nach `QGIS3/profiles/default/python/plugins/interpolation`.

   - Starte QGIS neu und aktiviere das Plugin.

## Schnellstart
- Aktiviere das Plugin (QGIS: Menü „Plugins“ → „Verwalten und installieren“)
- Wähle im Menüband „I-Plugin“ aus
- Lade deine Eingabedaten (Punkte, Polygone) und wähle die gewünschte Methode
- Die Ergebnisse werden als neue Layer hinzugefügt

## Voraussetzungen
- QGIS >= 3.x
- Python >= 3.7
- GSTools (wird automatisch installiert)

## Verzeichnisstruktur
```
interpolation/
  ├── i_plugin.py
  ├── i_plugin_dialog.py
  ├── variogram_models.py
  ├── variogram_plotter.py
  ├── /tests
  ├── /help
  ├── /i18n
  ├── /scripts
  └── README.txt
```

## Support & Kontakt
- Fehler bitte als Issue melden
- Kontakt: [Deine E-Mail-Adresse oder Link zu Issues]

## Lizenz
Dieses Plugin steht unter der MIT-Lizenz. Details siehe LICENSE.txt.
