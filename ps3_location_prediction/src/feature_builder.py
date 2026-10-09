import pandas as pd
import numpy as np

def extract_trail_features(gps_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates trail displacement, path length, and tortuosity."""
    # Ensure sequential order
    gps_df = gps_df.sort_values(['visit_id', 'seq'])
    
    # Calculate step distances between consecutive GPS points
    gps_df['step_x'] = gps_df.groupby('visit_id')['x'].diff()
    gps_df['step_y'] = gps_df.groupby('visit_id')['y'].diff()
    gps_df['step_dist'] = np.hypot(gps_df['step_x'], gps_df['step_y'])
    
    # Aggregate trail statistics
    agg = gps_df.groupby('visit_id').agg(
        trail_n_points=('seq', 'size'),
        trail_path_len=('step_dist', 'sum'),
        start_x=('x', 'first'),
        start_y=('y', 'first'),
        end_x=('x', 'last'),
        end_y=('y', 'last')
    )
    
    # Calculate total straight-line displacement
    agg['trail_displacement'] = np.hypot(agg['end_x'] - agg['start_x'], agg['end_y'] - agg['start_y'])
    
    # Calculate tortuosity (path length / displacement)
    # Clip displacement at 1.0 to avoid division by zero for stationary trails
    agg['trail_tortuosity'] = agg['trail_path_len'] / agg['trail_displacement'].clip(lower=1.0)
    
    return agg.reset_index()

def extract_integrity_features(visits_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates photo hash reuse, agent hotspots, and remark contradictions."""
    df = visits_df.copy()
    
    # 1. Photo Hash Reuse Count
    ph_counts = df['photo_hash'].value_counts()
    df['photo_hash_reuse_count'] = df['photo_hash'].map(ph_counts)
    
    # 2. Agent Hotspot Score
    # Bin check-ins into 25m x 25m grid cells
    df['cell_x'] = (df['checkin_x'] / 25.0).round() * 25
    df['cell_y'] = (df['checkin_y'] / 25.0).round() * 25
    
    # Count unique addresses an agent visited from this exact 25m cell
    hotspots = df.groupby(['agent_id', 'cell_x', 'cell_y'])['address_id'].nunique().reset_index()
    hotspots.rename(columns={'address_id': 'agent_hotspot_score'}, inplace=True)
    
    df = df.merge(hotspots, on=['agent_id', 'cell_x', 'cell_y'], how='left')
    
    # 3. Remark Outcome Contradiction
    # Basic logic: If marked as met/reached door, but remark says locked/not found
    contradiction_keywords = ['band', 'lock', 'nahi', 'illa', 'shifted', 'khaali', 'not traceable']
    is_met = df['outcome'].isin(['met_borrower', 'met_family'])
    has_negative_remark = df['remark'].str.lower().str.contains('|'.join(contradiction_keywords), na=False)
    
    df['remark_outcome_contradiction'] = (is_met & has_negative_remark).astype(int)
    
    # 4. Agent tenure (join from agents if provided here, or leave for upstream merge)
    
    return df

def build_all_visit_features(visits_df: pd.DataFrame, gps_df: pd.DataFrame, agents_df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Main entry point for calculating visit-level features for the Trust Model.
    """
    trail_features = extract_trail_features(gps_df)
    
    # Merge trail features into visits
    enriched_visits = visits_df.merge(trail_features, on='visit_id', how='left')
    
    # Add integrity features
    enriched_visits = extract_integrity_features(enriched_visits)
    
    # Add agent tenure if available
    if agents_df is not None:
        enriched_visits = enriched_visits.merge(agents_df[['agent_id', 'tenure_months']], on='agent_id', how='left')
        enriched_visits['tenure_months'] = enriched_visits['tenure_months'].fillna(enriched_visits['tenure_months'].median())
    
    return enriched_visits
