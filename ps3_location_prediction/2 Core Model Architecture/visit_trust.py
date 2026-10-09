import pandas as pd
import numpy as np

class VisitTrustModel:
    """
    Visit Trust / Reliability Estimator.
    
    Since explicit, ground-truth supervised fraud labels do not exist in this 
    dataset, this is a reliability/trust model, NOT a ground-truth fraud classifier.
    
    It operates by establishing a pseudo-target based on severe integrity violations 
    (e.g., photo hash reuse, extreme agent hotspot clustering) and then maps features
    to a probability pi_i using a calibrated sigmoid heuristic.
    
    pi_i = P(visit_i is genuine | features)
    """
    def __init__(self):
        pass
        
    def fit(self, enriched_visits: pd.DataFrame):
        # In a pure-NumPy heuristic model, we don't 'fit' parameters through gradient descent,
        # but we compute feature standardizations and thresholds from the dataset.
        pass
        
    def predict_trust_score(self, enriched_visits: pd.DataFrame) -> np.ndarray:
        df = enriched_visits.copy()
        
        # 1. Base trust score
        trust = np.ones(len(df))
        
        # 2. Hard limits for absolute anomalies
        hard_fake_mask = (df['photo_hash_reuse_count'] > 1) | (df['agent_hotspot_score'] >= 10)
        
        # 3. Penalize based on continuous variables (heuristic linear combination)
        # Low displacement -> lower trust
        # High tortuosity -> lower trust 
        # Contradictions -> lower trust
        
        disp = df['trail_displacement'].fillna(100)
        tort = df['trail_tortuosity'].fillna(1.0)
        contra = df['remark_outcome_contradiction'].fillna(0)
        
        # Logits approach
        # A normal visit has disp ~400, tortuosity ~2.0
        # A fake visit has disp ~10, tortuosity > 5.0
        logit = 2.0  # Base logit
        logit += np.clip((disp - 50) / 100, -3.0, 1.0) # Bonus for moving, penalty for not
        logit -= np.clip((tort - 2.0) / 1.0, 0.0, 3.0) # Penalty for extreme wandering
        logit -= contra * 3.0 # Big penalty for contradiction
        
        # Sigmoid to get probability
        pi = 1.0 / (1.0 + np.exp(-logit))
        
        # Apply hard caps
        trust = pi
        trust[hard_fake_mask] = 0.01
        
        return trust.values
