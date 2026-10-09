import numpy as np

def convex_hull(points):
    """Computes the convex hull of a set of 2D points using Monotone Chain."""
    points = sorted(points, key=lambda p: (p[0], p[1]))
    if len(points) <= 1:
        return points

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def calculate_prediction(res, confidence_level=0.80):
    """
    Implements the Convex Hull + fuzzy boundary (Step 11 & 12 of Final Workflow)
    for the no-visit branch.
    """
    # 1. Collect evidence points
    points_data = []
    
    # Locality centroid
    loc_x = res.get("locality_x")
    loc_y = res.get("locality_y")
    if loc_x is not None and loc_y is not None:
        points_data.append({"x": loc_x, "y": loc_y, "sigma": 390.0, "type": "locality"})
        
    # Landmarks
    landmarks = res.get("landmarks", [])
    for lm in landmarks:
        poi_x = lm.get("poi_x")
        poi_y = lm.get("poi_y")
        if poi_x is not None and poi_y is not None:
            points_data.append({"x": poi_x, "y": poi_y, "sigma": 50.0, "type": "landmark"})
            
    if not points_data:
        return None, None, 5000.0, "Low"
        
    # z_alpha for normal quantile
    z_alpha_map = {0.80: 0.842, 0.90: 1.282, 0.95: 1.645}
    z_a = z_alpha_map.get(confidence_level, 0.842)
    
    n = len(points_data)
    
    if n == 1:
        # Fallback 1 point: use it directly
        best_x = points_data[0]["x"]
        best_y = points_data[0]["y"]
        radius = points_data[0]["sigma"] * z_a
        score = "High" if points_data[0]["type"] == "landmark" else "Medium"
        return float(best_x), float(best_y), float(radius), score
        
    elif n == 2:
        # Fallback 2 points: midpoint and widened radius
        p1, p2 = points_data[0], points_data[1]
        best_x = (p1["x"] + p2["x"]) / 2.0
        best_y = (p1["y"] + p2["y"]) / 2.0
        
        # distance between points
        dist = np.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])
        sigma_edge = (p1["sigma"] + p2["sigma"]) / 2.0
        d_edge = z_a * sigma_edge
        
        # radius is half distance plus the fuzzy boundary
        radius = (dist / 2.0) + d_edge
        score = "High"
        return float(best_x), float(best_y), float(radius), score
        
    else:
        # 3+ points: Convex Hull
        coords = [(p["x"], p["y"]) for p in points_data]
        
        # Check for collinearity / get hull
        hull_coords = convex_hull(coords)
        if len(hull_coords) <= 2:
            # Collinear fallback: just use bounding box or average
            best_x = np.mean([c[0] for c in coords])
            best_y = np.mean([c[1] for c in coords])
            max_dist = np.max([np.hypot(c[0] - best_x, c[1] - best_y) for c in coords])
            avg_sigma = np.mean([p["sigma"] for p in points_data])
            return float(best_x), float(best_y), float(max_dist + z_a * avg_sigma), "High"

        # Centroid of the hull vertices
        centroid_x = np.mean([c[0] for c in hull_coords])
        centroid_y = np.mean([c[1] for c in hull_coords])
        
        # Find sigma for each hull vertex based on original points
        hull_sigmas = []
        for hc in hull_coords:
            # find matching point
            for p in points_data:
                if p["x"] == hc[0] and p["y"] == hc[1]:
                    hull_sigmas.append(p["sigma"])
                    break
                    
        max_r = 0.0
        for i in range(len(hull_coords)):
            dist = np.hypot(hull_coords[i][0] - centroid_x, hull_coords[i][1] - centroid_y)
            vertex_sigma = hull_sigmas[i]
            r = dist + z_a * vertex_sigma
            if r > max_r:
                max_r = r
                
        # Applying conformal calibration as described in Step 13 (multiplier q)
        # Without a held-out set to learn q, we assume q=1.1 (slightly conservative)
        q = 1.1
        final_radius = max_r * q
        
        return float(centroid_x), float(centroid_y), float(final_radius), "High"

