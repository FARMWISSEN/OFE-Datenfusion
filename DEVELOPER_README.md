# Developer README - QGIS Interpolation Plugin

## Schnellübersicht

**Zweck**: QGIS-Plugin für räumliche Interpolation mittels Ordinary Kriging für On-Farm Research  
**Sprache**: Python 3.7+  
**Framework**: QGIS 3.x Plugin API  
**Hauptbibliothek**: pykrige (Kriging-Implementierung)

---

## Architektur-Übersicht

```
interpolation/
├── i_plugin.py              # Hauptlogik: Interpolation, Datenverarbeitung, CRS-Handling
├── i_plugin_dialog.py       # UI-Controller: Dialog-Management, User-Input
├── variogram_models.py      # Variogramm-Modelle (linear, spherical, exponential, gaussian)
├── variogram_plotter.py     # Matplotlib-basierte Variogramm-Visualisierung
├── variogram_dialog.py      # Dialog für Variogramm-Analyse-Ergebnisse
├── config.py                # Zentrale Konfigurationskonstanten
├── exceptions.py            # Custom Exception-Hierarchie
├── Optimierung.ui           # Qt Designer UI-Datei
└── resources.py             # Qt-Ressourcen (Icons, etc.)
```

---

## Kernkomponenten

### 1. **i_plugin.py** - Hauptklasse `IPlugIn`

**Verantwortlichkeiten:**
- Plugin-Lifecycle (initGui, unload, run)
- Datenvalidierung und -vorbereitung
- Koordinatensystem-Transformationen (UTM)
- Variogramm-Analyse und -Optimierung
- Kriging-Interpolation (Raster + Punkt-zu-Punkt)
- Raster-Layer-Erstellung (GeoTIFF)
- Metadaten-Management (generisch für Raster + Punkt)
- **Automatisches Backup-Management**
- **Automatisches Farbrampen-Styling** (neu)

**Wichtige Methoden:**

| Methode | Zweck | Zeilen |
|---------|-------|--------|
| `validate_input_data()` | Prüft Layer, Felder, CRS, Boundary | 522-669 |
| `convert_to_utm()` | Automatische UTM-Konvertierung (mit Duplikat-Check) | 277-405 |
| `prepare_data()` | Extrahiert x, y, z für Kriging | 674-763 |
| `create_output_grid()` | Erstellt Interpolationsgrid mit Buffer | 765-837 |
| `analyze_variogram()` | Variogramm-Analyse + Optimierung | 894-1058 |
| `interpolate_ordinary_kriging()` | Führt Kriging durch (grid/points) | 1060-1147 |
| `create_raster_layer()` | Erstellt GeoTIFF aus Interpolationsdaten | 1149-1227 |
| **`apply_color_ramp_to_raster()`** | **Wendet automatisch Farbrampe auf Raster an (neu)** | **1253-1350** |
| **`save_metadata()`** | **Speichert Metadaten (generisch für Raster + Punkt)** | **1352-1412** |
| **`create_layer_backup()`** | **Erstellt Backup vor Layer-Modifikation** | **1366-1455** |
| `update_target_layer()` | Aktualisiert Ziel-Layer mit interpolierten Werten | 1457-1550 |
| `run_point_interpolation()` | Punkt-zu-Punkt Interpolation (mit Backup + Metadata) | 1552-1649 |
| `run()` | Hauptworkflow für Raster-Interpolation | 1653-1907 |

**Datenfluss (Raster-Interpolation):**
```
User Input (Dialog) 
  → validate_input_data() 
  → prepare_data() [x, y, z arrays]
  → create_output_grid() [grid_x, grid_y, mask]
  → analyze_variogram() [optimierte Parameter]
  → interpolate_ordinary_kriging() [z_pred]
  → create_raster_layer() [GeoTIFF]
  → Layer zu QGIS hinzufügen
```

---

