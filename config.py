# -*- coding: utf-8 -*-
"""
Configuration constants for the Interpolation Plugin.

This module contains all configuration parameters and constants used throughout
the plugin to ensure consistency and easy maintenance.
"""


class InterpolationMethod:
    """Enum-ähnliche Klasse für Interpolationsmethoden."""
    ORDINARY_KRIGING = "Ordinary Kriging"
    NEAREST_NEIGHBOR = "Nearest Neighbor"
    # Zukünftige Methoden können hier hinzugefügt werden:
    # UNIVERSAL_KRIGING = "Universal Kriging"
    # IDW = "Inverse Distance Weighting"
    # SPLINE = "Spline"
    # RBF = "Radial Basis Function"
    
    @classmethod
    def get_all_methods(cls):
        """Gibt alle verfügbaren Interpolationsmethoden zurück."""
        return [
            cls.ORDINARY_KRIGING,
            cls.NEAREST_NEIGHBOR,  # Test-Methode (noch nicht implementiert)
            # Weitere Methoden hier hinzufügen wenn implementiert
        ]
    
    @classmethod
    def get_method_index(cls, method_name):
        """Gibt den Index einer Methode in der Liste zurück."""
        methods = cls.get_all_methods()
        try:
            return methods.index(method_name)
        except ValueError:
            return 0  # Default: Ordinary Kriging


