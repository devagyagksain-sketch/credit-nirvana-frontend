import pandas as pd
import numpy as np
from src.bayesian_fusion import BayesianFuser
from src.confidence_region import ConfidenceRegion
from src.conformal import ConformalCalibrator
from src.visit_trust import VisitTrustModel
from src.feature_builder import build_all_visit_features
from src.upstream_interface import UpstreamAddressInterface

class LocationPredictor:
    """
    Main inference interface linking the entire PS-3 pipeline.
    """
    def __init__(self, trust_model: VisitTrustModel, calibrator_80: ConformalCalibrator, calibrator_90: ConformalCalibrator):
        self.trust_model = trust_model
        self.calibrator_80 = calibrator_80
        self.calibrator_90 = calibrator_90

    def predict(self, address_features: pd.DataFrame, geocoder_data: pd.DataFrame, gps_points: pd.DataFrame, visits_data: pd.DataFrame) -> dict:
        
        geocoder_x = geocoder_data['geocoder_x'].iloc[0]
        geocoder_y = geocoder_data['geocoder_y'].iloc[0]
        precision = geocoder_data['precision'].iloc[0]
        
        # 1. Feature Engineering & Trust (If visits exist)
        if len(visits_data) > 0:
            enriched_visits = build_all_visit_features(visits_data, gps_points)
            enriched_visits['trust_pi'] = self.trust_model.predict_trust_score(enriched_visits)
            
            # Count useful door-reached visits
            door_outcomes = ['met_borrower', 'met_family', 'locked_premises', 'neighbour_says_shifted', 'cash_collected']
            useful = enriched_visits[enriched_visits['outcome'].isin(door_outcomes)]
            num_useful = len(useful)
            trusted_fraction = (useful['trust_pi'] > 0.5).mean() if num_useful > 0 else 0.0
        else:
            enriched_visits = pd.DataFrame()
            num_useful = 0
            trusted_fraction = 0.0
            
        # 2. Bayesian Fusion
        pred_x, pred_y, prob_grid, X, Y = BayesianFuser.fuse(
            geocoder_x,
            geocoder_y,
            precision,
            enriched_visits,
            grid_radius=2000,
            step=25  # Increased step slightly for speed in prediction loop
        )
        
        # 3. Confidence Region (Raw)
        raw_r80 = ConfidenceRegion.compute_radius_from_grid(X, Y, prob_grid, pred_x, pred_y, 0.8)
        raw_r90 = ConfidenceRegion.compute_radius_from_grid(X, Y, prob_grid, pred_x, pred_y, 0.9)
        
        # 4. Conformal Calibration
        calibrated_r80 = self.calibrator_80.adjust_radius(raw_r80)
        calibrated_r90 = self.calibrator_90.adjust_radius(raw_r90)
        
        # 5. Explanatory Context
        if num_useful == 0:
            method_desc = "Bayesian Prior (Geocoder + Mapped Upstream Text) - No Visits"
        else:
            method_desc = f"Bayesian Fusion ({num_useful} door visits, {trusted_fraction*100:.0f}% trusted)"
            
        return {
            "predicted_x": pred_x,
            "predicted_y": pred_y,
            "confidence_level_80": 0.80,
            "raw_radius_80_m": raw_r80,
            "calibrated_radius_80_m": calibrated_r80,
            "confidence_level_90": 0.90,
            "raw_radius_90_m": raw_r90,
            "calibrated_radius_90_m": calibrated_r90,
            "num_visits": num_useful,
            "trusted_visit_fraction": trusted_fraction,
            "geocoder_precision": precision,
            "method": method_desc
        }
