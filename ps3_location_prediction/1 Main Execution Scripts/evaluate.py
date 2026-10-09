import sys
import os
import numpy as np
import pandas as pd

from src.data_loader import DataLoader
from src.upstream_interface import UpstreamAddressInterface
from src.visit_trust import VisitTrustModel
from src.conformal import ConformalCalibrator
from src.inference import LocationPredictor

def run_evaluation():
    print("Loading data...")
    loader = DataLoader()
    data = loader.load_all()
    
    # Isolate surveyed addresses for evaluation
    surveyed = data['surveyed']
    
    # We will use 50% for calibration, 50% for evaluation/testing
    np.random.seed(42)
    calib_idx = np.random.choice(surveyed.index, size=len(surveyed)//2, replace=False)
    test_idx = surveyed.index.difference(calib_idx)
    
    calib_set = surveyed.loc[calib_idx]
    test_set = surveyed.loc[test_idx]
    
    print(f"Calibration Set Size: {len(calib_set)}")
    print(f"Test Set Size: {len(test_set)}")
    
    # Initialize uncalibrated predictor
    trust_model = VisitTrustModel()
    dummy_calib_80 = ConformalCalibrator(alpha=0.8)
    dummy_calib_90 = ConformalCalibrator(alpha=0.9)
    predictor = LocationPredictor(trust_model, dummy_calib_80, dummy_calib_90)
    
    # Collect raw predictions on the calibration set
    calib_errors = []
    calib_raw_r80 = []
    calib_raw_r90 = []
    
    print("Running Bayesian Fusion on Calibration Set...")
    for _, row in calib_set.iterrows():
        addr_id = row['address_id']
        
        # Subselect data
        addr_feats = UpstreamAddressInterface.get_mock_structured_features(data['addresses'][data['addresses']['address_id'] == addr_id])
        geo = data['geocodes'][data['geocodes']['address_id'] == addr_id]
        if len(geo) == 0:
            continue
            
        vis = data['visits'][data['visits']['address_id'] == addr_id]
        gps = data['gps_points'][data['gps_points']['visit_id'].isin(vis['visit_id'])] if len(vis) > 0 else pd.DataFrame()
        
        res = predictor.predict(addr_feats, geo, gps, vis)
        
        err = np.hypot(res['predicted_x'] - row['surveyed_x'], res['predicted_y'] - row['surveyed_y'])
        calib_errors.append(err)
        calib_raw_r80.append(res['raw_radius_80_m'])
        calib_raw_r90.append(res['raw_radius_90_m'])
        
    # Fit the calibrators
    calib_80 = ConformalCalibrator(alpha=0.8)
    calib_80.calibrate(np.array(calib_errors), np.array(calib_raw_r80))
    
    calib_90 = ConformalCalibrator(alpha=0.9)
    calib_90.calibrate(np.array(calib_errors), np.array(calib_raw_r90))
    
    print(f"Calibration complete. Multiplier 80%: {calib_80.q_hat:.2f}, Multiplier 90%: {calib_90.q_hat:.2f}")
    
    # Now evaluate on Test Set
    predictor = LocationPredictor(trust_model, calib_80, calib_90)
    
    test_errors = []
    r80s = []
    r90s = []
    covered_80 = []
    covered_90 = []
    
    print("Evaluating fully calibrated system on Test Set...")
    for _, row in test_set.iterrows():
        addr_id = row['address_id']
        addr_feats = UpstreamAddressInterface.get_mock_structured_features(data['addresses'][data['addresses']['address_id'] == addr_id])
        geo = data['geocodes'][data['geocodes']['address_id'] == addr_id]
        if len(geo) == 0:
            continue
            
        vis = data['visits'][data['visits']['address_id'] == addr_id]
        gps = data['gps_points'][data['gps_points']['visit_id'].isin(vis['visit_id'])] if len(vis) > 0 else pd.DataFrame()
        
        res = predictor.predict(addr_feats, geo, gps, vis)
        
        err = np.hypot(res['predicted_x'] - row['surveyed_x'], res['predicted_y'] - row['surveyed_y'])
        test_errors.append(err)
        
        r80 = res['calibrated_radius_80_m']
        r90 = res['calibrated_radius_90_m']
        
        r80s.append(r80)
        r90s.append(r90)
        
        covered_80.append(1 if err <= r80 else 0)
        covered_90.append(1 if err <= r90 else 0)

    print("\n" + "="*40)
    print("FINAL TEST SET METRICS (BAYESIAN FUSION)")
    print("="*40)
    print(f"Median Error:      {np.median(test_errors):.1f} m")
    print(f"Mean Error:        {np.mean(test_errors):.1f} m")
    print(f"P90 Error:         {np.percentile(test_errors, 90):.1f} m")
    print("-" * 40)
    print(f"Target 80% Coverage: {np.mean(covered_80)*100:.1f}%")
    print(f"Median 80% Radius:   {np.nanmedian(r80s):.1f} m")
    print("-" * 40)
    print(f"Target 90% Coverage: {np.mean(covered_90)*100:.1f}%")
    print(f"Median 90% Radius:   {np.nanmedian(r90s):.1f} m")
    print("="*40)

if __name__ == '__main__':
    run_evaluation()
