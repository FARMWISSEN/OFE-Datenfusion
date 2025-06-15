import numpy as np
from scipy.optimize import curve_fit
from typing import Tuple, Dict, List, Optional

def linear_variogram_model(d: np.ndarray, nugget: float, range_: float, sill: float) -> np.ndarray:
    """Linear variogram model."""
    slope = (sill - nugget) / range_
    return slope * d + nugget

def spherical_variogram_model(d: np.ndarray, nugget: float, range_: float, sill: float) -> np.ndarray:
    """Spherical variogram model."""
    return np.where(d < range_, 
                   nugget + (sill - nugget) * (1.5 * d/range_ - 0.5 * (d/range_)**3),
                   sill)

def exponential_variogram_model(d: np.ndarray, nugget: float, range_: float, sill: float) -> np.ndarray:
    """Exponential variogram model."""
    return nugget + (sill - nugget) * (1 - np.exp(-3.0 * d/range_))

def gaussian_variogram_model(d: np.ndarray, nugget: float, range_: float, sill: float) -> np.ndarray:
    """Gaussian variogram model."""
    return nugget + (sill - nugget) * (1 - np.exp(-3.0 * (d/range_)**2))

# Dictionary of available variogram models
VARIOGRAM_MODELS = {
    'linear': linear_variogram_model,
    'spherical': spherical_variogram_model,
    'exponential': exponential_variogram_model,
    'gaussian': gaussian_variogram_model
}

def calculate_variogram_metrics(experimental: np.ndarray, theoretical: np.ndarray) -> Dict[str, float]:
    """Calculate goodness of fit metrics for variogram models.
    
    Args:
        experimental: Experimental variogram values
        theoretical: Theoretical variogram values from model
        
    Returns:
        Dictionary with RMSE and R² metrics
    """
    residuals = experimental - theoretical
    rmse = np.sqrt(np.mean(residuals**2))
    r2 = 1 - np.sum(residuals**2) / np.sum((experimental - np.mean(experimental))**2)
    return {'rmse': rmse, 'r2': r2}

def optimize_variogram_parameters(
    lags: np.ndarray,
    gamma: np.ndarray,
    model_type: str,
    initial_guess: Optional[List[float]] = None
) -> Tuple[List[float], Dict[str, float]]:
    """Optimize variogram model parameters using curve fitting.
    
    Args:
        lags: Distance values
        gamma: Experimental variogram values
        model_type: Type of variogram model ('linear', 'spherical', etc.)
        initial_guess: Initial [nugget, range, sill] values. If None, estimated from data.
        
    Returns:
        Tuple of:
        - List of optimized parameters [nugget, range, sill]
        - Dictionary of fit metrics {'rmse': float, 'r2': float}
    """
    if model_type not in VARIOGRAM_MODELS:
        raise ValueError(f"Unknown variogram model type: {model_type}")
        
    # Estimate initial parameters if not provided
    if initial_guess is None:
        nugget = gamma[0] if len(gamma) > 0 else 0
        sill = np.max(gamma) if len(gamma) > 0 else 1
        range_ = np.median(lags) if len(lags) > 0 else 1
        initial_guess = [nugget, range_, sill]
    
    # Set bounds for parameters
    bounds = ([0, 0, 0],  # Lower bounds: all parameters must be positive
             [np.inf, np.max(lags)*2, np.max(gamma)*2])  # Upper bounds
    
    try:
        # Try curve_fit optimization
        model_func = VARIOGRAM_MODELS[model_type]
        popt, _ = curve_fit(model_func, lags, gamma, 
                          p0=initial_guess,
                          bounds=bounds,
                          method='trf')
        
        # Calculate theoretical values with optimized parameters
        theoretical = model_func(lags, *popt)
        
        # Calculate fit metrics
        metrics = calculate_variogram_metrics(gamma, theoretical)
        
        return popt.tolist(), metrics
        
    except Exception as e:
        # Fallback to simple parameter estimation if optimization fails
        print(f"Optimization failed: {str(e)}")
        return initial_guess, calculate_variogram_metrics(gamma, 
            VARIOGRAM_MODELS[model_type](lags, *initial_guess))
