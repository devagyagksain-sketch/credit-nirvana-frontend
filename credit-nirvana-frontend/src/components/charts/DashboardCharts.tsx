"use client";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const qualityData = [
  { month: "Jan", learned: 45, commercial: 65 },
  { month: "Feb", learned: 38, commercial: 64 },
  { month: "Mar", learned: 30, commercial: 66 },
  { month: "Apr", learned: 24, commercial: 65 },
  { month: "May", learned: 18, commercial: 63 },
  { month: "Jun", learned: 12, commercial: 65 },
];

const territoryData = [
  { territory: "North Zone", untraceable: 320 },
  { territory: "South Zone", untraceable: 150 },
  { territory: "East Zone", untraceable: 210 },
  { territory: "West Zone", untraceable: 180 },
];

export function GeocodingQualityChart() {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={qualityData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
          <XAxis dataKey="month" tick={{ fill: "#64748b", fontSize: 12 }} tickLine={false} axisLine={{ stroke: "#cbd5e1" }} />
          <YAxis tick={{ fill: "#64748b", fontSize: 12 }} tickLine={false} axisLine={false} label={{ value: 'Error Distance (m)', angle: -90, position: 'insideLeft', fill: '#94a3b8', fontSize: 12 }} />
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            labelStyle={{ fontWeight: 'bold', color: '#1e293b' }}
          />
          <Legend wrapperStyle={{ paddingTop: '10px' }} />
          <Line
            type="monotone"
            name="Learned Geocoder Error"
            dataKey="learned"
            stroke="#0d9488" // Teal
            strokeWidth={3}
            dot={{ r: 4, strokeWidth: 2 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            name="Commercial Geocoder Error"
            dataKey="commercial"
            stroke="#94a3b8" // Slate
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function TerritoryTrendsChart() {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={territoryData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
          <XAxis dataKey="territory" tick={{ fill: "#64748b", fontSize: 12 }} tickLine={false} axisLine={{ stroke: "#cbd5e1" }} />
          <YAxis tick={{ fill: "#64748b", fontSize: 12 }} tickLine={false} axisLine={false} />
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            cursor={{ fill: '#f1f5f9' }}
          />
          <Legend wrapperStyle={{ paddingTop: '10px' }} />
          <Bar 
            name="Addresses Not Traceable"
            dataKey="untraceable" 
            fill="#1e3a8a" // Deep navy blue
            radius={[4, 4, 0, 0]}
            maxBarSize={50}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

