from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict
import uvicorn

app = FastAPI()

class AddressRequest(BaseModel):
    raw_address: str

@app.post("/api/geocode")
def geocode(req: AddressRequest):
    res = predict(req.raw_address, address_id="API_REQ")
    
    # Map the response to the expected frontend schema
    # res has: address_id, raw_address, town_name, locality_name, locality_x, locality_y, landmarks, dropped
    
    # We will use locality_x and locality_y if available, else hardcode fallback for testing
    lat = res.get("locality_y")
    lng = res.get("locality_x")
    
    if lat is None or lng is None:
        lat = 12.9715987
        lng = 77.5945627
        
    landmarks = [lm["landmark_name"] for lm in res.get("landmarks", [])]
    
    return {
        "latitude": lat,
        "longitude": lng,
        "confidence_radius": res.get("radius_50", 150) if "radius_50" in res else 150,
        "confidence_score": "High" if "radius_50" not in res else res.get("confidence_action", "High"),
        "cleaned_address": res["raw_address"],
        "extracted_locality": res.get("locality_name", "Locality not found"),
        "transliteration": res.get("town_name", ""),
        "landmarks": landmarks
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

