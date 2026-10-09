import sys
import os
sys.path.append(os.path.abspath('ps3_location_prediction'))

from src.data_loader import DataLoader
from src.feature_builder import build_all_visit_features
from src.visit_trust import VisitTrustModel
from src.baselines import VisitBaselines

print("Loading data & extracting features...")
data = DataLoader(ps3_dir="ps-3", shared_dir="shared ").load_all()
enriched_visits = build_all_visit_features(data['visits'], data['gps_points'], data['agents'])

print("\n3. Testing Visit Trust Model (Phase 4)...")
trust_model = VisitTrustModel()
trust_model.fit(enriched_visits)
enriched_visits['trust_pi'] = trust_model.predict_trust_score(enriched_visits)
print("Trust scores generated. Sample:")
print(enriched_visits[['visit_id', 'photo_hash_reuse_count', 'trust_pi']].head())

print("\n4. Testing Robust Baselines (Phase 5)...")
# Filter for just one address with multiple visits
addr_group = enriched_visits[enriched_visits['address_id'] == 'AD001646']
if len(addr_group) > 0:
    print(f"Address AD001646 has {len(addr_group)} visits.")
    print("Mean:", VisitBaselines.mean_estimator(addr_group))
    print("Median:", VisitBaselines.median_estimator(addr_group))
    print("Geo-Median:", VisitBaselines.geometric_median_estimator(addr_group))
    print("Weighted:", VisitBaselines.weighted_estimator(addr_group))
else:
    print("Skipping aggregation (no visits for test address).")

print("\nSUCCESS: Phases 4 & 5 executed without errors.")