class InterpolationConfig:
    """Zentrale Konfiguration für Interpolations-Parameter und Konstanten."""
    
    # Variogramm-Analyse
    MIN_POINTS_FOR_VARIOGRAM = 30  # Minimale Anzahl Punkte für stabile Variogramm-Analyse
    MIN_PAIRS_PER_LAG = 30  # Minimale Anzahl Punkt-Paare pro Lag-Klasse
    MIN_LAGS = 3  # Minimale Anzahl von Lags
    MAX_LAGS = 20  # Maximale Anzahl von Lags
    
    # Grid-Erstellung
    GRID_BUFFER_MULTIPLIER = 1.0  # Multiplikator für Grid-Buffer (cell_size * multiplier)
    GRID_ARANGE_OFFSET = 0.5  # Offset für np.arange zur Vermeidung von Rundungsfehlern
    
    # Raster-Parameter
    RASTER_PIXEL_OFFSET = 0.5  # Pixel-Offset für GeoTransform
    
    # Farbrampen-Styling
    COLOR_RAMP_CLASSES = 6  # Anzahl der Farbklassen für Raster-Visualisierung
    
    # Farbverlauf-Definitionen (RGB-Werte)
    # QGIS Standard Red-Yellow-Green Gradient mit 5 Stops
    COLOR_RAMP_START = (215, 25, 28)      # Rot (0%)
    COLOR_RAMP_STOP_1 = (253, 174, 97)    # Orange (25%)
    COLOR_RAMP_MIDDLE = (255, 255, 192)   # Helles Gelb (50%)
    COLOR_RAMP_STOP_2 = (166, 217, 106)   # Hellgrün (75%)
    COLOR_RAMP_END = (26, 150, 65)        # Grün (100%)
    
    # Positionen der Gradient-Stops (0.0 bis 1.0)
    COLOR_RAMP_STOP_1_POSITION = 0.25
    COLOR_RAMP_MIDDLE_POSITION = 0.5
    COLOR_RAMP_STOP_2_POSITION = 0.75
    
    # Feldnamen (für Shapefile-Kompatibilität)
    DEFAULT_FIELD_PREFIX = "COV_INT"  # Standard-Präfix für interpolierte Felder
    MAX_FIELD_NAME_LENGTH = 10  # Maximale Länge für Shapefile-Feldnamen
    FIELD_NAME_TRUNCATE = 6  # Anzahl Zeichen vom Original-Feldnamen
    
    # Feld-Eigenschaften
    FIELD_TYPE_DOUBLE_LENGTH = 20  # Länge für Double-Felder
    FIELD_TYPE_DOUBLE_PRECISION = 10  # Präzision für Double-Felder
    
    # Datenvalidierung
    ZERO_VALUE_WARNING_THRESHOLD = 90  # Prozent - Warnung wenn mehr als X% Null-Werte
    
    # UI-Defaults
    DEFAULT_CELL_SIZE = 10.0
    DEFAULT_CELL_SIZE_MIN = 0.1
    DEFAULT_CELL_SIZE_MAX = 10000.0
    DEFAULT_SILL = 0.1
    DEFAULT_SILL_MIN = 0.0
    DEFAULT_SILL_MAX = 10000.0
    DEFAULT_RANGE = 100.0
    DEFAULT_RANGE_MIN = 0.1
    DEFAULT_RANGE_MAX = 10000.0
    DEFAULT_NUGGET = 0.0
    DEFAULT_NUGGET_MIN = 0.0
    DEFAULT_NUGGET_MAX = 10000.0
    DEFAULT_NLAGS = 15
    
    # Output-Verzeichnisse
    OUTPUT_DIR_NAME = "i_plugin_outputs"
    LAYER_GROUP_NAME = "I-PlugIn Interpolationen"
    RASTER_INTERPOLATION_DIR = "raster_interpolation"
    POINT_INTERPOLATION_DIR = "point_interpolation"
    
    # Datei-Suffixe
    METADATA_SUFFIX = "_metadata.json"
    VARIOGRAM_PLOT_SUFFIX = "_variogram.png"
    UTM_LAYER_PREFIX = "UTM_"
    
    # Distanz-Berechnung
    DISTANCE_PERCENTILE = 95  # Perzentil für maximale Distanz in Variogramm-Analyse
    
    # Variogramm-Modell-Parameter
    VARIOGRAM_EXPONENTIAL_FACTOR = 3.0  # Faktor für exponential/gaussian Modelle
    VARIOGRAM_BOUNDS_MULTIPLIER = 2  # Multiplikator für Upper Bounds bei Optimierung
    VARIOGRAM_DEFAULT_NUGGET_FALLBACK = 0  # Fallback-Wert wenn keine Daten
    VARIOGRAM_DEFAULT_SILL_FALLBACK = 1  # Fallback-Wert wenn keine Daten
    VARIOGRAM_DEFAULT_RANGE_FALLBACK = 1  # Fallback-Wert wenn keine Daten
    
    # Variogramm-Plot-Einstellungen
    VARIOGRAM_PLOT_FIGSIZE = (10, 6)  # Plot-Dimensionen (width, height)
    VARIOGRAM_PLOT_RESOLUTION = 100  # Anzahl Punkte für theoretische Kurve
    VARIOGRAM_PLOT_EXPERIMENTAL_COLOR = 'blue'  # Farbe für experimentelle Punkte
    VARIOGRAM_PLOT_EXPERIMENTAL_MARKER = 'o'  # Marker-Style für experimentelle Punkte
    VARIOGRAM_PLOT_EXPERIMENTAL_ALPHA = 0.6  # Transparenz für experimentelle Punkte
    VARIOGRAM_PLOT_MODEL_COLOR = 'red'  # Farbe für Modell-Linie
    VARIOGRAM_PLOT_MODEL_LINESTYLE = '-'  # Linien-Style für Modell
    VARIOGRAM_PLOT_GRID_ALPHA = 0.3  # Transparenz für Grid
    
    # Variogramm-Dialog-Einstellungen
    VARIOGRAM_DIALOG_MIN_WIDTH = 600  # Minimale Dialog-Breite
    VARIOGRAM_DIALOG_MIN_HEIGHT = 500  # Minimale Dialog-Höhe
    VARIOGRAM_METRICS_TEXT_HEIGHT = 100  # Höhe des Metrics-Textfeldes
    VARIOGRAM_IMAGE_WIDTH = 550  # Breite des angezeigten Bildes
    VARIOGRAM_IMAGE_HEIGHT = 400  # Höhe des angezeigten Bildes
