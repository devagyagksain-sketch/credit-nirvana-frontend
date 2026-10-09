"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { 
  BarChart3, 
  MapPin, 
  Users, 
  Settings, 
  ShieldAlert,
  ArrowDownRight,
  TrendingDown,
  Navigation,
  MessageSquare,
  CheckCircle2,
  Search,
  WifiOff,
  AlertCircle
} from "lucide-react";
import { GeocodingQualityChart, TerritoryTrendsChart } from "@/components/charts/DashboardCharts";

// Dynamic import for the Map to prevent SSR issues
const Map = dynamic(() => import("@/components/map/Map"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full bg-slate-100 flex items-center justify-center animate-pulse">
      <MapPin className="text-slate-400 w-10 h-10" />
    </div>
  ),
});

export default function UnifiedApp() {
  const [activeTab, setActiveTab] = useState("dispatcher");
  
  return (
    <div className="flex h-screen w-full overflow-hidden">
      
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col h-full border-r border-slate-800 shrink-0 z-20">
        <div className="p-4">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <span className="w-8 h-8 rounded bg-teal-600 flex items-center justify-center text-sm">CN</span>
            CreditNirvana
          </h1>
        </div>
        
        <nav className="flex-1 px-4 py-4 space-y-2">
          <button 
            onClick={() => setActiveTab("dispatcher")}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
              activeTab === "dispatcher" ? "bg-slate-800 text-white font-medium border border-slate-700" : "hover:bg-slate-800 hover:text-white text-slate-300"
            }`}
          >
            <MapPin className={`w-5 h-5 ${activeTab === "dispatcher" ? "text-teal-400" : ""}`} />
            Visit Dispatcher
          </button>
          
          <button 
            onClick={() => setActiveTab("metrics")}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
              activeTab === "metrics" ? "bg-slate-800 text-white font-medium border border-slate-700" : "hover:bg-slate-800 hover:text-white text-slate-300"
            }`}
          >
            <BarChart3 className={`w-5 h-5 ${activeTab === "metrics" ? "text-teal-400" : ""}`} />
            Performance Metrics
          </button>
          
          <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-colors text-slate-300">
            <Users className="w-5 h-5" />
            Field Agents
          </button>
          <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-800 hover:text-white transition-colors text-slate-300">
            <Settings className="w-5 h-5" />
            Settings
          </button>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col bg-gray-50 h-full overflow-y-auto">
        {activeTab === "metrics" ? <PerformanceMetricsView /> : <VisitDispatcherView />}
      </main>
      
    </div>
  );
}