### 2. **i_plugin_dialog.py** - Klasse `IPlugInDialog`

**Verantwortlichkeiten:**
- UI-Setup und Signal-Verbindungen
- Layer- und Feld-Auswahl (mit Filtern)
- Parameter-Validierung (UI-Ebene)
- Settings speichern/laden (QSettings)
- Variogramm-Analyse-Dialog triggern

**UI-Komponenten:**

| Widget | Typ | Zweck |
|--------|-----|-------|
| `mMapLayerComboBox` | QgsMapLayerComboBox | Input-Layer (Punkte) |
| `mFieldComboBox` | QgsFieldComboBox | Zu interpolierendes Feld |
| `mMapLayerComboBox_boundary` | QgsMapLayerComboBox | Boundary-Layer (Polygone) |
| `mMapLayerComboBox_target_layer` | QgsMapLayerComboBox | Ziel-Layer (Punkt-Interpolation) |
| `mMapLayerComboBox_covariate_point` | QgsMapLayerComboBox | Kovariaten-Layer (Punkt-Interpolation) |
| `doubleSpinBox_cellsize` | QDoubleSpinBox | Raster-Zellgröße |
| `doubleSpinBox_sill/range/nugget` | QDoubleSpinBox | Variogramm-Parameter |
| `comboBox_variogram` | QComboBox | Variogramm-Modell-Auswahl |
| `spinBox_lags` | QSpinBox | Anzahl Lags für Variogramm |

**Wichtige Methoden:**

| Methode | Zweck | Zeilen |
|---------|-------|--------|
| `setup_ui_components()` | Initialisiert UI-Elemente | 72-165 |
| `connect_signals()` | Verbindet Signals mit Slots | 360-390 |
| `_validate_and_add_layer()` | Generische Layer-Validierung (Helper) | 168-243 |
| `validate_inputs()` | Prüft UI-Eingaben (Raster) | 653-734 |
| `validate_point_interpolation_inputs()` | Prüft UI-Eingaben (Punkt) | 434-490 |
| `get_parameters()` | Sammelt Parameter für Backend | 618-633 |
| `show_variogram_analysis()` | Zeigt Variogramm-Dialog | (in Dialog) |
| `interpolate_points()` | Startet Punkt-Interpolation | 492-542 |

---

### 3. **variogram_models.py**

**Verfügbare Modelle:**
- `linear_variogram_model` - Lineares Modell
- `spherical_variogram_model` - Sphärisches Modell (häufig verwendet)
- `exponential_variogram_model` - Exponentielles Modell
- `gaussian_variogram_model` - Gaußsches Modell

**Optimierung:**
- `optimize_variogram_parameters()` - Curve-Fitting mit scipy.optimize.curve_fit
- Berechnet RMSE und R² für Modellgüte
- Bounds: [0, 0, 0] bis [∞, max_lags*2, max_gamma*2]

---

### 4. **config.py** - `InterpolationConfig`

**Wichtige Konstanten:**

| Kategorie | Konstante | Wert | Zweck |
|-----------|-----------|------|-------|
| Variogramm | `MIN_POINTS_FOR_VARIOGRAM` | 30 | Min. Punkte für Analyse |
| Variogramm | `MIN_LAGS` / `MAX_LAGS` | 3 / 20 | Lag-Bereich |
| Grid | `GRID_BUFFER_MULTIPLIER` | 1.0 | Buffer um Boundary |
| Validierung | `ZERO_VALUE_WARNING_THRESHOLD` | 90 | Warnung bei >90% Nullen |
| UI | `DEFAULT_CELL_SIZE` | 10.0 | Standard-Rastergröße |
| Shapefile | `MAX_FIELD_NAME_LENGTH` | 10 | Shapefile-Limit |
| Output | `OUTPUT_DIR_NAME` | "i_plugin_outputs" | Output-Verzeichnis |
| Output | `RASTER_INTERPOLATION_DIR` | "raster_interpolation" | Raster-Output-Unterverzeichnis |
| Output | `POINT_INTERPOLATION_DIR` | "point_interpolation" | Punkt-Output-Unterverzeichnis |
| Styling | `COLOR_RAMP_CLASSES` | 6 | Anzahl Farbklassen für Raster-Visualisierung |

