import sys
import os

# Ensure Python can find the src modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import DataLoader
from src.upstream_interface import UpstreamAddressInterface
from src.visit_trust import VisitTrustModel
from src.conformal import ConformalCalibrator
from src.inference import LocationPredictor
import warnings
warnings.filterwarnings('ignore') # Hide numpy math warnings

print("Loading AI Model and dataset into memory (this takes a few seconds)...")
data = DataLoader().load_all()
predictor = LocationPredictor(VisitTrustModel(), ConformalCalibrator(alpha=0.8), ConformalCalibrator(alpha=0.9))
print("Ready!\n")

while True:
    user_input = input("Enter an Address ID (e.g., 68, 527, AD000123) or type 'exit' to quit: ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'q']:
        print("Goodbye!")
        break
        
    if not user_input:
        continue
        
    # Search for the address
    matches = data['addresses'][data['addresses']['address_id'].str.contains(user_input, na=False, case=False)]
    if len(matches) == 0:
        print(f"❌ Could not find any address matching '{user_input}'. Try another.\n")
        continue
        
    target_address = matches.iloc[0]['address_id']
    print(f"\n🔍 Found Address: {target_address}")
    
    addr_feats = UpstreamAddressInterface.get_mock_structured_features(data['addresses'][data['addresses']['address_id'] == target_address])
    geo = data['geocodes'][data['geocodes']['address_id'] == target_address]
    vis = data['visits'][data['visits']['address_id'] == target_address]
    
    if len(geo) == 0:
        print("❌ No geocoder prior data found for this address. Cannot predict.\n")
        continue
        
    gps = data['gps_points'][data['gps_points']['visit_id'].isin(vis['visit_id'])] if len(vis) > 0 else []

    print(f"Evidence: Geocoder Precision [{geo.iloc[0]['precision'].upper()}], Field Visits [{len(vis)}]")
    if len(vis) > 0:
        print(f"Visit Outcomes: {vis['outcome'].tolist()}")
    
    print("Calculating Bayesian Fusion...")
    result = predictor.predict(addr_feats, geo, gps, vis)
    
    print("-" * 40)
    for key, value in result.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title().ljust(25)}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title().ljust(25)}: {value}")
    print("-" * 40 + "\n")
