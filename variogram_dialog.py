from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class VariogramDialog(QDialog):
    def __init__(self, parent=None):
        super(VariogramDialog, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog's UI components."""
        self.setWindowTitle("Variogram Analysis")
        self.setMinimumSize(600, 500)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Plot label
        self.plot_label = QLabel()
        self.plot_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.plot_label)
        
        # Metrics text area
        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)
        self.metrics_text.setMaximumHeight(100)
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
        """
        # Display plot
        pixmap = QPixmap(plot_path)
        scaled_pixmap = pixmap.scaled(550, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.plot_label.setPixmap(scaled_pixmap)
        
        # Display metrics
        metrics_text = f"Model Evaluation Metrics:\n"
        metrics_text += f"RMSE: {metrics['rmse']:.3f}\n"
        metrics_text += f"R²: {metrics['r2']:.3f}\n"
        metrics_text += "\nLower RMSE values and R² values closer to 1 indicate better model fit."
        
        self.metrics_text.setText(metrics_text)
