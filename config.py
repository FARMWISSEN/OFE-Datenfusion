# -*- coding: utf-8 -*-
"""
Configuration constants for the Interpolation Plugin.

This module contains all configuration parameters and constants used throughout
the plugin to ensure consistency and easy maintenance.
"""


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
    DEFAULT_NLAGS = 10
    
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
