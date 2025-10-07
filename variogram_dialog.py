from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Import config and exceptions for constants
try:
    from .config import InterpolationConfig
    from .exceptions import InterpolationError, InterpolationCalculationError
except ImportError:
    # Fallback if import fails
    class InterpolationConfig:
        VARIOGRAM_DIALOG_MIN_WIDTH = 600
        VARIOGRAM_DIALOG_MIN_HEIGHT = 500
        VARIOGRAM_METRICS_TEXT_HEIGHT = 100
        VARIOGRAM_IMAGE_WIDTH = 550
        VARIOGRAM_IMAGE_HEIGHT = 400
    
    # Fallback exceptions
    class InterpolationError(Exception):
        pass
    class InterpolationCalculationError(InterpolationError):
        pass

class VariogramDialog(QDialog):
    def __init__(self, parent=None):
        super(VariogramDialog, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog's UI components."""
        self.setWindowTitle("Variogram Analyse")
        self.setMinimumSize(
            InterpolationConfig.VARIOGRAM_DIALOG_MIN_WIDTH,
            InterpolationConfig.VARIOGRAM_DIALOG_MIN_HEIGHT
        )
        
        # Create layout
        layout = QVBoxLayout()
        
        # Plot label
        self.plot_label = QLabel()
        self.plot_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.plot_label)
        
        # Metrics text area
        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)
        self.metrics_text.setMaximumHeight(InterpolationConfig.VARIOGRAM_METRICS_TEXT_HEIGHT)
        layout.addWidget(self.metrics_text)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
    def display_results(self, plot_path, metrics):
        """Display variogram analysis results.
        
        Args:
            plot_path: Path to the variogram plot image
            metrics: Dictionary containing RMSE and R² values
            
        Raises:
            InterpolationCalculationError: If plot image cannot be loaded
        """
        try:
            # Display plot
            pixmap = QPixmap(plot_path)
            if pixmap.isNull():
                raise InterpolationCalculationError(
                    f"Variogramm-Plot konnte nicht geladen werden: {plot_path}"
                )
            
            scaled_pixmap = pixmap.scaled(
                InterpolationConfig.VARIOGRAM_IMAGE_WIDTH,
                InterpolationConfig.VARIOGRAM_IMAGE_HEIGHT,
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.plot_label.setPixmap(scaled_pixmap)
            
            # Display metrics
            metrics_text = f"Variogram Analyse:\n"
            metrics_text += f"RMSE: {metrics['rmse']:.3f}\n"
            metrics_text += f"R²: {metrics['r2']:.3f}\n"
            metrics_text += "\nLower RMSE values and R² values closer to 1 indicate better model fit."
            
            self.metrics_text.setText(metrics_text)
            
        except (KeyError, TypeError) as e:
            raise InterpolationCalculationError(
                f"Ungültige Metriken für Variogramm-Anzeige: {str(e)}"
            )
