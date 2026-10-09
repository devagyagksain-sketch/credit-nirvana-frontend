"use client";

import dynamic from "next/dynamic";
import { WifiOff, MapPin, Navigation, CheckCircle2, MessageSquare } from "lucide-react";

// Dynamic import for the Leaflet map (client-only)
const Map = dynamic(() => import("@/components/map/Map"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full bg-gray-100 flex items-center justify-center animate-pulse">
      <MapPin className="text-gray-400 w-10 h-10" />
    </div>
  ),
});

export default function AgentVisitPage() {
  const targetLocation = {
    lat: 12.9715987,
    lng: 77.5945627,
    radius: 150,
  };

  const addressData = {
    raw: "No 45, 2nd Cross, Opposite to Ganesh Temple, Marathahalli, Bangalore 560037",
    transliteration: "नं ४५, दूसरा क्रॉस, गणेश मंदिर के सामने, मराठहल्ली, बैंगलोर ५६००३७",
    landmarks: ["Opposite to Ganesh Temple"],
    confidence: "High (150m radius)",
  };

  return (
    <main className="flex flex-col md:flex-row h-screen bg-gray-50 font-sans overflow-hidden">
      
      {/* Left Sidebar (Address Details & Actions) */}
      <aside className="w-full md:w-[400px] lg:w-[450px] bg-white border-r border-gray-200 flex flex-col h-[50vh] md:h-full shadow-lg z-10 order-2 md:order-1">
        
        {/* Offline Mode Banner */}
        <div className="bg-emerald-600 text-white px-4 py-3 flex items-center justify-center gap-2 text-sm font-semibold shrink-0">
          <WifiOff className="w-4 h-4" />
          Offline Mode Ready
        </div>

        {/* Scrollable Content Area */}
        <div className="flex-1 overflow-y-auto p-5 md:p-6 flex flex-col gap-6">
          
          <div className="flex items-start gap-3">
            <div className="bg-blue-50 p-2.5 rounded-xl shrink-0 mt-1">
              <MapPin className="w-6 h-6 text-blue-600" />
            </div>
            
            <div className="flex-1 flex flex-col gap-4">
              {/* Title and Badge */}
              <div className="flex items-center justify-between">
                <h2 className="text-gray-900 font-bold text-xl leading-tight">
                  Target Address
                </h2>
                <span className="text-[10px] font-bold px-2.5 py-1 bg-green-100 text-green-700 rounded-full uppercase tracking-wider shrink-0 ml-2">
                  {addressData.confidence}
                </span>
              </div>
              
              {/* English Address */}
              <p className="text-gray-700 text-base leading-relaxed">
                {addressData.raw}
              </p>
              
              {/* Transliteration Block */}
              <div className="bg-gray-50 rounded-xl p-3.5 border border-gray-100">
                <span className="text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-2 block">
                  Transliteration
                </span>
                <p className="text-gray-800 text-[15px] font-medium leading-relaxed">
                  {addressData.transliteration}
                </p>
              </div>

              {/* Landmark Highlight */}
              {addressData.landmarks.length > 0 && (
                <div>
                  <span className="text-sm font-semibold text-amber-800 bg-amber-50 px-3 py-1.5 rounded-lg border border-amber-200 inline-block">
                    Landmark: {addressData.landmarks[0]}
                  </span>
                </div>
              )}
            </div>
          </div>

        </div>

        {/* Action Buttons (Sticky at bottom of sidebar) */}
        <div className="p-5 md:p-6 border-t border-gray-100 bg-white shrink-0 flex flex-col gap-3">
          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 px-4 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg shadow-blue-200/50 transition-all active:scale-[0.98]">
            <Navigation className="w-5 h-5" />
            Start GPS Trail
          </button>
          
          <div className="flex gap-3 mt-1">
            <button className="flex-1 bg-white hover:bg-gray-50 text-gray-700 py-3.5 px-4 rounded-xl font-bold flex items-center justify-center gap-2 border border-gray-200 shadow-sm transition-all active:scale-[0.98]">
              <MessageSquare className="w-5 h-5 text-gray-500" />
              <span className="text-sm">Remarks</span>
            </button>
            
            <button className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-3.5 px-4 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg shadow-emerald-200/50 transition-all active:scale-[0.98]">
              <CheckCircle2 className="w-5 h-5" />
              <span className="text-sm">Outcome</span>
            </button>
          </div>
        </div>

      </aside>

      {/* Right Panel (Map View) */}
      <section className="flex-1 h-[50vh] md:h-full relative z-0 order-1 md:order-2 bg-gray-200">
        <Map lat={targetLocation.lat} lng={targetLocation.lng} radius={targetLocation.radius} />
      </section>

    </main>
  );
}
