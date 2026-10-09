import sys
import os
sys.path.append(os.path.abspath('ps3_location_prediction'))

from src.data_loader import DataLoader
from src.upstream_interface import UpstreamAddressInterface
from src.feature_builder import build_all_visit_features
import pandas as pd

print("Loading data...")
loader = DataLoader(ps3_dir="ps-3", shared_dir="shared ")
data = loader.load_all()

print("1. Testing Upstream Address Interface (Phase 2)...")
mock_upstream_features = UpstreamAddressInterface.get_mock_structured_features(data['addresses'])
print(f"Mock generated for {len(mock_upstream_features)} addresses.")
print("Sample of mock structured features:")
print(mock_upstream_features[['address_id', 'struct_locality_id', 'struct_landmark_type']].head(3).to_string())

print("\n2. Testing Visit Feature Builder (Phase 3)...")
enriched_visits = build_all_visit_features(data['visits'], data['gps_points'], data['agents'])
print(f"Features built for {len(enriched_visits)} visits.")
print("Sample of enriched visit features:")
print(enriched_visits[['visit_id', 'trail_displacement', 'trail_tortuosity', 'photo_hash_reuse_count', 'agent_hotspot_score', 'remark_outcome_contradiction']].head(5).to_string())

print("\nSUCCESS: Phases 2 & 3 executed without errors.")
