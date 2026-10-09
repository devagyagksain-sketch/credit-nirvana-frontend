import numpy as np

class ConfidenceRegion:
    @staticmethod
    def compute_radius_from_grid(X, Y, prob_grid, pred_x, pred_y, alpha=0.8):
        """
        Calculates the radius around pred_x, pred_y that contains alpha probability mass.
        """
        if prob_grid.sum() == 0:
            return np.nan
            
        dist = np.hypot(X - pred_x, Y - pred_y)
        
        flat_dist = dist.flatten()
        flat_prob = prob_grid.flatten()
        
        sort_idx = np.argsort(flat_dist)
        sorted_dist = flat_dist[sort_idx]
        sorted_prob = flat_prob[sort_idx]
        
        cum_prob = np.cumsum(sorted_prob)
        
        idx = np.searchsorted(cum_prob, alpha)
        if idx >= len(sorted_dist):
            idx = len(sorted_dist) - 1
            
        return sorted_dist[idx]
