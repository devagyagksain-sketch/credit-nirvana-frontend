import numpy as np
import pandas as pd
from src.prior_model import SpatialPrior
from src.likelihood import VisitLikelihood

class BayesianFuser:
    @staticmethod
    def fuse(geocoder_x, geocoder_y, precision, visits_df, grid_radius=2000, step=15):
        X, Y, prob_grid = SpatialPrior.get_prior_grid(geocoder_x, geocoder_y, precision, grid_radius, step)
        
        for _, visit in visits_df.iterrows():
            if pd.isna(visit['checkin_x']) or pd.isna(visit['checkin_y']):
                continue
                
            if visit['outcome'] == 'address_not_traceable':
                sigma = max(visit['gps_accuracy_m'], 50.0)
                dist_sq = (X - visit['checkin_x'])**2 + (Y - visit['checkin_y'])**2
                penalty = 1.0 - 0.9 * np.exp(-dist_sq / (2 * sigma**2))
                prob_grid *= penalty
            else:
                L = VisitLikelihood.compute(
                    X, Y, 
                    visit['checkin_x'], 
                    visit['checkin_y'], 
                    visit['gps_accuracy_m'], 
                    visit.get('trust_pi', 1.0)
                )
                prob_grid *= L
                
            if prob_grid.sum() > 0:
                prob_grid /= prob_grid.sum()
                
        if prob_grid.sum() == 0:
            return geocoder_x, geocoder_y, prob_grid, X, Y
            
        max_idx = np.unravel_index(np.argmax(prob_grid), prob_grid.shape)
        pred_x = X[max_idx]
        pred_y = Y[max_idx]
        
        return pred_x, pred_y, prob_grid, X, Y
