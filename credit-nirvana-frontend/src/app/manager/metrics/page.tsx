import { 
  AlertTriangle, 
  TrendingDown, 
  MapPin, 
  BarChart3, 
  Users, 
  Settings, 
  ShieldAlert,
  ArrowDownRight
} from "lucide-react";
import { GeocodingQualityChart, TerritoryTrendsChart } from "@/components/charts/DashboardCharts";

export default function ManagerDashboardPage() {
  return (
    <div className="flex h-screen bg-gray-50 font-sans overflow-hidden">
      
      {/* Navigation Sidebar */}
      <aside className="w-[260px] bg-[#111827] text-gray-300 flex flex-col shrink-0">
        <div className="p-6">
          <h1 className="text-white text-xl font-bold flex items-center gap-2">
            <span className="w-8 h-8 rounded bg-teal-600 flex items-center justify-center text-sm">CN</span>
            CreditNirvana
          </h1>
        </div>
        
        <nav className="flex-1 px-4 py-2 space-y-1">
          <a href="#" className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-[#1f2937] text-white font-medium border border-[#374151]">
            <BarChart3 className="w-5 h-5 text-teal-400" />
            Performance Metrics
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-[#1f2937] hover:text-white transition-colors">
            <MapPin className="w-5 h-5" />
            Visit Dispatcher
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-[#1f2937] hover:text-white transition-colors">
            <Users className="w-5 h-5" />
            Field Agents
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-[#1f2937] hover:text-white transition-colors">
            <Settings className="w-5 h-5" />
            Settings
          </a>
        </nav>
        
        <div className="p-4 m-4 bg-[#1f2937] rounded-lg border border-[#374151] flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-teal-700 flex items-center justify-center text-white font-bold">
            JD
          </div>
          <div>
            <p className="text-sm font-semibold text-white">Jane Doe</p>
            <p className="text-xs text-gray-400">Territory Manager</p>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-y-auto">
        
        {/* Compliance & Governance Banner */}
        <div className="bg-amber-50 border-b border-amber-200 px-6 py-3 flex items-center gap-3 shrink-0">
          <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0" />
          <p className="text-sm font-medium text-amber-900">
            <strong>Restricted Access:</strong> Location data is strictly siloed for field operations and governed by DPDP retention limits.
          </p>
        </div>

        <div className="p-8 max-w-7xl mx-auto w-full flex-1">
          <header className="mb-8">
            <h2 className="text-2xl font-bold text-[#1e3a8a]">Metrics & Analytics</h2>
            <p className="text-slate-500 mt-1">Monitor geocoding accuracy and field visit performance.</p>
          </header>

          {/* KPI Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            
            {/* Card 1 */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Median Distance Error</h3>
              <div className="flex items-end gap-4">
                <span className="text-4xl font-bold text-[#1e3a8a]">12m</span>
                <div className="flex items-center text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md text-sm font-medium mb-1">
                  <ArrowDownRight className="w-4 h-4 mr-1" />
                  -4m (vs last mo)
                </div>
              </div>
            </div>

            {/* Card 2 */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Address Not Traceable Rate</h3>
              <div className="flex items-end gap-4">
                <span className="text-4xl font-bold text-[#1e3a8a]">4.2%</span>
                <div className="flex items-center text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md text-sm font-medium mb-1">
                  <TrendingDown className="w-4 h-4 mr-1" />
                  -1.5%
                </div>
              </div>
            </div>

            {/* Card 3 */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Confirmed Pin Updates</h3>
              <div className="flex items-end gap-4">
                <span className="text-4xl font-bold text-[#1e3a8a]">14,259</span>
                <div className="flex items-center text-slate-500 bg-slate-100 px-2 py-1 rounded-md text-sm font-medium mb-1">
                  This Month
                </div>
              </div>
            </div>

          </div>

          {/* Performance Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* Chart 1 */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
              <h3 className="text-lg font-bold text-[#1e3a8a] mb-6">Geocoding Quality Improvement</h3>
              <GeocodingQualityChart />
            </div>

            {/* Chart 2 */}
            <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
              <h3 className="text-lg font-bold text-[#1e3a8a] mb-6">"Not Traceable" Outcomes by Territory</h3>
              <TerritoryTrendsChart />
            </div>

          </div>

        </div>
      </main>
    </div>
  );
}