---

### 5. **exceptions.py** - Exception-Hierarchie

```
InterpolationError (Base)
├── DataValidationError      # Ungültige Eingabedaten
├── GeometryError            # Geometrie-Probleme
├── CoordinateSystemError    # CRS/UTM-Fehler
├── InterpolationCalculationError  # Kriging-Fehler
└── OutputError              # Raster-Erstellung-Fehler
```

**Verwendung:** Ermöglicht spezifisches Error-Handling in UI und Backend

---

## Workflows

### **Workflow 1: Raster-Interpolation**

1. **User-Aktion**: Wählt Input-Layer, Feld, optional Boundary
2. **Validierung**: 
   - Layer hat Features?
   - Feld hat gültige Werte (keine NULLs/NaNs)?
   - CRS ist UTM? → Falls nein: Auto-Konvertierung anbieten
   - Punkte innerhalb Boundary?
3. **Daten vorbereiten**:
   - `prepare_data()` extrahiert x, y, z als numpy arrays
   - Filtert Punkte außerhalb Boundary
4. **Grid erstellen**:
   - `create_output_grid()` erstellt Interpolationsgrid
   - Erweitert Boundary um Buffer (cell_size * 1.0)
   - Erstellt Maske für Punkte innerhalb Boundary
5. **Variogramm-Analyse** (optional):
   - `analyze_variogram()` berechnet experimentelles Variogramm
   - Optimiert Parameter (nugget, range, sill)
   - Erstellt Plot mit RMSE/R²
6. **Interpolation**:
   - `interpolate_ordinary_kriging()` führt Kriging durch
   - Verwendet pykrige.OrdinaryKriging
   - Gibt interpolierte Werte zurück
7. **Raster erstellen**:
   - `create_raster_layer()` erstellt GeoTIFF
   - Wendet Maske an (NaN außerhalb Boundary)
   - Setzt GeoTransform und Projektion
8. **Output**:
   - Layer zu QGIS-Projekt hinzufügen
   - Metadaten als JSON speichern
   - Variogramm-Plot als PNG speichern

### **Workflow 2: Punkt-zu-Punkt-Interpolation**

1. **User-Aktion**: Wählt Kovariaten-Layer (mit Werten) + Ziel-Layer (ohne Werte)
2. **Validierung**: Beide Layer gültig, Feld hat Werte
3. **Daten vorbereiten**:
   - Kovariaten: x, y, z aus Layer extrahieren
   - Ziel: x, y Koordinaten extrahieren
4. **Interpolation**:
   - `interpolate_ordinary_kriging()` mit style='points'
   - Interpoliert an Ziel-Koordinaten
5. **🆕 Backup erstellen**:
   - `create_layer_backup()` sichert Ziel-Layer
   - Nur beim ersten Mal (idempotent)
   - Speichert in `projektverzeichnis/backups/`
6. **Layer aktualisieren**:
   - `update_target_layer()` fügt neues Feld hinzu
   - Schreibt interpolierte Werte in Attributtabelle
   - Feldname: max. 10 Zeichen (Shapefile-kompatibel)
7. **Metadaten speichern**:
   - `save_metadata()` mit `interpolation_type="point"`
   - Speichert in `projektverzeichnis/i_plugin_outputs/point_interpolation/`
   - Enthält: Kovariaten-Layer, Ziel-Layer, Backup-Info, Kriging-Parameter

---

## Wichtige Design-Entscheidungen

