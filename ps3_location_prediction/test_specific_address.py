import sys
from src.data_loader import DataLoader
from src.upstream_interface import UpstreamAddressInterface
from src.visit_trust import VisitTrustModel
from src.conformal import ConformalCalibrator
from src.inference import LocationPredictor
import warnings
warnings.filterwarnings('ignore')

print("Loading data into memory...")
data = DataLoader().load_all()

# Find the address ID containing '68' (we look for '068' to avoid matching '168' etc.)
matches = data['addresses'][data['addresses']['address_id'].str.contains('068', na=False)]
if len(matches) == 0:
    print("Could not find an address containing '68'.")
    sys.exit(1)

target_address = matches.iloc[0]['address_id']
print(f"\nTarget address found: {target_address}")

predictor = LocationPredictor(VisitTrustModel(), ConformalCalibrator(alpha=0.8), ConformalCalibrator(alpha=0.9))

addr_feats = UpstreamAddressInterface.get_mock_structured_features(data['addresses'][data['addresses']['address_id'] == target_address])
geo = data['geocodes'][data['geocodes']['address_id'] == target_address]
vis = data['visits'][data['visits']['address_id'] == target_address]

if len(geo) == 0:
    print("Error: No geocoder data found for this address. The model needs at least a prior.")
    sys.exit(1)

gps = data['gps_points'][data['gps_points']['visit_id'].isin(vis['visit_id'])] if len(vis) > 0 else []

print(f"Evidence found:")
print(f" - Geocoder Prior Precision: {geo.iloc[0]['precision'].upper()}")
print(f" - Number of Field Visits: {len(vis)}")
if len(vis) > 0:
    print(f" - Visit Outcomes: {vis['outcome'].tolist()}")

print("\nRunning Bayesian Fusion & Trust Model...")
result = predictor.predict(addr_feats, geo, gps, vis)

print("\n" + "="*40)
print("FINAL PREDICTION REPORT")
print("="*40)
for key, value in result.items():
    if isinstance(value, float):
        print(f"{key.replace('_', ' ').title().ljust(25)}: {value:.2f}")
    else:
        print(f"{key.replace('_', ' ').title().ljust(25)}: {value}")
print("="*40)
