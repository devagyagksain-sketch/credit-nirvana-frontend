import numpy as np

class SpatialPrior:
    @staticmethod
    def get_precision_sigma(precision: str) -> float:
        mapping = {
            'rooftop': 25.0,
            'street': 110.0,
            'locality': 390.0,
            'pincode': 1400.0
        }
        return mapping.get(precision, 400.0)
        
    @staticmethod
    def get_prior_grid(geocoder_x, geocoder_y, precision, grid_radius=2000, step=25):
        sigma = SpatialPrior.get_precision_sigma(precision)
        
        x = np.arange(geocoder_x - grid_radius, geocoder_x + grid_radius, step)
        y = np.arange(geocoder_y - grid_radius, geocoder_y + grid_radius, step)
        X, Y = np.meshgrid(x, y)
        
        exponent = -((X - geocoder_x)**2 + (Y - geocoder_y)**2) / (2 * sigma**2)
        prior_prob = np.exp(exponent)
        
        if prior_prob.sum() > 0:
            prior_prob /= prior_prob.sum()
            
        return X, Y, prior_prob