### **1. UTM-Zwang**
- **Warum**: Kriging benötigt metrische Distanzen
- **Implementierung**: `is_utm_crs()` prüft EPSG:326xx/327xx
- **User-Flow**: Dialog fragt bei Nicht-UTM nach Auto-Konvertierung
- **Duplikat-Vermeidung**: `convert_to_utm()` prüft auf existierende Layer im Projekt und Dateien im Filesystem
- **Robustheit**: Generiert eindeutige Dateinamen (`UTM_Layer_1.shp`, `_2.shp`, etc.) bei Konflikten

### **2. Boundary-Handling**
- **Multipart-Support**: `combine_boundary_geometries()` kombiniert alle Polygone
- **Grid-Buffer**: Erweitert Grid um 1*cell_size für bessere Randinterpolation
- **Masking**: Setzt Werte außerhalb Boundary auf NaN

### **3. Null-Wert-Handling**
- **Validierung**: `get_field_value()` prüft None, QVariant.isNull(), np.isnan()
- **Warnung**: Bei >90% Nullen → User-Warnung
- **Fehler**: Bei NULL/NaN in Daten → DataValidationError

### **4. Shapefile-Kompatibilität**
- **Feldnamen**: Max. 10 Zeichen (z.B. "EM38_INT", "EM38_IN1")
- **Feldtyp**: QVariant.Double mit Length=20, Precision=10
- **Implementierung**: `update_target_layer()` generiert kurze Namen

### **5. Variogramm-Optimierung**
- **Automatisch**: `calculate_optimal_lags()` berechnet optimale Lag-Anzahl
- **Metriken**: RMSE, R², AIC für Modellvergleich
- **Bounds**: Verhindert unrealistische Parameter

### **6. Backup-Management (neu)**
- **Automatisch**: Backup vor jeder Punkt-Interpolation
- **Idempotent**: Nur ein Backup pro Layer (kein Timestamp)
- **Speicherort**: `projektverzeichnis/backups/LayerName_backup.shp`
- **Nicht-invasiv**: Backup wird nicht zum Projekt hinzugefügt
- **Fallback**: Bei nicht gespeichertem Projekt → Home-Verzeichnis
- **Return-Wert**: Tuple `(backup_path, was_created)` für User-Feedback

### **7. Metadaten-Management (generisch)**
- **Beide Typen**: `save_metadata()` funktioniert für Raster + Punkt
- **Typ-Parameter**: `interpolation_type="raster"` oder `"point"`
- **Basis-Metadaten**: Timestamp, Methode, Kriging-Parameter (beide Typen)
- **Typ-spezifisch**: Raster (cell_size, boundary) vs. Punkt (backup_info, target_layer)
- **Speicherorte**: 
  - Raster: `i_plugin_outputs/raster_interpolation/`
  - Punkt: `i_plugin_outputs/point_interpolation/`

### **8. Boundary-Masken-Berechnung (verbessert)**
- **Problem**: Pixel an Rändern/Ecken wurden nicht eingeschlossen
- **Alte Methode**: Prüft ob Pixel-**Zentrum** innerhalb Boundary (`point.within()`)
- **Neue Methode**: Prüft ob Pixel-**Polygon** Boundary überlappt (`polygon.intersects()`)
- **Ergebnis**: Vollständige Feldabdeckung, keine fehlenden Randpixel
- **Implementierung**: `create_output_grid()` erstellt Pixel-Quadrate (cell_size/2 Radius)

### **9. Automatisches Farbrampen-Styling (neu)**
- **Automatisch**: Jedes Raster bekommt sofort eine Farbrampe
- **Farbschema**: Red → Yellow → Green (intuitiv: niedrig=rot, hoch=grün)
- **Klassifizierung**: 6 gleichmäßig verteilte Klassen (konfigurierbar)
- **Interpoliert**: Sanfte Übergänge zwischen Farben
- **Min/Max**: Automatisch aus Band-Statistiken
- **Optional**: Fehler werden nur geloggt, Raster bleibt verwendbar
- **Konfiguration**: `COLOR_RAMP_CLASSES` in `config.py`

