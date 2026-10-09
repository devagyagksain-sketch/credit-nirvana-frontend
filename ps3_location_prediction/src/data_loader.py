import os
import pandas as pd

class DataLoader:
    def __init__(self, ps3_dir=None, shared_dir=None):
        # Dynamically resolve the parent directory (OPEN IIT) regardless of where the script is run
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        self.ps3_dir = ps3_dir or os.path.join(base_dir, "ps-3")
        self.shared_dir = shared_dir or os.path.join(base_dir, "shared ")

    def load_all(self):
        """Loads all relevant CSV files for PS-3 Location Prediction."""
        
        # 1. Ground Truth
        surveyed = pd.read_csv(os.path.join(self.ps3_dir, "surveyed_addresses.csv"))
        
        # 2. Prior / Geocoder Information
        geocodes = pd.read_csv(os.path.join(self.ps3_dir, "baseline_geocodes (1).csv"))
        
        # 3. Visit Evidence
        gps_points = pd.read_csv(os.path.join(self.ps3_dir, "visit_gps_points.csv"))
        # Using only one of the duplicate field_visits files
        visits = pd.read_csv(os.path.join(self.shared_dir, "field_visits.csv"))
        
        # 4. Spatial Context
        landmarks = pd.read_csv(os.path.join(self.ps3_dir, "landmarks_poi.csv"))
        localities = pd.read_csv(os.path.join(self.ps3_dir, "localities.csv"))
        towns = pd.read_csv(os.path.join(self.ps3_dir, "towns.csv"))
        
        # 5. Accounts & Cross-references
        accounts = pd.read_csv(os.path.join(self.shared_dir, "accounts.csv"))
        agents = pd.read_csv(os.path.join(self.shared_dir, "agents.csv"))
        addresses = pd.read_csv(os.path.join(self.shared_dir, "addresses.csv"))
        splits = pd.read_csv(os.path.join(self.shared_dir, "splits.csv"))
        
        return {
            "surveyed": surveyed,
            "geocodes": geocodes,
            "gps_points": gps_points,
            "visits": visits,
            "landmarks": landmarks,
            "localities": localities,
            "towns": towns,
            "accounts": accounts,
            "agents": agents,
            "addresses": addresses,
            "splits": splits
        }
