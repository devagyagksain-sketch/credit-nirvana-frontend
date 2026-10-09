import pandas as pd
import numpy as np

class UpstreamAddressInterface:
    """
    INTERFACE STUB FOR THE UPSTREAM ADDRESS PARSING TEAM.
    
    DO NOT implement NLP here. This module simulates receiving 
    structured address features from the upstream NLP/Parsing team.
    
    The interface takes raw addresses and returns a dataframe of 
    structured spatial constraints.
    """
    
    @staticmethod
    def get_mock_structured_features(raw_addresses_df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates a mock dataframe representing what the other team will provide.
        """
        # We start with the address IDs to join back to our pipeline
        df = raw_addresses_df[['address_id', 'town_id']].copy()
        
        # 1. Text Completeness (0.0 to 1.0)
        np.random.seed(42)
        df['struct_text_completeness'] = np.random.uniform(0.3, 1.0, size=len(df))
        
        # 2. Extracted Landmark Type (mocking based on random choice)
        landmark_types = ['temple', 'masjid', 'school', 'water_tank', 'ration_shop', 'none']
        df['struct_landmark_type'] = np.random.choice(landmark_types, size=len(df))
        
        # 3. Extracted Spatial Relation (e.g., behind, opposite, near)
        relations = ['near', 'behind', 'opposite', 'none']
        df['struct_spatial_relation'] = np.random.choice(relations, size=len(df))
        
        # 4. Resolved Locality ID (mocking by appending '-L01' to town_id)
        df['struct_locality_id'] = df['town_id'] + "-L01"
        
        # 5. Street Tokens (e.g., '4th cross', 'gali no 3')
        df['struct_street_token'] = np.random.choice(['cross', 'main', 'gali', 'block', 'none'], size=len(df))
        
        return df