**Output-Verzeichnisstruktur:**
```
projektverzeichnis/
├── i_plugin_outputs/
│   ├── raster_interpolation/              # Raster-Outputs
│   │   ├── raster_interpolation_Layer_Field_TIMESTAMP.tif
│   │   ├── raster_interpolation_Layer_Field_TIMESTAMP_metadata.json
│   │   └── raster_interpolation_Layer_Field_TIMESTAMP_variogram.png
│   │
│   └── point_interpolation/               # Punkt-Outputs
│       └── point_interpolation_Layer_Field_TIMESTAMP_metadata.json
│
└── backups/                                # Layer-Backups
    └── LayerName_backup.shp
```

---

## Debugging-Tipps

### **Logging aktivieren**
```python
# In QGIS Python Console:
from qgis.core import QgsMessageLog, Qgis
QgsMessageLog.logMessage("Test", "I-PlugIn", Qgis.Info)
```

**Log-Viewer**: QGIS → View → Panels → Log Messages → Filter "I-PlugIn"

### **Häufige Probleme**

| Problem | Ursache | Lösung |
|---------|---------|--------|
| "Keine gültigen Werte" | NULL/NaN in Feld | `get_field_value()` prüfen, Daten bereinigen |
| "Keine Punkte innerhalb Boundary" | CRS-Mismatch | Beide Layer in gleiches UTM konvertieren |
| "Grid Shape Mismatch" | Buffer-Berechnung falsch | `create_output_grid()` Logs prüfen |
| "Raster versetzt" | GeoTransform falsch | x, y an `create_raster_layer()` übergeben |
| "Variogramm-Optimierung fehlgeschlagen" | Zu wenige Punkte | Min. 30 Punkte benötigt |
| "Fehler beim UTM-Layer erstellen" (Windows) | Datei existiert bereits | Wird automatisch mit `_1`, `_2` suffix gelöst |
| "Viele identische UTM-Layer" (macOS) | Keine Duplikat-Prüfung | Wird jetzt automatisch verhindert |

### **Debug-Logs in Code**
```python
self.log(f"Debug: {variable}", Qgis.Info)  # Info-Level
self.log(f"Warning: {issue}", Qgis.Warning)  # Warnung
self.log(f"Error: {error}", Qgis.Critical)  # Fehler
```

---

## Testing

### **Manuelle Tests**

1. **Raster-Interpolation**:
   - Layer mit 50+ Punkten, numerisches Feld
   - Mit/ohne Boundary
   - Verschiedene Variogramm-Modelle
   - Verschiedene Zellgrößen

2. **Punkt-Interpolation**:
   - Kovariaten-Layer (50+ Punkte mit Werten)
   - Ziel-Layer (beliebig viele Punkte)
   - Prüfe neues Feld in Attributtabelle

3. **Edge Cases**:
   - Layer mit nur 10 Punkten → Warnung
   - Layer mit 100% Null-Werten → Fehler
   - Nicht-UTM CRS → Konvertierungs-Dialog
   - Punkte außerhalb Boundary → Warnung

### **Unit Tests** (TODO)
- Siehe `test/` Verzeichnis
- Aktuell: Mock-Interfaces für QGIS-API

---

## Erweiterungsmöglichkeiten

### **Kurzfristig**
- [ ] Co-Kriging (multivariate Interpolation)
- [ ] Cross-Validation für Variogramm-Parameter
- [ ] Batch-Processing (mehrere Layer/Felder)
- [ ] Export von Variogramm-Parametern (CSV)

### **Mittelfristig**
- [ ] Universal Kriging (mit Trend)
- [ ] Indicator Kriging (kategoriale Daten)
- [ ] Anisotropie-Support (richtungsabhängige Variogramme)
- [ ] GPU-Beschleunigung (große Datasets)

