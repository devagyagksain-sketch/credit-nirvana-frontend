from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict
import uvicorn
import math

app = FastAPI()

class AddressRequest(BaseModel):
    raw_address: str

# Base coordinates (e.g., center of Bangalore) to map synthetic Cartesian (x,y) to real-world GPS
BASE_LAT = 12.9716
BASE_LNG = 77.5946
METERS_PER_DEG_LAT = 111320
METERS_PER_DEG_LNG = 111320 * math.cos(math.radians(BASE_LAT))

@app.post("/api/geocode")
def geocode(req: AddressRequest):
    res = predict(req.raw_address, address_id="API_REQ")
    
    # Use math engine to determine coordinate and confidence radius
    from math_engine import calculate_prediction
    best_x, best_y, confidence_radius, confidence_score = calculate_prediction(res, confidence_level=0.80)

    # 2. Convert Synthetic Cartesian (x, y) meters to Real GPS Lat/Lng for Leaflet Map
    if best_x is not None and best_y is not None:
        # y represents North/South (Latitude offset)
        final_lat = BASE_LAT + (best_y / METERS_PER_DEG_LAT)
        # x represents East/West (Longitude offset)
        final_lng = BASE_LNG + (best_x / METERS_PER_DEG_LNG)
    else:
        # Fallback if nothing was found
        final_lat = BASE_LAT
        final_lng = BASE_LNG
        confidence_radius = 5000
        confidence_score = "Low"

    landmarks = res.get("landmarks", [])
    landmark_names = [lm["landmark_name"] for lm in landmarks]
    
    return {
        "latitude": final_lat,
        "longitude": final_lng,
        "confidence_radius": confidence_radius,
        "confidence_score": confidence_score,
        "cleaned_address": res["raw_address"],
        "extracted_locality": res.get("locality_name", "Locality not found"),
        "transliteration": res.get("town_name", ""),
        "landmarks": landmark_names,
        "cartesian_x": best_x,
        "cartesian_y": best_y
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
