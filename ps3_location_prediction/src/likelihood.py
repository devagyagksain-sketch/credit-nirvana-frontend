import numpy as np

class VisitLikelihood:
    @staticmethod
    def compute(X, Y, checkin_x, checkin_y, gps_accuracy, trust_pi, outlier_prob=1e-7):
        sigma = max(gps_accuracy, 5.0) 
        
        exponent = -((X - checkin_x)**2 + (Y - checkin_y)**2) / (2 * sigma**2)
        norm_const = 1.0 / (2 * np.pi * sigma**2)
        inlier_likelihood = norm_const * np.exp(exponent)
        
        likelihood = trust_pi * inlier_likelihood + (1 - trust_pi) * outlier_prob
        return likelihood