### **Langfristig**
- [ ] Machine Learning Hybrid (Kriging + Random Forest)
- [ ] Zeitreihen-Kriging (Raum-Zeit-Interpolation)
- [ ] Web-Service Integration (Cloud-Processing)

---

## Abhängigkeiten

### **Python-Packages**
```bash
# Installation in QGIS Python:
python -m pip install pykrige numpy scipy matplotlib
```

| Package | Version | Zweck |
|---------|---------|-------|
| pykrige | ≥1.6.0 | Kriging-Implementierung |
| numpy | ≥1.19.0 | Array-Operationen |
| scipy | ≥1.5.0 | Optimierung (curve_fit) |
| matplotlib | ≥3.3.0 | Variogramm-Plots |
| gdal/osgeo | (QGIS) | Raster-I/O |

### **QGIS-Module**
- `qgis.core` - Layer, CRS, Processing
- `qgis.PyQt` - UI-Komponenten
- `processing` - Native QGIS-Algorithmen (reprojectlayer)

---

## Code-Konventionen

### **Naming**
- **Klassen**: PascalCase (`IPlugIn`, `VariogramPlotter`)
- **Methoden**: snake_case (`prepare_data`, `convert_to_utm`)
- **Konstanten**: UPPER_SNAKE_CASE (`MIN_LAGS`, `DEFAULT_CELL_SIZE`)
- **Private**: Prefix `_` (nicht verwendet, da QGIS-Plugin)

### **Docstrings**
- **Deutsch** für User-facing Funktionen
- **Format**: Google-Style mit Args/Returns/Raises
- **Beispiel**:
```python
def prepare_data(self, layer, field_name, boundary_layer=None):
    """Bereitet die Vektordaten für die Kriging-Interpolation vor.
    
    Args:
        layer (QgsVectorLayer): Layer mit den Punktdaten
        field_name (str): Name des Feldes mit den zu interpolierenden Werten
        boundary_layer (QgsVectorLayer, optional): Layer mit Begrenzungspolygonen
        
    Returns:
        tuple: (x, y, z) - NumPy Arrays mit den Koordinaten und Werten
        
    Raises:
        ValueError: Wenn die Validierung fehlschlägt
    """
```

### **Error-Handling**
- **Spezifische Exceptions**: Verwende Custom Exceptions aus `exceptions.py`
- **User-Feedback**: Immer mit deutschen Fehlermeldungen
- **Logging**: Zusätzlich technische Details ins Log

---

## Kontakt & Support

- **Autor**: Lucas Johannsen (lucas.johannsen@fh-kiel.de)
- **Projekt**: On-Farm Research Module (OFR 3)
- **QGIS Version**: ≥3.0
- **Lizenz**: GNU GPL v2+

---

## Changelog

### Version 0.1 (aktuell)
- Ordinary Kriging für Raster- und Punkt-Interpolation
- 4 Variogramm-Modelle (linear, spherical, exponential, gaussian)
- Automatische UTM-Konvertierung mit Duplikat-Vermeidung
- Variogramm-Analyse mit Optimierung
- Boundary-Support mit Multipart-Geometrien
- Metadaten-Export (JSON)
- Deutsche UI und Fehlermeldungen
- **Bugfix**: UTM-Konvertierung prüft auf existierende Layer/Dateien (verhindert Duplikate und Windows-Fehler)
- **Feature**: Automatisches Backup vor Punkt-Interpolation (idempotent, nur ein Backup pro Layer)
- **Feature**: Generische Metadaten-Speicherung für beide Interpolationstypen
- **Improvement**: Selbsterklärende Ordnernamen (`raster_interpolation` statt `ordinary_kriging`)
- **Bugfix**: Vollständige Raster-Abdeckung an Boundary-Rändern (Pixel-Polygon-Maske statt Punkt-Maske)
- **Feature**: Automatisches Farbrampen-Styling für Raster-Layer (Red→Yellow→Green, 6 Klassen)

