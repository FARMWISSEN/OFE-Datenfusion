import matplotlib.pyplot as plt
import numpy as np
from .variogram_models import VARIOGRAM_MODELS

class VariogramPlotter:
    def __init__(self):
        """Initialize the variogram plotter"""
        self.fig = None
        self.ax = None
        
    def plot_variogram(self, lags, experimental, model_type, nugget, range_, sill,
                      title='Variogram Analyse', save_path=None, show=True):
        """Plot experimental and theoretical variograms.
        
        Args:
            lags: Array of lag distances
            experimental: Array of experimental variogram values
            model_type: Type of variogram model
            nugget: Nugget parameter
            range_: Range parameter
            sill: Sill parameter
            title: Plot title
            save_path: Path to save plot to
            show: Whether to display the plot
        """
        # Create plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        
        # Plot experimental variogram points
        self.ax.scatter(lags, experimental, c='blue', marker='o', 
                   label='Experimental', alpha=0.6)
        
        # Plot theoretical variogram line
        if model_type in VARIOGRAM_MODELS:
            x = np.linspace(0, max(lags), 100)
            y = VARIOGRAM_MODELS[model_type](x, nugget, range_, sill)
            self.ax.plot(x, y, 'r-', label=f'{model_type.capitalize()} Model')
        
        # Customize plot
        self.ax.set_xlabel('Lag Distance')
        self.ax.set_ylabel('Semivariance')
        self.ax.set_title(title)
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        if save_path:
            self.fig.savefig(save_path)
        
        if show:
            self.fig.show()
        
    def close(self):
        """Close the current plot"""
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