function PerformanceMetricsView() {
  return (
    <div className="flex-1 flex flex-col">
      {/* Compliance & Governance Banner */}
      <div className="bg-amber-50 border-b border-amber-200 px-6 py-3 flex items-center gap-3 shrink-0">
        <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0" />
        <p className="text-sm font-medium text-amber-900">
          <strong>Restricted Access:</strong> Location data is strictly siloed for field operations and governed by DPDP retention limits.
        </p>
      </div>

      <div className="p-8 max-w-7xl mx-auto w-full flex-1">
        <header className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900">Metrics & Analytics</h2>
          <p className="text-slate-500 mt-1">Monitor geocoding accuracy and field visit performance.</p>
        </header>

        {/* KPI Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Median Distance Error</h3>
            <div className="flex items-end gap-4">
              <span className="text-4xl font-bold text-slate-900">12m</span>
              <div className="flex items-center text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md text-sm font-medium mb-1">
                <ArrowDownRight className="w-4 h-4 mr-1" />
                -4m
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Address Not Traceable Rate</h3>
            <div className="flex items-end gap-4">
              <span className="text-4xl font-bold text-slate-900">4.2%</span>
              <div className="flex items-center text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md text-sm font-medium mb-1">
                <TrendingDown className="w-4 h-4 mr-1" />
                -1.5%
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Confirmed Pin Updates</h3>
            <div className="flex items-end gap-4">
              <span className="text-4xl font-bold text-slate-900">14,259</span>
              <div className="flex items-center text-slate-500 bg-slate-100 px-2 py-1 rounded-md text-sm font-medium mb-1">
                Total
              </div>
            </div>
          </div>
        </div>

        {/* Performance Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
            <h3 className="text-lg font-bold text-slate-900 mb-6">Geocoding Quality Improvement</h3>
            <GeocodingQualityChart />
          </div>
          <div className="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
            <h3 className="text-lg font-bold text-slate-900 mb-6">"Not Traceable" Outcomes by Territory</h3>
            <TerritoryTrendsChart />
          </div>
        </div>
      </div>
    </div>
  );
}

function VisitDispatcherView() {
  const [addressInput, setAddressInput] = useState("");
  const [isDispatched, setIsDispatched] = useState(false);
  const [isGeocoding, setIsGeocoding] = useState(false);
  const [error, setError] = useState("");
  const [geocodedData, setGeocodedData] = useState<any>(null);

  const handleDispatch = async () => {
    if (!addressInput.trim()) return;
    setIsGeocoding(true);
    setError("");
    
    try {
      const response = await fetch("/api/geocode", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ raw_address: addressInput }),
      });
      
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      
      const data = await response.json();
      setGeocodedData(data);
      setIsDispatched(true);
    } catch (err) {
      console.error(err);
      setError("Backend connection failed. Ensure the Address-Parser model is running on port 8000.");
    } finally {
      setIsGeocoding(false);
    }
  };

  if (!isDispatched) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8">
        <div className="max-w-xl w-full">
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-3">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          <div className="bg-white p-8 rounded-lg shadow-sm border border-slate-200 text-center transition-all">
            <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <MapPin className="w-8 h-8 text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Visit Dispatcher</h2>
            <p className="text-slate-500 mb-8">Enter a raw field address to geocode and dispatch an agent visit.</p>
            
            <div className="flex flex-col gap-4">
              <div className="relative">
                <Search className="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Enter Raw Field Address..."
                  value={addressInput}
                  onChange={(e) => setAddressInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleDispatch()}
                  className="w-full pl-12 pr-4 py-4 rounded-lg border border-slate-300 bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-slate-900 font-medium"
                />
              </div>
              <button
                onClick={handleDispatch}
                disabled={isGeocoding || !addressInput.trim()}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white py-4 rounded-lg font-bold shadow-md transition-all flex items-center justify-center gap-2"
              >
                {isGeocoding ? (
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <>
                    <Navigation className="w-5 h-5" />
                    Geocode & Dispatch
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const targetLocation = {
    lat: geocodedData?.latitude || 12.9715987,
    lng: geocodedData?.longitude || 77.5945627,
    radius: geocodedData?.confidence_radius || 150,
  };

  const confidenceScore = geocodedData?.confidence_score || `High`;
  const cleanedAddress = geocodedData?.cleaned_address || addressInput;
  const transliteration = geocodedData?.transliteration || "Transliteration not provided by backend";
  
  // Fix the repeating landmark bug with a Set
  const rawLandmarks = geocodedData?.landmarks || ["Opposite to Ganesh Temple"];
  const uniqueLandmarks = [...new Set<string>(rawLandmarks)];

  return (
    <div className="flex-1 flex flex-col md:flex-row h-full">
      <aside className="w-full md:w-[450px] lg:w-[480px] bg-white border-r border-slate-200 flex flex-col h-full shadow-sm z-10 shrink-0">
        <div className="bg-emerald-600 text-white px-4 py-3 flex items-center justify-center gap-2 text-sm font-semibold shrink-0">
          <WifiOff className="w-4 h-4" />
          Offline Mode Ready
        </div>

        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-5">
          <button 
            onClick={() => setIsDispatched(false)}
            className="text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-1 w-fit -mt-2 mb-2"
          >
            ← Back to Search
          </button>

          <div className="flex items-start gap-3">
            <div className="bg-blue-50 p-2.5 rounded-lg shrink-0 mt-1">
              <MapPin className="w-6 h-6 text-blue-600" />
            </div>
            
            <div className="flex-1 flex flex-col gap-4">
              <div className="flex items-center justify-between gap-2">
                <h2 className="text-slate-900 font-bold text-xl leading-tight">Target Address</h2>
                <span className="text-[10px] font-bold px-2.5 py-1 bg-green-100 text-green-700 rounded-full uppercase tracking-wider shrink-0 whitespace-nowrap">
                  {confidenceScore} Confidence
                </span>
              </div>
              
              <p className="text-slate-700 text-[15px] leading-relaxed font-medium">
                {cleanedAddress}
              </p>
              
              {/* Added explicit problem statement data points */}
              <div className="flex flex-col gap-2 mt-2">
                <div className="flex justify-between items-center py-2 border-b border-slate-100">
                  <span className="text-sm font-semibold text-slate-500">Predicted Coordinates</span>
                  <span className="text-sm font-mono text-slate-800 bg-slate-50 px-2 py-1 rounded border border-slate-200">
                    {targetLocation.lat.toFixed(5)}, {targetLocation.lng.toFixed(5)}
                  </span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-slate-100">
                  <span className="text-sm font-semibold text-slate-500">Locality</span>
                  <span className="text-sm font-medium text-blue-700 bg-blue-50 px-2 py-1 rounded border border-blue-100">
                    {geocodedData?.extracted_locality || "Not Extracted"}
                  </span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-slate-100">
                  <span className="text-sm font-semibold text-slate-500">Confidence Radius</span>
                  <span className="text-sm font-medium text-emerald-700 bg-emerald-50 px-2 py-1 rounded border border-emerald-100">
                    {targetLocation.radius} meters
                  </span>
                </div>
              </div>
              
              {geocodedData?.transliteration && (
                <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 mt-2">
                  <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2 block">
                    Transliteration
                  </span>
                  <p className="text-slate-800 text-[15px] font-medium leading-relaxed">
                    {transliteration}
                  </p>
                </div>
              )}

              {uniqueLandmarks.length > 0 && (
                <div className="mt-2">
                  <span className="text-[13px] font-bold text-amber-900 bg-amber-50 px-3 py-1.5 rounded-lg border border-amber-200 inline-flex">
                    Landmark: {uniqueLandmarks.join(', ')}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="p-6 border-t border-slate-200 bg-white shrink-0 flex flex-col gap-3">
          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 px-4 rounded-lg font-bold flex items-center justify-center gap-2 shadow-md">
            <Navigation className="w-5 h-5" />
            Start GPS Trail
          </button>
          
          <div className="flex gap-3 mt-1">
            <button className="flex-1 bg-white hover:bg-gray-50 text-slate-700 py-3.5 px-4 rounded-lg font-bold flex items-center justify-center gap-2 border border-slate-300 shadow-sm">
              <MessageSquare className="w-5 h-5 text-slate-500" />
              Remarks
            </button>
            <button className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-3.5 px-4 rounded-lg font-bold flex items-center justify-center gap-2 shadow-md">
              <CheckCircle2 className="w-5 h-5" />
              Outcome
            </button>
          </div>
        </div>
      </aside>

      <section className="flex-1 h-full relative z-0 bg-slate-200 overflow-hidden">
        {/* The map will now dynamically flyTo the updated coords without unmounting via key prop */}
        <Map 
          lat={targetLocation.lat} 
          lng={targetLocation.lng} 
          radius={targetLocation.radius} 
        />
      </section>
    </div>
  );
}