---

## Schnellreferenz: Wichtigste Dateien

| Datei | Zeilen | Zweck | Wichtigste Funktionen |
|-------|--------|-------|----------------------|
| `i_plugin.py` | ~1850 | Backend-Logik | `run()`, `interpolate_ordinary_kriging()`, `analyze_variogram()`, `convert_to_utm()`, `create_layer_backup()` |
| `i_plugin_dialog.py` | ~1020 | UI-Controller | `get_parameters()`, `validate_inputs()`, `interpolate_points()` |
| `config.py` | 88 | Konfiguration | `InterpolationConfig` (alle Konstanten) |
| `variogram_models.py` | 115 | Variogramm-Modelle | `optimize_variogram_parameters()`, `VARIOGRAM_MODELS` |
| `exceptions.py` | 74 | Exception-Typen | `DataValidationError`, `GeometryError`, etc. |

---

## Bekannte Verbesserungen (2025-10-07)

### ✅ UTM-Konvertierung robuster gemacht
**Problem**: `convert_to_utm()` erstellte immer neue Layer ohne Duplikat-Prüfung
- Windows: Fehler beim Überschreiben existierender Dateien
- macOS: Viele identische Layer im Projekt

**Lösung**:
1. Prüft auf existierende UTM-Layer im QGIS-Projekt (Zeile 331-342)
2. Prüft auf existierende Dateien im Filesystem (Zeile 360-366)
3. Generiert eindeutige Dateinamen mit Counter bei Konflikten
4. Verwendet `CoordinateSystemError` für besseres Error-Handling
5. Umfangreiches Logging für Debugging

### ✅ Automatisches Backup-Management implementiert
**Problem**: Bei Punkt-Interpolation wurde der Ziel-Layer direkt modifiziert ohne Backup
- Keine Möglichkeit zur Wiederherstellung bei Fehlern
- User musste manuell Backups erstellen

**Lösung**:
1. Neue Methode `create_layer_backup()` (Zeile 1366-1455)
2. Automatisches Backup vor `update_target_layer()` in `run_point_interpolation()`
3. Idempotent: Nur ein Backup pro Layer (ohne Timestamp)
4. Speicherort: `projektverzeichnis/backups/LayerName_backup.shp`
5. Return-Wert: `(backup_path, was_created)` für präzises User-Feedback
6. Intelligente Nachricht: "wurde erstellt" vs. "existiert bereits"
7. Nicht-invasiv: Backup wird nicht zum Projekt hinzugefügt
8. Fallback: Bei nicht gespeichertem Projekt → Home-Verzeichnis

### ✅ Metadaten-Management generisch gemacht
**Problem**: Metadaten wurden nur für Raster-Interpolation gespeichert
- Punkt-Interpolation hatte keine Nachvollziehbarkeit
- Keine Info über verwendete Parameter

**Lösung**:
1. `save_metadata()` erweitert mit `interpolation_type` Parameter (Zeile 1264-1324)
2. Basis-Metadaten für beide Typen: Timestamp, Methode, Kriging-Parameter
3. Typ-spezifische Metadaten:
   - Raster: input_layer, cell_size, boundary_layer, output_format
   - Punkt: covariate_layer, target_layer, interpolated_points, backup_info
4. Konsistente Ordnerstruktur:
   - Raster: `i_plugin_outputs/raster_interpolation/` (vorher: `ordinary_kriging/`)
   - Punkt: `i_plugin_outputs/point_interpolation/`
5. Konstanten in `config.py`: `RASTER_INTERPOLATION_DIR`, `POINT_INTERPOLATION_DIR`

### ✅ Boundary-Masken-Berechnung verbessert
**Problem**: Pixel an Boundary-Rändern und -Ecken fehlten
- Alte Maske prüfte nur ob Pixel-Zentrum innerhalb Boundary liegt
- Pixel, die Boundary berühren aber Zentrum außerhalb haben, wurden maskiert (NaN)
- Resultat: Unvollständige Feldabdeckung, fehlende Ecken

