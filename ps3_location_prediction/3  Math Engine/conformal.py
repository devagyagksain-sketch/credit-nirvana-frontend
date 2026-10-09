import numpy as np

class ConformalCalibrator:
    """
    Implements Split Conformal Calibration for Confidence Radii.
    
    This ensures the model's confidence region has a mathematical 
    guarantee of covering the true location `alpha` percent of the time,
    assuming exchangeability.
    """
    def __init__(self, alpha=0.8):
        self.alpha = alpha
        self.q_hat = 1.0 # default multiplier (no adjustment)

    def calibrate(self, true_distances: np.ndarray, raw_radii: np.ndarray):
        """
        Calibrates the model using a held-out set of true errors.
        true_distances: array of actual distance errors ||true - pred||
        raw_radii: array of raw confidence radii predicted by the model.
        """
        valid = ~np.isnan(true_distances) & ~np.isnan(raw_radii) & (raw_radii > 0)
        true_distances = true_distances[valid]
        raw_radii = raw_radii[valid]
        
        n = len(true_distances)
        if n == 0:
            return
            
        # Non-conformity scores
        scores = true_distances / raw_radii
        
        # Conformal quantile: ceil((n+1)*alpha) / n
        val = (n + 1) * self.alpha / n
        target_quantile = min(1.0, val)
        
        # Use 'higher' interpolation to be conservative
        self.q_hat = np.quantile(scores, target_quantile, method='higher')
        
    def adjust_radius(self, raw_radius: float) -> float:
        """Applies the learned conformal calibration multiplier."""
        return raw_radius * self.q_hat
