"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Circle, Popup, ZoomControl, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix Leaflet's default icon path issues with bundlers
const icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

interface MapProps {
  lat: any;
  lng: any;
  radius: any;
}

function MapUpdater({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap();
  useEffect(() => {
    if (lat && lng) {
      map.flyTo([lat, lng], 16, { animate: true });
    }
  }, [lat, lng, map]);
  return null;
}

export default function Map({ lat, lng, radius }: MapProps) {
  const parsedLat = parseFloat(lat);
  const parsedLng = parseFloat(lng);
  const parsedRadius = parseFloat(radius) || 150;

  useEffect(() => {
    // Ensure window is available
  }, []);

  return (
    <div className="w-full h-full z-0 relative">
      <MapContainer
        center={[parsedLat || 12.9715987, parsedLng || 77.5945627]}
        zoom={15}
        scrollWheelZoom={false}
        className="w-full h-full shadow-sm"
        zoomControl={false}
      >
        <MapUpdater lat={parsedLat} lng={parsedLng} />
        <ZoomControl position="bottomright" />
        <TileLayer
          attribution='&copy; OpenStreetMap'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {parsedLat && parsedLng && (
          <>
            <Marker position={[parsedLat, parsedLng]} icon={icon}>
              <Popup>Target Location</Popup>
            </Marker>
            <Circle
              center={[parsedLat, parsedLng]}
              radius={parsedRadius}
              pathOptions={{
                color: "blue",
                fillColor: "blue",
                fillOpacity: 0.2,
                weight: 2,
              }}
            />
          </>
        )}
      </MapContainer>
    </div>
  );
}