**Lösung**:
1. Pixel-Polygone statt Punkte: Erstellt Quadrat mit `cell_size/2` Radius (Zeile 811-825)
2. Überlappungs-Test: Verwendet `intersects()` statt `within()` (Zeile 831)
3. Alle Pixel, die Boundary berühren oder überlappen, werden eingeschlossen
4. Vollständige Feldabdeckung ohne fehlende Randpixel
5. Keine Änderung an Grid-Größe notwendig - nur Masken-Logik verbessert

### ✅ Automatisches Farbrampen-Styling implementiert
**Problem**: Raster-Layer wurden in Graustufen angezeigt
- Schwer zu interpretieren
- User musste manuell Styling anpassen
- Keine konsistente Visualisierung

**Lösung**:
1. Neue Methode `apply_color_ramp_to_raster()` (Zeile 1253-1350)
2. Gradient Color Ramp: Red → Yellow → Green mit Zwischenstopp bei 50%
3. Automatische Min/Max-Erkennung aus Band-Statistiken
4. 6 gleichmäßig verteilte Farbklassen (konfigurierbar via `COLOR_RAMP_CLASSES`)
5. Interpolierter Modus für sanfte Übergänge
6. Wird automatisch nach Layer-Erstellung aufgerufen
7. Optional: Fehler werden nur geloggt, werfen keine Exception
8. Imports: `QgsGradientColorRamp`, `QgsGradientStop`, `QgsColorRampShader`

### ✅ Punkt-Interpolation Validierung korrigiert
**Problem**: `validate_point_interpolation_inputs()` hatte mehrere Bugs (i_plugin_dialog.py)
- Prüfte falsches Feld (`mFieldComboBox` statt `mFieldComboBox_covariate`)
- Prüfte falschen Layer (Target statt Covariate für Null/Zero-Werte)
- Redundanter Check für Target-Layer (zweimal)
- Fehlende Prüfung für Covariate-Layer
- Keine NULL-Wert-Prüfung (nur Zero)

**Lösung**:
1. Kovariaten-Layer-Check hinzugefügt (Zeile 441-444)
2. Korrektes Feld geprüft: `mFieldComboBox_covariate` (Zeile 447-449)
3. Null/Zero-Check im richtigen Layer: Covariate statt Target (Zeile 456-472)
4. NULL-Wert-Prüfung hinzugefügt mit `QVariant.isNull()` (Zeile 462-464)
5. Redundanter Check entfernt
6. Klarere Fehlermeldungen: "Kovariaten-Daten enthalten..."

### ✅ Layer-Validierungs-Funktionen refactored (DRY)
**Problem**: 4 fast identische Funktionen mit dupliziertem Code (~132 Zeilen)
- `boundary_layer_add()`
- `target_layer_add()`
- `raster_interpolation_layer_add()`
- `point_interpolation_layer_add()`

**Lösung**:
1. Generische Helper-Funktion erstellt: `_validate_and_add_layer()` (Zeile 168-243)
2. Alle 4 Funktionen refactored zu schlanken Wrappern (je ~5 Zeilen)
3. Zentrale Fehlerbehandlung für alle 5 Exception-Typen
4. Explizite Parameter (layer_combo, field_combo, layer_type_name)
5. Rückwärtskompatibel - keine Breaking Changes
6. **30 Zeilen Code gespart** (1027 → 997 Zeilen)

**Vorteile**:
- DRY-Prinzip: Code nur einmal
- Wartbarkeit: Änderungen an einer Stelle
- Testbarkeit: Eine Funktion statt vier
- Lesbarkeit: Selbstdokumentierend

---

**Letzte Aktualisierung**: 2025-10-07  
**Für**: Schneller Kontext-Aufbau bei Entwicklung/Debugging
