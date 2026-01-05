# OFR Interpolation – QGIS Plugin für On-Farm Research

## Übersicht
Das OFR Interpolation Plugin erweitert QGIS um leistungsstarke Interpolationsverfahren für Raster- und Punktdaten. Es bietet mehrere Interpolationsmethoden, interaktive Variogramm-Analyse, automatische UTM-Konvertierung und eine deutschsprachige Benutzeroberfläche.

## Hauptfunktionen
- **Raster-Interpolation** - Erzeugt flächendeckende Rasterkarten
- **Punkt-Interpolation** - Überträgt Werte zwischen Punktdatensätzen
- Automatische UTM-Koordinatensystem-Konvertierung
- Interaktive Variogramm-Analyse und -Optimierung

## Interpolationsmethoden

| Methode | Beschreibung | Bibliothek |
|---------|--------------|------------|
| **Ordinary Kriging** | Geostatistische Interpolation mit Variogramm-Analyse | PyKrige (optional) |
| **IDW** | Inverse Distance Weighting - distanzgewichtete Interpolation | QGIS-nativ |
| **Nearest Neighbor** | Nächster-Nachbar-Zuweisung ohne Glättung | GDAL |

## Features

### Interpolation
- Ordinary Kriging, IDW und Nearest Neighbor
- Flexible Rasterauflösung
- Punkt-zu-Punkt Interpolation zur Datensatzanreicherung
- Automatische Variogramm-Parameter-Optimierung
- Optionale Kriging-Varianz (σ²) als zusätzliche Karte

### Variogramm-Analyse (nur Kriging)
- Experimentelles und theoretisches Variogramm
- Modellvergleich: Linear, Spherical, Exponential, Gaussian
- RMSE- und R²-Berechnung für Modellvalidierung
- Automatische Parameteroptimierung mit grüner Spinbox-Markierung

### Datenverarbeitung
- Automatische UTM-Zonenerkennung und -Konvertierung
- Validierung von Eingabedaten und Geometrien
- Unterstützung von Begrenzungspolygonen (Boundary Clipping)
- Behandlung von Multi-Part-Geometrien
- Duplikat-Koordinaten-Erkennung mit Averaging-Option

### Benutzerfreundlichkeit
- Interaktive Benutzeroberfläche mit Tab-System
- Dialog bleibt nach Interpolation offen für Folgeanalysen
- Optionale Vektor-Layer Ausgabe
- Automatisches Farbrampen-Styling (Rot-Gelb-Grün)
- Ausführliche Fehlerbehandlung und Logging
- Deutsche Benutzerführung

## Installation

### Plugin installieren
1. Kopiere dieses Repository nach:
   `QGIS3/profiles/default/python/plugins/interpolation`
2. Starte QGIS neu
3. Aktiviere das Plugin unter *Erweiterungen → Erweiterungen verwalten*

### Optionale Abhängigkeit: PyKrige
PyKrige wird nur für Kriging-Interpolation benötigt. IDW und Nearest Neighbor funktionieren auch ohne PyKrige.

**Windows (OSGeo4W Shell):**
```
python -m pip install pykrige
```

**Mac:**
```
/Applications/QGIS-LTR.app/Contents/MacOS/bin/pip3 install pykrige
```

> **Hinweis:** Ohne PyKrige wird Kriging automatisch deaktiviert und die entsprechenden UI-Elemente ausgeblendet.

## Schnellstart
1. Öffne das Plugin: *Praxisversuche → OFR Interpolation*
2. **Raster-Tab:** Wähle Eingabe-Layer, Attributfeld und optional Boundary
3. **Punkt-Tab:** Wähle Kovariaten-Layer und Ziel-Layer
4. Führe optional eine Variogramm-Analyse durch (nur Kriging)
5. Klicke auf "Interpolieren"
6. Die Ergebnisse werden zur Layer-Gruppe "OFR Interpolationen" hinzugefügt

## Voraussetzungen
- QGIS >= 3.x
- Python >= 3.7
- PyKrige (optional, nur für Kriging)

## Verzeichnisstruktur
```
interpolation/
├── i_plugin.py                    # Hauptlogik: Dispatcher + Interpolations-Workflows
├── i_plugin_dialog.py             # UI-Controller: Dialog-Management
├── config.py                      # Zentrale Konfigurationskonstanten
├── exceptions.py                  # Custom Exception-Hierarchie
├── variogram_models.py            # Variogramm-Modelle
├── variogram_plotter.py           # Variogramm-Visualisierung
├── variogram_dialog.py            # Variogramm-Analyse Dialog
├── model_comparison_dialog.py     # Modellvergleich-Dialog
├── duplicate_coordinates_dialog.py # Duplikat-Behandlung Dialog
├── Optimierung.ui                 # Qt Designer UI-Datei
├── DEVELOPER_README.md            # Entwickler-Dokumentation
└── README.txt
```

## Output-Struktur
```
projektverzeichnis/
└── ofr_interpolation_outputs/
    ├── raster_interpolation/      # Raster-Ergebnisse (.tif)
    ├── point_interpolation/       # Punkt-Ergebnisse (.shp)
    ├── utm_layers/                # UTM-transformierte Layer
    └── backups/                   # Automatische Backups
```

## Support & Kontakt
- Fehler bitte als Issue melden
- Repository: https://gitlab.eip-snapwuerz.de/

## Lizenz
Dieses Plugin steht unter der MIT-Lizenz. Details siehe LICENSE.txt.
