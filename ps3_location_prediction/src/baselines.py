import pandas as pd
import numpy as np
from typing import Tuple

def geometric_median(X: np.ndarray, eps=1e-5) -> np.ndarray:
    """Weiszfeld's algorithm for geometric median."""
    if len(X) == 0:
        return np.array([np.nan, np.nan])
    y = np.mean(X, 0)
    for _ in range(100):
        D = np.linalg.norm(X - y, axis=1)
        nonzeros = (D > eps)
        if not nonzeros.any():
            break
        W = 1.0 / D[nonzeros]
        y_new = np.sum(X[nonzeros] * W[:, None], axis=0) / np.sum(W)
        if np.linalg.norm(y - y_new) < eps:
            break
        y = y_new
    return y

class VisitBaselines:
    """
    Robust alternatives to average all GPS points.
    Used for baseline comparisons before full Bayesian Fusion.
    """
    
    @staticmethod
    def mean_estimator(group: pd.DataFrame) -> Tuple[float, float]:
        return group['checkin_x'].mean(), group['checkin_y'].mean()
        
    @staticmethod
    def median_estimator(group: pd.DataFrame) -> Tuple[float, float]:
        return group['checkin_x'].median(), group['checkin_y'].median()
        
    @staticmethod
    def geometric_median_estimator(group: pd.DataFrame) -> Tuple[float, float]:
        pts = group[['checkin_x', 'checkin_y']].values
        gm = geometric_median(pts)
        return gm[0], gm[1]
        
    @staticmethod
    def weighted_estimator(group: pd.DataFrame) -> Tuple[float, float]:
        """
        Weights points by (Trust Pi) / (Variance).
        Requires 'trust_pi' calculated by VisitTrustModel.
        """
        if 'trust_pi' not in group.columns:
            group = group.copy()
            group['trust_pi'] = 1.0
            
        # Treat gps_accuracy_m as standard deviation, so var is acc^2
        var = np.clip(group['gps_accuracy_m']**2, 1.0, None)
        w = group['trust_pi'] / var
        
        if w.sum() == 0:
            return VisitBaselines.mean_estimator(group)
            
        w_norm = w / w.sum()
        est_x = np.sum(group['checkin_x'] * w_norm)
        est_y = np.sum(group['checkin_y'] * w_norm)
        return est_x, est_y
